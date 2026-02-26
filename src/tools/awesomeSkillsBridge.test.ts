import { describe, expect, it } from "vitest";
import {
    AwesomeSkillsBridgeError,
    resolveAwesomeSkillsBridgeConfig,
    runAwesomeSkillsSearch,
    type AwesomeSkillsBridgeConfig,
    type AwesomeSkillsBridgeRunner,
} from "./awesomeSkillsBridge.js";

function makeConfig(command: string[], runner?: AwesomeSkillsBridgeRunner): AwesomeSkillsBridgeConfig {
    return {
        enabled: true,
        command,
        timeoutMs: 10_000,
        cacheEnabled: true,
        cacheTtlMs: 30_000,
        cacheMaxEntries: 128,
        runner,
    };
}

describe("awesomeSkillsBridge", () => {
    it("falls back from auto to context when auto fails", async () => {
        const runner: AwesomeSkillsBridgeRunner = async (_command, args) => {
            const strategyIndex = args.indexOf("--strategy");
            const strategy = strategyIndex >= 0 ? args[strategyIndex + 1] : "auto";
            const query = args[1] ?? "";
            if (strategy === "auto") {
                throw new Error("auto failed");
            }
            return {
                stdout: JSON.stringify({
                    mode_used: strategy,
                    query,
                    count: 1,
                    results: [{ id: "demo", name: "demo" }],
                    alternatives: [],
                }),
            };
        };

        const result = await runAwesomeSkillsSearch(makeConfig(["python", "-m", "awesome_skills"], runner), {
            query: "plan migration",
            limit: 5,
            strategy: "auto",
        });

        expect(result.strategyUsed).toBe("context");
        expect(result.payload.mode_used).toBe("context");
        expect(result.payload.results).toHaveLength(1);
        expect(result.attempts.map((a) => a.strategy)).toEqual(["auto", "context"]);
        expect(result.attempts[0].error).toBeTruthy();
        expect(result.attempts[1].error).toBeUndefined();
    });

    it("uses classic only when classic strategy is requested", async () => {
        const runner: AwesomeSkillsBridgeRunner = async (_command, args) => {
            const strategyIndex = args.indexOf("--strategy");
            const strategy = strategyIndex >= 0 ? args[strategyIndex + 1] : "auto";
            return {
                stdout: JSON.stringify({
                    mode_used: strategy,
                    count: 1,
                    results: [{ id: "classic-demo", name: "classic-demo" }],
                }),
            };
        };

        const result = await runAwesomeSkillsSearch(makeConfig(["python", "-m", "awesome_skills"], runner), {
            query: "debug flaky tests",
            limit: 3,
            strategy: "classic",
        });

        expect(result.strategyUsed).toBe("classic");
        expect(result.attempts.map((a) => a.strategy)).toEqual(["classic"]);
        expect(result.payload.results).toHaveLength(1);
    });

    it("fails with deterministic error when all strategies return schema-invalid payloads", async () => {
        const runner: AwesomeSkillsBridgeRunner = async () => ({
            stdout: JSON.stringify({ mode_used: "context" }),
        });

        try {
            await runAwesomeSkillsSearch(makeConfig(["python", "-m", "awesome_skills"], runner), {
                query: "test query",
                limit: 2,
                strategy: "auto",
            });
            throw new Error("expected failure");
        } catch (error) {
            expect(error).toBeInstanceOf(AwesomeSkillsBridgeError);
            const bridgeError = error as AwesomeSkillsBridgeError;
            expect(bridgeError.code).toBe("BRIDGE_STRATEGY_FAILURE");
            expect(bridgeError.message).toContain("All bridge strategies failed");
            expect(Array.isArray(bridgeError.details?.attempts)).toBe(true);
        }
    });

    it("reports configuration errors for invalid command JSON", () => {
        const config = resolveAwesomeSkillsBridgeConfig({
            AWESOME_SKILLS_ENABLE_BRIDGE: "1",
            AWESOME_SKILLS_BRIDGE_COMMAND_JSON: '{"bad":"shape"}',
        });
        expect(config.enabled).toBe(true);
        expect(config.command).toEqual([]);
        expect(config.configError).toContain("must be a non-empty JSON array");
    });

    it("uses default runner path when custom runner is absent", async () => {
        const config = resolveAwesomeSkillsBridgeConfig({
            AWESOME_SKILLS_ENABLE_BRIDGE: "1",
            AWESOME_SKILLS_BRIDGE_COMMAND_JSON: JSON.stringify([
                "bash",
                "-lc",
                "printf '{\\\"mode_used\\\":\\\"classic\\\",\\\"results\\\":[{\\\"id\\\":\\\"ok\\\"}]}'",
            ]),
        });

        const result = await runAwesomeSkillsSearch(config, {
            query: "ignored by mock command",
            limit: 1,
            strategy: "classic",
        });

        expect(result.strategyUsed).toBe("classic");
        expect(result.payload.results).toHaveLength(1);
    });

    it("returns cached result for identical repeated requests", async () => {
        let callCount = 0;
        const runner: AwesomeSkillsBridgeRunner = async () => {
            callCount += 1;
            return {
                stdout: JSON.stringify({
                    mode_used: "classic",
                    count: 1,
                    results: [{ id: "cache-demo", name: "cache-demo" }],
                }),
            };
        };

        const config = makeConfig(["python", "-m", "awesome_skills"], runner);
        const request = {
            query: "cache warmup query",
            limit: 3,
            strategy: "classic" as const,
        };

        const first = await runAwesomeSkillsSearch(config, request);
        const second = await runAwesomeSkillsSearch(config, request);

        expect(callCount).toBe(1);
        expect(first.payload.results).toHaveLength(1);
        expect(second.payload.results).toHaveLength(1);
    });

    it("coalesces concurrent identical requests into one bridge execution", async () => {
        let callCount = 0;
        const runner: AwesomeSkillsBridgeRunner = async () => {
            callCount += 1;
            await new Promise((resolve) => setTimeout(resolve, 30));
            return {
                stdout: JSON.stringify({
                    mode_used: "classic",
                    count: 1,
                    results: [{ id: "dedupe-demo", name: "dedupe-demo" }],
                }),
            };
        };

        const config = makeConfig(["python", "-m", "awesome_skills"], runner);
        const request = {
            query: "coalesce query",
            limit: 5,
            strategy: "classic" as const,
        };

        const [resultA, resultB] = await Promise.all([
            runAwesomeSkillsSearch(config, request),
            runAwesomeSkillsSearch(config, request),
        ]);

        expect(callCount).toBe(1);
        expect(resultA.payload.results).toHaveLength(1);
        expect(resultB.payload.results).toHaveLength(1);
    });

    it("expires cached entries when TTL elapses", async () => {
        let callCount = 0;
        const runner: AwesomeSkillsBridgeRunner = async () => {
            callCount += 1;
            return {
                stdout: JSON.stringify({
                    mode_used: "classic",
                    count: 1,
                    results: [{ id: `ttl-demo-${callCount}`, name: "ttl-demo" }],
                }),
            };
        };

        const config: AwesomeSkillsBridgeConfig = {
            ...makeConfig(["python", "-m", "awesome_skills"], runner),
            cacheTtlMs: 100,
        };
        const request = {
            query: "ttl query",
            limit: 2,
            strategy: "classic" as const,
        };

        const first = await runAwesomeSkillsSearch(config, request);
        await new Promise((resolve) => setTimeout(resolve, 150));
        const second = await runAwesomeSkillsSearch(config, request);

        expect(callCount).toBe(2);
        expect(first.payload.results[0]?.id).toBe("ttl-demo-1");
        expect(second.payload.results[0]?.id).toBe("ttl-demo-2");
    });
});

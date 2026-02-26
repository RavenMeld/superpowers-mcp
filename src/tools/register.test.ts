import { describe, it, expect, beforeAll } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { registerTools } from "./register.js";
import type { Skill } from "../skills/types.js";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

function makeTestSkills(): Skill[] {
    return [
        {
            metadata: { name: "brainstorming", description: "Explore ideas" },
            directoryName: "brainstorming",
            content: "# Brainstorming\n\nFull content here.",
            files: [],
        },
        {
            metadata: { name: "tdd", description: "Test driven development" },
            directoryName: "test-driven-development",
            content: "# TDD\n\nTDD content.",
            files: [
                {
                    name: "anti-patterns.md",
                    relativePath: "test-driven-development/anti-patterns.md",
                },
            ],
        },
    ];
}

describe("registerTools", () => {
    let client: Client;

    beforeAll(async () => {
        const server = new McpServer({ name: "test", version: "0.0.1" });
        const skills = makeTestSkills();
        registerTools(server, skills);

        const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
        client = new Client({ name: "test-client", version: "0.0.1" }, { capabilities: {} });
        await server.connect(serverTransport);
        await client.connect(clientTransport);
    });

    it("should register list_skills, use_skill, and get_skill_file tools", async () => {
        const result = await client.listTools();
        const toolNames = result.tools.map((t) => t.name);
        expect(toolNames).toContain("list_skills");
        expect(toolNames).toContain("use_skill");
        expect(toolNames).toContain("get_skill_file");
        expect(toolNames).toHaveLength(3);
    });

    it("list_skills should return all skills with metadata", async () => {
        const result = await client.callTool({ name: "list_skills", arguments: {} });
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        const skills = JSON.parse(text);
        expect(skills).toHaveLength(2);
        expect(skills[0].name).toBe("brainstorming");
        expect(skills[0].description).toBe("Explore ideas");
        expect(skills[0].files).toEqual([]);
        expect(skills[1].name).toBe("test-driven-development");
        expect(skills[1].files).toEqual(["anti-patterns.md"]);
    });

    it("use_skill should return full skill content", async () => {
        const result = await client.callTool({
            name: "use_skill",
            arguments: { name: "brainstorming" },
        });
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        expect(text).toBe("# Brainstorming\n\nFull content here.");
        expect(result.isError).toBeFalsy();
    });

    it("use_skill should return error for unknown skill", async () => {
        const result = await client.callTool({
            name: "use_skill",
            arguments: { name: "nonexistent" },
        });
        expect(result.isError).toBe(true);
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        expect(text).toContain("not found");
        expect(text).toContain("list_skills");
    });

    it("get_skill_file should return error for unknown skill", async () => {
        const result = await client.callTool({
            name: "get_skill_file",
            arguments: { skill: "nonexistent", file: "foo.md" },
        });
        expect(result.isError).toBe(true);
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        expect(text).toContain("not found");
    });

    it("get_skill_file should return error for unknown file in valid skill", async () => {
        const result = await client.callTool({
            name: "get_skill_file",
            arguments: { skill: "brainstorming", file: "nonexistent.md" },
        });
        expect(result.isError).toBe(true);
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        expect(text).toContain("not found");
        expect(text).toContain("brainstorming");
    });

    it("get_skill_file should list available files when file not found", async () => {
        const result = await client.callTool({
            name: "get_skill_file",
            arguments: { skill: "test-driven-development", file: "wrong.md" },
        });
        expect(result.isError).toBe(true);
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        expect(text).toContain("anti-patterns.md");
    });

    it("get_skill_file should return error when no skillsDir provided", async () => {
        const result = await client.callTool({
            name: "get_skill_file",
            arguments: { skill: "test-driven-development", file: "anti-patterns.md" },
        });
        expect(result.isError).toBe(true);
        const text = (result.content as Array<{ type: string; text: string }>)[0].text;
        expect(text).toContain("skills directory not available");
    });
});

describe("registerTools awesome skills bridge", () => {
    it("should register and execute search_awesome_skills when bridge is enabled", async () => {
        const testRoot = join(tmpdir(), `superpowers-mcp-bridge-${Date.now()}`);
        mkdirSync(testRoot, { recursive: true });
        const mockBridgePath = join(testRoot, "mock-bridge.mjs");
        writeFileSync(
            mockBridgePath,
            `#!/usr/bin/env node
const args = process.argv.slice(2);
const query = args[1] ?? "";
const getArg = (flag) => {
  const idx = args.indexOf(flag);
  return idx >= 0 && idx + 1 < args.length ? args[idx + 1] : undefined;
};
const strategy = getArg("--strategy") ?? "auto";
const limit = Number(getArg("--limit") ?? "8");
if (query.includes("coalesce")) {
  await new Promise((resolve) => setTimeout(resolve, 60));
}
process.stdout.write(JSON.stringify({
  mode_used: strategy === "classic" ? "classic" : "context",
  query,
  limit,
  results: [{ id: "demo-skill", name: "demo-skill" }]
}), () => {});`,
            "utf-8"
        );

        const bridgeCommand =
            process.platform === "win32"
                ? ["node", mockBridgePath]
                : [
                      "bash",
                      "-lc",
                      [
                          "query=\"$1\"",
                          "strategy=\"$3\"",
                          "limit=\"$5\"",
                          "mode=\"context\"",
                          "if [ \"$strategy\" = \"classic\" ]; then mode=\"classic\"; fi",
                          "if [[ \"$query\" == *coalesce* ]]; then sleep 0.06; fi",
                          "printf '{\"mode_used\":\"%s\",\"query\":\"%s\",\"limit\":%s,\"results\":[{\"id\":\"demo-skill\",\"name\":\"demo-skill\"}]}' \"$mode\" \"$query\" \"$limit\"",
                      ].join("; "),
                  ];

        const server = new McpServer({ name: "test-bridge", version: "0.0.1" });
        registerTools(server, makeTestSkills(), undefined, {
            env: {
                AWESOME_SKILLS_ENABLE_BRIDGE: "1",
                AWESOME_SKILLS_BRIDGE_COMMAND_JSON: JSON.stringify(bridgeCommand),
            },
        });

        const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
        const client = new Client({ name: "test-client", version: "0.0.1" }, { capabilities: {} });
        await server.connect(serverTransport);
        await client.connect(clientTransport);

        try {
            const listed = await client.listTools();
            const toolNames = listed.tools.map((t) => t.name);
            expect(toolNames).toContain("search_awesome_skills");

            const call = await client.callTool({
                name: "search_awesome_skills",
                arguments: {
                    query: "plan a feature",
                    strategy: "auto",
                    limit: 3,
                },
            });

            expect(call.isError).toBeFalsy();
            const text = (call.content as Array<{ type: string; text: string }>)[0].text;
            const payload = JSON.parse(text) as {
                bridge: {
                    command: string[];
                    timeout_ms: number;
                    cache_hit: boolean;
                    coalesced: boolean;
                };
                result: { query: string; limit: number; mode_used: string };
            };
            const expectedCommandHead = process.platform === "win32" ? "node" : "bash";
            expect(payload.bridge.command[0]).toBe(expectedCommandHead);
            expect(payload.bridge.cache_hit).toBe(false);
            expect(payload.bridge.coalesced).toBe(false);
            expect(payload.result.query).toBe("plan a feature");
            expect(payload.result.limit).toBe(3);
            expect(payload.result.mode_used).toBe("context");

            const callRepeat = await client.callTool({
                name: "search_awesome_skills",
                arguments: {
                    query: "plan a feature",
                    strategy: "auto",
                    limit: 3,
                },
            });
            expect(callRepeat.isError).toBeFalsy();
            const repeatText = (callRepeat.content as Array<{ type: string; text: string }>)[0].text;
            const repeatPayload = JSON.parse(repeatText) as {
                bridge: {
                    cache_hit: boolean;
                    coalesced: boolean;
                };
            };
            expect(repeatPayload.bridge.cache_hit).toBe(true);
            expect(repeatPayload.bridge.coalesced).toBe(false);

            const [parallelA, parallelB] = await Promise.all([
                client.callTool({
                    name: "search_awesome_skills",
                    arguments: {
                        query: "coalesce smoke check",
                        strategy: "auto",
                        limit: 3,
                    },
                }),
                client.callTool({
                    name: "search_awesome_skills",
                    arguments: {
                        query: "coalesce smoke check",
                        strategy: "auto",
                        limit: 3,
                    },
                }),
            ]);

            const parallelPayloadA = JSON.parse(
                (parallelA.content as Array<{ type: string; text: string }>)[0].text
            ) as {
                bridge: { cache_hit: boolean; coalesced: boolean };
            };
            const parallelPayloadB = JSON.parse(
                (parallelB.content as Array<{ type: string; text: string }>)[0].text
            ) as {
                bridge: { cache_hit: boolean; coalesced: boolean };
            };
            expect(parallelPayloadA.bridge.cache_hit).toBe(false);
            expect(parallelPayloadB.bridge.cache_hit).toBe(false);
            expect([parallelPayloadA.bridge.coalesced, parallelPayloadB.bridge.coalesced].sort()).toEqual([
                false,
                true,
            ]);
        } finally {
            rmSync(testRoot, { recursive: true, force: true });
        }
    });

    it("should return structured bridge error codes when bridge configuration is invalid", async () => {
        const server = new McpServer({ name: "test-bridge-error", version: "0.0.1" });
        registerTools(server, makeTestSkills(), undefined, {
            env: {
                AWESOME_SKILLS_ENABLE_BRIDGE: "1",
                AWESOME_SKILLS_BRIDGE_COMMAND_JSON: '{"invalid":"shape"}',
            },
        });

        const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
        const client = new Client({ name: "test-client", version: "0.0.1" }, { capabilities: {} });
        await server.connect(serverTransport);
        await client.connect(clientTransport);

        const call = await client.callTool({
            name: "search_awesome_skills",
            arguments: {
                query: "debug flaky tests",
            },
        });

        expect(call.isError).toBe(true);
        const text = (call.content as Array<{ type: string; text: string }>)[0].text;
        const payload = JSON.parse(text) as {
            error: { code: string; message: string; hints: string[] };
            bridge: { timeout_ms: number };
        };
        expect(payload.error.code).toBe("BRIDGE_CONFIG");
        expect(payload.error.message).toContain("non-empty JSON array");
        expect(Array.isArray(payload.error.hints)).toBe(true);
        expect(payload.bridge.timeout_ms).toBeGreaterThan(0);
    });
});

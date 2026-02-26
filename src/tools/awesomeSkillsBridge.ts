import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { z } from "zod";

const execFileAsync = promisify(execFile);

export type AwesomeSkillsStrategy = "auto" | "classic" | "context";

export interface AwesomeSkillsBridgeConfig {
    enabled: boolean;
    command: string[];
    timeoutMs: number;
    defaultDbPath?: string;
    defaultContextAliasJson?: string;
    configError?: string;
    runner?: AwesomeSkillsBridgeRunner;
}

export interface AwesomeSkillsSearchRequest {
    query: string;
    limit: number;
    strategy: AwesomeSkillsStrategy;
    dbPath?: string;
    contextAliasJson?: string;
}

export interface AwesomeSkillsSearchResult {
    payload: AwesomeSkillsBridgePayload;
    command: string[];
    strategyUsed: AwesomeSkillsStrategy;
    attempts: AwesomeSkillsSearchAttempt[];
}

export interface AwesomeSkillsSearchAttempt {
    strategy: AwesomeSkillsStrategy;
    command: string[];
    error?: string;
}

export type AwesomeSkillsBridgeRunner = (
    command: string,
    args: string[],
    options: { timeoutMs: number }
) => Promise<{ stdout: string }>;

const AwesomeSkillsBridgeResultSchema = z
    .object({
        mode_used: z.enum(["auto", "classic", "context"]).optional(),
        query: z.string().optional(),
        count: z.number().int().nonnegative().optional(),
        context: z.record(z.string(), z.unknown()).nullable().optional(),
        results: z.array(z.record(z.string(), z.unknown())),
        alternatives: z.array(z.record(z.string(), z.unknown())).optional(),
    })
    .passthrough();

export type AwesomeSkillsBridgePayload = z.infer<typeof AwesomeSkillsBridgeResultSchema>;

function isTruthy(input: string | undefined): boolean {
    if (!input) {
        return false;
    }
    const normalized = input.trim().toLowerCase();
    return normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "on";
}

function parseTimeoutMs(input: string | undefined): number {
    if (!input) {
        return 15_000;
    }
    const parsed = Number.parseInt(input, 10);
    if (!Number.isFinite(parsed) || Number.isNaN(parsed)) {
        return 15_000;
    }
    if (parsed < 1_000) {
        return 1_000;
    }
    if (parsed > 120_000) {
        return 120_000;
    }
    return parsed;
}

function parseCommandJson(raw: string | undefined): string[] | undefined {
    if (!raw) {
        return undefined;
    }
    const parsed = JSON.parse(raw) as unknown;
    if (!Array.isArray(parsed) || parsed.length === 0) {
        throw new Error("AWESOME_SKILLS_BRIDGE_COMMAND_JSON must be a non-empty JSON array.");
    }
    const command = parsed.map((item) => {
        if (typeof item !== "string" || item.trim().length === 0) {
            throw new Error("AWESOME_SKILLS_BRIDGE_COMMAND_JSON must contain only non-empty strings.");
        }
        return item;
    });
    return command;
}

export function resolveAwesomeSkillsBridgeConfig(
    env: NodeJS.ProcessEnv = process.env
): AwesomeSkillsBridgeConfig {
    const enabled = isTruthy(env.AWESOME_SKILLS_ENABLE_BRIDGE);
    const timeoutMs = parseTimeoutMs(env.AWESOME_SKILLS_BRIDGE_TIMEOUT_MS);
    const defaultDbPath = env.AWESOME_SKILLS_DB_PATH;
    const defaultContextAliasJson = env.AWESOME_SKILLS_CONTEXT_ALIAS_JSON;

    try {
        const command =
            parseCommandJson(env.AWESOME_SKILLS_BRIDGE_COMMAND_JSON) ??
            [env.AWESOME_SKILLS_PYTHON ?? "python", "-m", "awesome_skills"];
        return {
            enabled,
            command,
            timeoutMs,
            defaultDbPath,
            defaultContextAliasJson,
        };
    } catch (error) {
        const message = error instanceof Error ? error.message : "Unknown configuration error.";
        return {
            enabled,
            command: [],
            timeoutMs,
            defaultDbPath,
            defaultContextAliasJson,
            configError: message,
        };
    }
}

export async function runAwesomeSkillsSearch(
    config: AwesomeSkillsBridgeConfig,
    request: AwesomeSkillsSearchRequest
): Promise<AwesomeSkillsSearchResult> {
    if (!config.enabled) {
        throw new Error("Awesome Skills bridge is disabled.");
    }
    if (config.configError) {
        throw new Error(config.configError);
    }
    if (config.command.length === 0) {
        throw new Error("No bridge command configured.");
    }

    const dbPath = request.dbPath ?? config.defaultDbPath;
    const contextAliasJson = request.contextAliasJson ?? config.defaultContextAliasJson;

    const attempts: AwesomeSkillsSearchAttempt[] = [];
    const strategyPlan = buildStrategyPlan(request.strategy);
    const runner = config.runner ?? defaultBridgeRunner;

    for (const strategy of strategyPlan) {
        const command = buildBridgeCommand(config.command, request.query, request.limit, strategy, dbPath, contextAliasJson);
        const attempt: AwesomeSkillsSearchAttempt = { strategy, command };
        attempts.push(attempt);

        try {
            const [execCommand, ...execArgs] = command;
            const { stdout } = await runner(execCommand, execArgs, { timeoutMs: config.timeoutMs });
            const payload = parseBridgePayload(stdout);
            return { payload, command, strategyUsed: strategy, attempts };
        } catch (error) {
            const message = error instanceof Error ? error.message : "Unknown bridge error.";
            attempt.error = message;
        }
    }

    const planText = strategyPlan.join(" -> ");
    const lastError = attempts.at(-1)?.error ?? "Unknown bridge error.";
    throw new Error(`All bridge strategies failed (${planText}). Last error: ${lastError}`);
}

function buildStrategyPlan(requested: AwesomeSkillsStrategy): AwesomeSkillsStrategy[] {
    if (requested === "classic") {
        return ["classic"];
    }
    if (requested === "context") {
        return ["context", "classic"];
    }
    return ["auto", "context", "classic"];
}

function buildBridgeCommand(
    baseCommand: string[],
    query: string,
    limit: number,
    strategy: AwesomeSkillsStrategy,
    dbPath?: string,
    contextAliasJson?: string
): string[] {
    const command = [
        ...baseCommand,
        "search",
        query,
        "--strategy",
        strategy,
        "--limit",
        String(limit),
        "--json",
    ];

    if (dbPath) {
        command.push("--db", dbPath);
    }
    if (contextAliasJson) {
        command.push("--context-alias-json", contextAliasJson);
    }
    return command;
}

function parseBridgePayload(stdout: string): AwesomeSkillsBridgePayload {
    const text = stdout.trim();
    if (!text) {
        throw new Error("Bridge command returned empty output.");
    }

    let jsonPayload: unknown;
    try {
        jsonPayload = JSON.parse(text);
    } catch {
        throw new Error(`Bridge command did not return valid JSON. Output: ${text.slice(0, 300)}`);
    }

    const parsed = AwesomeSkillsBridgeResultSchema.safeParse(jsonPayload);
    if (!parsed.success) {
        const firstIssue = parsed.error.issues[0];
        const path = firstIssue?.path.join(".") || "<root>";
        const detail = firstIssue ? `${path}: ${firstIssue.message}` : "Unknown schema error.";
        throw new Error(`Bridge response schema mismatch: ${detail}`);
    }
    return parsed.data;
}

async function defaultBridgeRunner(
    command: string,
    args: string[],
    options: { timeoutMs: number }
): Promise<{ stdout: string }> {
    const { stdout } = await execFileAsync(command, args, {
        encoding: "utf8",
        timeout: options.timeoutMs,
        maxBuffer: 4 * 1024 * 1024,
    });
    return { stdout };
}

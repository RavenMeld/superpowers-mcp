import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export type AwesomeSkillsStrategy = "auto" | "classic" | "context";

export interface AwesomeSkillsBridgeConfig {
    enabled: boolean;
    command: string[];
    timeoutMs: number;
    defaultDbPath?: string;
    defaultContextAliasJson?: string;
    configError?: string;
}

export interface AwesomeSkillsSearchRequest {
    query: string;
    limit: number;
    strategy: AwesomeSkillsStrategy;
    dbPath?: string;
    contextAliasJson?: string;
}

export interface AwesomeSkillsSearchResult {
    payload: unknown;
    command: string[];
}

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

    const command = [
        ...config.command,
        "search",
        request.query,
        "--strategy",
        request.strategy,
        "--limit",
        String(request.limit),
        "--json",
    ];

    if (dbPath) {
        command.push("--db", dbPath);
    }
    if (contextAliasJson) {
        command.push("--context-alias-json", contextAliasJson);
    }

    const [execCommand, ...execArgs] = command;
    const { stdout } = await execFileAsync(execCommand, execArgs, {
        encoding: "utf8",
        timeout: config.timeoutMs,
        maxBuffer: 4 * 1024 * 1024,
    });

    const text = stdout.trim();
    if (!text) {
        throw new Error("Bridge command returned empty output.");
    }

    let payload: unknown;
    try {
        payload = JSON.parse(text);
    } catch {
        throw new Error(`Bridge command did not return valid JSON. Output: ${text.slice(0, 300)}`);
    }

    return { payload, command };
}

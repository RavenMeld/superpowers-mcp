import { execFile } from "node:child_process";
import { promisify } from "node:util";
import { z } from "zod";

const execFileAsync = promisify(execFile);

export type AwesomeSkillsStrategy = "auto" | "classic" | "context";

export interface AwesomeSkillsBridgeConfig {
    enabled: boolean;
    command: string[];
    timeoutMs: number;
    cacheEnabled: boolean;
    cacheTtlMs: number;
    cacheMaxEntries: number;
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

export type AwesomeSkillsBridgeErrorCode =
    | "BRIDGE_DISABLED"
    | "BRIDGE_CONFIG"
    | "BRIDGE_EXEC"
    | "BRIDGE_EMPTY_OUTPUT"
    | "BRIDGE_INVALID_JSON"
    | "BRIDGE_SCHEMA_MISMATCH"
    | "BRIDGE_STRATEGY_FAILURE";

export class AwesomeSkillsBridgeError extends Error {
    readonly code: AwesomeSkillsBridgeErrorCode;
    readonly details?: Record<string, unknown>;

    constructor(code: AwesomeSkillsBridgeErrorCode, message: string, details?: Record<string, unknown>) {
        super(message);
        this.name = "AwesomeSkillsBridgeError";
        this.code = code;
        this.details = details;
    }
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

interface AwesomeSkillsCacheEntry {
    value: AwesomeSkillsSearchResult;
    expiresAt: number;
}

const awesomeSkillsCache = new Map<string, AwesomeSkillsCacheEntry>();
const awesomeSkillsInFlight = new Map<string, Promise<AwesomeSkillsSearchResult>>();
const awesomeSkillsRunnerIds = new WeakMap<AwesomeSkillsBridgeRunner, number>();
let awesomeSkillsRunnerIdCounter = 0;

function isTruthy(input: string | undefined): boolean {
    if (!input) {
        return false;
    }
    const normalized = input.trim().toLowerCase();
    return normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "on";
}

function parseBooleanWithDefault(input: string | undefined, fallback: boolean): boolean {
    if (!input) {
        return fallback;
    }
    const normalized = input.trim().toLowerCase();
    if (normalized === "1" || normalized === "true" || normalized === "yes" || normalized === "on") {
        return true;
    }
    if (normalized === "0" || normalized === "false" || normalized === "no" || normalized === "off") {
        return false;
    }
    return fallback;
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

function parseBoundedInt(input: string | undefined, fallback: number, min: number, max: number): number {
    if (!input) {
        return fallback;
    }
    const parsed = Number.parseInt(input, 10);
    if (!Number.isFinite(parsed) || Number.isNaN(parsed)) {
        return fallback;
    }
    if (parsed < min) {
        return min;
    }
    if (parsed > max) {
        return max;
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
    const cacheEnabled = parseBooleanWithDefault(env.AWESOME_SKILLS_BRIDGE_CACHE_ENABLED, true);
    const cacheTtlMs = parseBoundedInt(env.AWESOME_SKILLS_BRIDGE_CACHE_TTL_MS, 30_000, 100, 600_000);
    const cacheMaxEntries = parseBoundedInt(env.AWESOME_SKILLS_BRIDGE_CACHE_MAX_ENTRIES, 128, 1, 1_000);
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
            cacheEnabled,
            cacheTtlMs,
            cacheMaxEntries,
            defaultDbPath,
            defaultContextAliasJson,
        };
    } catch (error) {
        const message = error instanceof Error ? error.message : "Unknown configuration error.";
        return {
            enabled,
            command: [],
            timeoutMs,
            cacheEnabled,
            cacheTtlMs,
            cacheMaxEntries,
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
        throw new AwesomeSkillsBridgeError("BRIDGE_DISABLED", "Awesome Skills bridge is disabled.");
    }
    if (config.configError) {
        throw new AwesomeSkillsBridgeError("BRIDGE_CONFIG", config.configError);
    }
    if (config.command.length === 0) {
        throw new AwesomeSkillsBridgeError("BRIDGE_CONFIG", "No bridge command configured.");
    }

    const dbPath = request.dbPath ?? config.defaultDbPath;
    const contextAliasJson = request.contextAliasJson ?? config.defaultContextAliasJson;
    const runner = config.runner ?? defaultBridgeRunner;
    const cacheKey = buildCacheKey(config, request, dbPath, contextAliasJson, runner);

    if (config.cacheEnabled) {
        const cached = readCachedResult(cacheKey, Date.now());
        if (cached) {
            return cached;
        }
    }

    const inFlight = awesomeSkillsInFlight.get(cacheKey);
    if (inFlight) {
        return inFlight;
    }

    const runPromise = executeSearchWithFallback(config, request, dbPath, contextAliasJson, runner)
        .then((result) => {
            if (config.cacheEnabled) {
                writeCachedResult(cacheKey, result, config.cacheTtlMs, config.cacheMaxEntries, Date.now());
            }
            return result;
        })
        .finally(() => {
            awesomeSkillsInFlight.delete(cacheKey);
        });

    awesomeSkillsInFlight.set(cacheKey, runPromise);
    return runPromise;
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

async function executeSearchWithFallback(
    config: AwesomeSkillsBridgeConfig,
    request: AwesomeSkillsSearchRequest,
    dbPath: string | undefined,
    contextAliasJson: string | undefined,
    runner: AwesomeSkillsBridgeRunner
): Promise<AwesomeSkillsSearchResult> {
    const attempts: AwesomeSkillsSearchAttempt[] = [];
    const strategyPlan = buildStrategyPlan(request.strategy);

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
            const bridgeError = normalizeBridgeError(error);
            attempt.error = `${bridgeError.code}: ${bridgeError.message}`;
        }
    }

    const planText = strategyPlan.join(" -> ");
    const lastError = attempts.at(-1)?.error ?? "BRIDGE_EXEC: Unknown bridge error.";
    throw new AwesomeSkillsBridgeError(
        "BRIDGE_STRATEGY_FAILURE",
        `All bridge strategies failed (${planText}). Last error: ${lastError}`,
        { attempts }
    );
}

function buildCacheKey(
    config: AwesomeSkillsBridgeConfig,
    request: AwesomeSkillsSearchRequest,
    dbPath: string | undefined,
    contextAliasJson: string | undefined,
    runner: AwesomeSkillsBridgeRunner
): string {
    return JSON.stringify({
        command: config.command,
        timeoutMs: config.timeoutMs,
        query: request.query,
        limit: request.limit,
        strategy: request.strategy,
        dbPath: dbPath ?? null,
        contextAliasJson: contextAliasJson ?? null,
        runner: getRunnerId(runner),
    });
}

function getRunnerId(runner: AwesomeSkillsBridgeRunner): number {
    const existing = awesomeSkillsRunnerIds.get(runner);
    if (typeof existing === "number") {
        return existing;
    }
    awesomeSkillsRunnerIdCounter += 1;
    awesomeSkillsRunnerIds.set(runner, awesomeSkillsRunnerIdCounter);
    return awesomeSkillsRunnerIdCounter;
}

function readCachedResult(cacheKey: string, now: number): AwesomeSkillsSearchResult | undefined {
    const entry = awesomeSkillsCache.get(cacheKey);
    if (!entry) {
        return undefined;
    }
    if (entry.expiresAt <= now) {
        awesomeSkillsCache.delete(cacheKey);
        return undefined;
    }
    return entry.value;
}

function writeCachedResult(
    cacheKey: string,
    result: AwesomeSkillsSearchResult,
    ttlMs: number,
    maxEntries: number,
    now: number
): void {
    pruneExpiredCacheEntries(now);
    if (awesomeSkillsCache.has(cacheKey)) {
        awesomeSkillsCache.delete(cacheKey);
    }
    while (awesomeSkillsCache.size >= maxEntries) {
        const oldestKey = awesomeSkillsCache.keys().next().value;
        if (!oldestKey) {
            break;
        }
        awesomeSkillsCache.delete(oldestKey);
    }
    awesomeSkillsCache.set(cacheKey, {
        value: result,
        expiresAt: now + ttlMs,
    });
}

function pruneExpiredCacheEntries(now: number): void {
    for (const [key, entry] of awesomeSkillsCache) {
        if (entry.expiresAt <= now) {
            awesomeSkillsCache.delete(key);
        }
    }
}

function parseBridgePayload(stdout: string): AwesomeSkillsBridgePayload {
    const text = stdout.trim();
    if (!text) {
        throw new AwesomeSkillsBridgeError("BRIDGE_EMPTY_OUTPUT", "Bridge command returned empty output.");
    }

    let jsonPayload: unknown;
    try {
        jsonPayload = JSON.parse(text);
    } catch {
        throw new AwesomeSkillsBridgeError(
            "BRIDGE_INVALID_JSON",
            `Bridge command did not return valid JSON. Output: ${text.slice(0, 300)}`
        );
    }

    const parsed = AwesomeSkillsBridgeResultSchema.safeParse(jsonPayload);
    if (!parsed.success) {
        const firstIssue = parsed.error.issues[0];
        const path = firstIssue?.path.join(".") || "<root>";
        const detail = firstIssue ? `${path}: ${firstIssue.message}` : "Unknown schema error.";
        throw new AwesomeSkillsBridgeError("BRIDGE_SCHEMA_MISMATCH", `Bridge response schema mismatch: ${detail}`);
    }
    return parsed.data;
}

function normalizeBridgeError(error: unknown): AwesomeSkillsBridgeError {
    if (error instanceof AwesomeSkillsBridgeError) {
        return error;
    }
    if (error instanceof Error) {
        return new AwesomeSkillsBridgeError("BRIDGE_EXEC", error.message);
    }
    return new AwesomeSkillsBridgeError("BRIDGE_EXEC", "Unknown bridge execution error.");
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

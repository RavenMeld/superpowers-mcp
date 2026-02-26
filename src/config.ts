import Conf from "conf";
import { mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

interface SuperpowersConfig {
    skillsDir?: string;
    lastUpdateCheck?: number;
    useLocalSkills?: boolean;
}

const FALLBACK_CONFIG_DIR = join(tmpdir(), "superpowers-mcp-config");

export function resolveConfigDirOverride(env: NodeJS.ProcessEnv = process.env): string | undefined {
    const configured = env.SUPERPOWERS_CONFIG_DIR?.trim();
    if (!configured) {
        return undefined;
    }
    return resolve(configured);
}

function createConfigStore(cwd?: string): Conf<SuperpowersConfig> {
    const options: {
        projectName: string;
        defaults: SuperpowersConfig;
        cwd?: string;
    } = {
        projectName: "superpowers-mcp",
        defaults: {
            useLocalSkills: false,
        },
    };
    if (cwd) {
        options.cwd = cwd;
    }
    return new Conf<SuperpowersConfig>(options);
}

function ensureFallbackConfigStore(): Conf<SuperpowersConfig> {
    mkdirSync(FALLBACK_CONFIG_DIR, { recursive: true });
    return createConfigStore(FALLBACK_CONFIG_DIR);
}

let fallbackModeLogged = false;
let fallbackConfig: Conf<SuperpowersConfig> | undefined;
const primaryConfig = createConfigStore(resolveConfigDirOverride(process.env));

function withConfigStore<T>(fn: (store: Conf<SuperpowersConfig>) => T): T {
    try {
        return fn(primaryConfig);
    } catch (error) {
        if (!fallbackConfig) {
            fallbackConfig = ensureFallbackConfigStore();
        }
        if (!fallbackModeLogged) {
            const reason = error instanceof Error ? error.message : String(error);
            console.error(
                `superpowers-mcp: config store fallback enabled at ${FALLBACK_CONFIG_DIR} (${reason})`
            );
            fallbackModeLogged = true;
        }
        return fn(fallbackConfig);
    }
}

export function getConfig(): SuperpowersConfig {
    return withConfigStore((store) => store.store);
}

export function setConfig(newConfig: Partial<SuperpowersConfig>): void {
    withConfigStore((store) => store.set(newConfig));
}

export function getSkillsDir(): string | undefined {
    return withConfigStore((store) => store.get("skillsDir"));
}

export function setSkillsDir(dir: string): void {
    withConfigStore((store) => store.set("skillsDir", dir));
}

export function getLastUpdateCheck(): number | undefined {
    return withConfigStore((store) => store.get("lastUpdateCheck"));
}

export function setLastUpdateCheck(timestamp: number): void {
    withConfigStore((store) => store.set("lastUpdateCheck", timestamp));
}

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import type { Skill } from "../skills/types.js";
import {
    AwesomeSkillsBridgeError,
    resolveAwesomeSkillsBridgeConfig,
    runAwesomeSkillsSearch,
    type AwesomeSkillsStrategy,
} from "./awesomeSkillsBridge.js";

export interface RegisterToolsOptions {
    env?: NodeJS.ProcessEnv;
}

export function registerTools(
    server: McpServer,
    skills: Skill[],
    skillsDir?: string,
    options: RegisterToolsOptions = {}
): void {
    const skillMap = new Map<string, Skill>();
    for (const skill of skills) {
        skillMap.set(skill.directoryName, skill);
    }
    const bridgeConfig = resolveAwesomeSkillsBridgeConfig(options.env ?? process.env);

    server.tool(
        "list_skills",
        "List all available superpowers skills with their descriptions and supporting files",
        async () => {
            const listing = skills.map((s) => ({
                name: s.directoryName,
                displayName: s.metadata.name,
                description: s.metadata.description,
                files: s.files.map((f) => f.name),
            }));
            return {
                content: [
                    { type: "text" as const, text: JSON.stringify(listing, null, 2) },
                ],
            };
        }
    );

    server.tool(
        "use_skill",
        "Load a superpowers skill by name. Returns the full skill content to follow as instructions.",
        {
            name: z.string().describe("The skill directory name (e.g. 'brainstorming', 'test-driven-development')"),
        },
        async ({ name }) => {
            const skill = skillMap.get(name);
            if (!skill) {
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: `Skill '${name}' not found. Use list_skills to see available skills.`,
                        },
                    ],
                    isError: true,
                };
            }
            return {
                content: [{ type: "text" as const, text: skill.content }],
            };
        }
    );

    server.tool(
        "get_skill_file",
        "Load a supporting file from a superpowers skill",
        {
            skill: z.string().describe("The skill directory name"),
            file: z.string().describe("The filename to load (e.g. 'testing-anti-patterns.md')"),
        },
        async ({ skill: skillName, file: fileName }) => {
            const skill = skillMap.get(skillName);
            if (!skill) {
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: `Skill '${skillName}' not found. Use list_skills to see available skills.`,
                        },
                    ],
                    isError: true,
                };
            }

            const fileEntry = skill.files.find((f) => f.name === fileName);
            if (!fileEntry) {
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: `File '${fileName}' not found in skill '${skillName}'. Available files: ${skill.files.map((f) => f.name).join(", ") || "none"}`,
                        },
                    ],
                    isError: true,
                };
            }

            if (!skillsDir) {
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: `Cannot read supporting files: skills directory not available (using bundled skills).`,
                        },
                    ],
                    isError: true,
                };
            }

            try {
                const filePath = join(skillsDir, fileEntry.relativePath);
                const content = await readFile(filePath, "utf-8");
                return {
                    content: [{ type: "text" as const, text: content }],
                };
            } catch {
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: `Error reading file '${fileName}' from skill '${skillName}'.`,
                        },
                    ],
                    isError: true,
                };
            }
        }
    );

    if (!bridgeConfig.enabled) {
        return;
    }

    server.tool(
        "search_awesome_skills",
        "Search Awesome Skills Context Engine and return context-aware skill recommendations.",
        {
            query: z.string().min(1).describe("Natural language query (task, goal, or problem statement)."),
            limit: z.number().int().min(1).max(50).optional().describe("Max results (default: 8)."),
            strategy: z
                .enum(["auto", "classic", "context"])
                .optional()
                .describe("Search strategy for awesome_skills (default: auto)."),
            db_path: z.string().optional().describe("Optional path to awesome_skills SQLite DB."),
            context_alias_json: z
                .string()
                .optional()
                .describe("Optional phrase alias JSON for context routing boosts."),
        },
        async ({ query, limit, strategy, db_path: dbPath, context_alias_json: contextAliasJson }) => {
            const safeLimit = Math.max(1, Math.min(50, limit ?? 8));
            const safeStrategy: AwesomeSkillsStrategy = strategy ?? "auto";

            try {
                const result = await runAwesomeSkillsSearch(bridgeConfig, {
                    query,
                    limit: safeLimit,
                    strategy: safeStrategy,
                    dbPath,
                    contextAliasJson,
                });
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: JSON.stringify(
                                {
                                    bridge: {
                                        command: result.command,
                                        timeout_ms: bridgeConfig.timeoutMs,
                                        strategy_used: result.strategyUsed,
                                        attempts: result.attempts,
                                        cache_hit: result.cacheHit,
                                        coalesced: result.coalesced,
                                    },
                                    result: result.payload,
                                },
                                null,
                                2
                            ),
                        },
                    ],
                };
            } catch (error) {
                const message = error instanceof Error ? error.message : "Unknown bridge error.";
                const code =
                    error instanceof AwesomeSkillsBridgeError ? error.code : "BRIDGE_UNKNOWN";
                const details =
                    error instanceof AwesomeSkillsBridgeError ? error.details : undefined;
                return {
                    content: [
                        {
                            type: "text" as const,
                            text: JSON.stringify(
                                {
                                    error: {
                                        code,
                                        message,
                                        hints: [
                                            "Set AWESOME_SKILLS_ENABLE_BRIDGE=1 and ensure awesome_skills is installed.",
                                            "Optional: set AWESOME_SKILLS_BRIDGE_COMMAND_JSON to override the command.",
                                        ],
                                    },
                                    bridge: {
                                        timeout_ms: bridgeConfig.timeoutMs,
                                        ...(details ? { details } : {}),
                                    },
                                },
                                null,
                                2
                            ),
                        },
                    ],
                    isError: true,
                };
            }
        }
    );
}

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import type { Skill } from "../skills/types.js";

export function registerTools(
    server: McpServer,
    skills: Skill[],
    skillsDir?: string
): void {
    const skillMap = new Map<string, Skill>();
    for (const skill of skills) {
        skillMap.set(skill.directoryName, skill);
    }

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
}

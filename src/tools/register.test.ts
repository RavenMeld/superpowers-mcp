import { describe, it, expect, beforeAll } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { registerTools } from "./register.js";
import type { Skill } from "../skills/types.js";

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

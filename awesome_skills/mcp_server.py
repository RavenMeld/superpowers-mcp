from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
from typing import Any

from .context import parse_query_context
from .db import context_search_db, search_db
from .invent import load_skills_json, propose_novel_skills, write_skill_stubs

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool, ToolAnnotations
except ImportError as e:  # pragma: no cover - runtime dependency guard
    raise SystemExit(
        "The MCP SDK is required to run Awesome Skills Context Engine MCP server "
        "(package `awesome_skills`). "
        "Install with: pip install mcp"
    ) from e


WRITE_CONFIRM_TOKEN = "ALLOW_WRITE"


def _jtext(obj: Any) -> list[TextContent]:
    return [TextContent(type="text", text=json.dumps(obj, ensure_ascii=False, indent=2))]


def _as_path(path: str | None, default: Path) -> Path:
    if not path:
        return default
    return Path(path).expanduser().resolve()


def _as_int(v: Any, default: int, *, min_value: int = 1, max_value: int = 1000) -> int:
    if v is None:
        return default
    if isinstance(v, bool):
        return default
    if isinstance(v, (int, float)):
        i = int(v)
    else:
        i = int(str(v))
    if i < min_value:
        i = min_value
    if i > max_value:
        i = max_value
    return i


def _as_str_list(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        out: list[str] = []
        for x in v:
            if isinstance(x, str) and x.strip():
                out.append(x.strip())
        return out
    if isinstance(v, str) and v.strip():
        return [v.strip()]
    return []


def _as_bool(v: Any, default: bool = False) -> bool:
    if v is None:
        return bool(default)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return bool(v)
    if isinstance(v, str):
        s = v.strip().lower()
        if s in {"1", "true", "yes", "y", "on"}:
            return True
        if s in {"0", "false", "no", "n", "off"}:
            return False
    return bool(default)


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _default_write_roots() -> list[Path]:
    return [Path.cwd().resolve(), Path("/tmp").resolve()]


def _tool_error_payload(tool: str, error: Exception) -> dict[str, Any]:
    msg = str(error).strip() or error.__class__.__name__
    if isinstance(error, PermissionError):
        code = "POLICY_VIOLATION"
    elif isinstance(error, ValueError):
        code = "INVALID_ARGUMENT"
    elif isinstance(error, FileNotFoundError):
        code = "NOT_FOUND"
    else:
        code = "INTERNAL_ERROR"

    # Allow explicit "CODE: message" surface from policy gates.
    if ": " in msg:
        prefix, rest = msg.split(": ", 1)
        if prefix and prefix.replace("_", "").isalnum() and prefix.upper() == prefix:
            code = prefix
            msg = rest

    return {"error": {"code": code, "message": msg, "tool": tool}}


def get_tool_specs() -> list[dict[str, Any]]:
    return [
        {
            "name": "awesome_skills_invent",
            "description": (
                "Propose novel skill ideas by mining coverage gaps in skills.json "
                "(domain-action gaps and bridge gaps)."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "skills_json": {
                        "type": "string",
                        "description": "Optional path to skills.json (defaults to server startup path).",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max candidates to return (default: 20, max: 200).",
                    },
                    "exclude_domains": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of domain slugs to exclude (e.g. [\"hytale\"]).",
                    },
                },
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "skills_json": {"type": "string"},
                    "count": {"type": "integer"},
                    "exclude_domains": {"type": "array", "items": {"type": "string"}},
                    "candidates": {"type": "array", "items": {"type": "object"}},
                },
                "required": ["skills_json", "count", "exclude_domains", "candidates"],
            },
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
        },
        {
            "name": "awesome_skills_invent_write",
            "description": (
                "Generate and write SKILL.md stubs for novel candidates into an output directory. "
                "Disabled by default unless server is started with --allow-write-tools."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "skills_json": {
                        "type": "string",
                        "description": "Optional path to skills.json (defaults to server startup path).",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max candidates to generate (default: 20, max: 200).",
                    },
                    "exclude_domains": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of domain slugs to exclude.",
                    },
                    "out_dir": {
                        "type": "string",
                        "description": "Output directory for generated skill folders.",
                    },
                    "confirm": {
                        "type": "string",
                        "description": f"Required by default for writes. Must be '{WRITE_CONFIRM_TOKEN}'.",
                    },
                },
                "required": ["out_dir"],
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "skills_json": {"type": "string"},
                    "out_dir": {"type": "string"},
                    "requested": {"type": "integer"},
                    "written": {"type": "array", "items": {"type": "string"}},
                    "exclude_domains": {"type": "array", "items": {"type": "string"}},
                    "policy": {"type": "object"},
                },
                "required": ["skills_json", "out_dir", "requested", "written", "exclude_domains", "policy"],
            },
            "annotations": {
                "readOnlyHint": False,
                "destructiveHint": True,
                "idempotentHint": False,
                "openWorldHint": False,
            },
        },
        {
            "name": "awesome_skills_search",
            "description": (
                "Search indexed skills in awesome_skills.sqlite using FTS + worth/quality reranking "
                "with optional alias collapse."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query text."},
                    "limit": {"type": "integer", "description": "Max results (default: 10)."},
                    "db_path": {
                        "type": "string",
                        "description": "Optional DB path (defaults to server startup path).",
                    },
                    "alias_json": {
                        "type": "string",
                        "description": "Optional alias manifest path used for canonical dedupe.",
                    },
                    "collapse_aliases": {
                        "type": "boolean",
                        "description": "Whether to collapse duplicate aliases to canonical IDs (default: true).",
                    },
                    "strategy": {
                        "type": "string",
                        "description": (
                            "Search strategy: classic|context|auto (default: auto). "
                            "auto uses context-search when the query has strong phase/tool/alias signals."
                        ),
                    },
                },
                "required": ["query"],
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "db_path": {"type": "string"},
                    "alias_json": {"type": ["string", "null"]},
                    "collapse_aliases": {"type": "boolean"},
                    "mode_used": {"type": "string"},
                    "query": {"type": "string"},
                    "context": {"type": ["object", "null"]},
                    "count": {"type": "integer"},
                    "results": {"type": "array", "items": {"type": "object"}},
                    "alternatives": {"type": "array", "items": {"type": "object"}},
                },
                "required": [
                    "db_path",
                    "alias_json",
                    "collapse_aliases",
                    "mode_used",
                    "query",
                    "context",
                    "count",
                    "results",
                    "alternatives",
                ],
            },
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
        },
        {
            "name": "awesome_skills_context_search",
            "description": (
                "Context-aware skill search with query phase/tool detection, compatibility alias boosts, "
                "and source-priority reranking."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query text."},
                    "limit": {"type": "integer", "description": "Max results (default: 10)."},
                    "db_path": {
                        "type": "string",
                        "description": "Optional DB path (defaults to server startup path).",
                    },
                    "alias_json": {
                        "type": "string",
                        "description": (
                            "Optional phrase-alias path for context boosts "
                            "(defaults to sources/compat_aliases.json when present)."
                        ),
                    },
                },
                "required": ["query"],
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "db_path": {"type": "string"},
                    "alias_json": {"type": ["string", "null"]},
                    "query": {"type": "string"},
                    "context": {"type": "object"},
                    "count": {"type": "integer"},
                    "results": {"type": "array", "items": {"type": "object"}},
                    "alternatives": {"type": "array", "items": {"type": "object"}},
                },
                "required": ["db_path", "alias_json", "query", "context", "count", "results", "alternatives"],
            },
            "annotations": {
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
        },
    ]


class AwesomeSkillsMCPServer:
    def __init__(
        self,
        *,
        skills_json: Path,
        db_path: Path,
        allow_write_tools: bool = False,
        allowed_write_roots: list[Path] | None = None,
        require_write_confirm: bool = True,
    ):
        self.skills_json = skills_json
        self.db_path = db_path
        self.allow_write_tools = bool(allow_write_tools)
        roots = allowed_write_roots if allowed_write_roots is not None else _default_write_roots()
        self.allowed_write_roots = self._normalize_write_roots(roots)
        self.require_write_confirm = bool(require_write_confirm)
        self.server = Server("awesome-skills-context-engine")
        self._setup_handlers()

    @staticmethod
    def _normalize_write_roots(roots: list[Path]) -> list[Path]:
        out: list[Path] = []
        seen: set[str] = set()
        for r in roots:
            rp = Path(r).expanduser().resolve()
            key = str(rp)
            if key in seen:
                continue
            seen.add(key)
            out.append(rp)
        return out

    def _setup_handlers(self) -> None:
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            tools: list[Tool] = []
            for spec in get_tool_specs():
                tools.append(
                    Tool(
                        name=str(spec["name"]),
                        description=str(spec["description"]),
                        inputSchema=dict(spec["input_schema"]),
                        outputSchema=dict(spec["output_schema"]),
                        annotations=ToolAnnotations(**dict(spec["annotations"])),
                    )
                )
            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any] | None = None) -> list[TextContent]:
            args = arguments or {}
            try:
                if name == "awesome_skills_invent":
                    return _jtext(self._tool_invent(args))
                if name == "awesome_skills_invent_write":
                    return _jtext(self._tool_invent_write(args))
                if name == "awesome_skills_search":
                    return _jtext(self._tool_search(args))
                if name == "awesome_skills_context_search":
                    return _jtext(self._tool_context_search(args))
                return _jtext({"error": {"code": "TOOL_NOT_FOUND", "message": f"unknown tool: {name}", "tool": name}})
            except Exception as e:  # noqa: BLE001 - tool errors should return structured output.
                return _jtext(_tool_error_payload(name, e))

    def _enforce_write_policy(self, *, out_dir: Path, confirm: str | None) -> None:
        if not self.allow_write_tools:
            raise PermissionError(
                "POLICY_WRITE_DISABLED: write tools are disabled; start server with --allow-write-tools"
            )
        if self.require_write_confirm and confirm != WRITE_CONFIRM_TOKEN:
            raise PermissionError(
                f"POLICY_CONFIRM_REQUIRED: pass confirm='{WRITE_CONFIRM_TOKEN}' to authorize write operations"
            )
        if not any(_is_relative_to(out_dir, root) for root in self.allowed_write_roots):
            roots_text = ", ".join(str(x) for x in self.allowed_write_roots)
            raise PermissionError(
                f"POLICY_WRITE_ROOT_DENIED: out_dir={out_dir} is outside allowed roots: {roots_text}"
            )

    def _tool_invent(self, args: dict[str, Any]) -> dict[str, Any]:
        skills_json = _as_path(args.get("skills_json"), self.skills_json)
        if not skills_json.exists():
            raise FileNotFoundError(f"skills_json not found: {skills_json}")
        limit = _as_int(args.get("limit"), default=20, min_value=1, max_value=200)
        exclude_domains = _as_str_list(args.get("exclude_domains"))

        skills = load_skills_json(skills_json)
        cands = propose_novel_skills(skills=skills, limit=limit, exclude_domains=exclude_domains)
        return {
            "skills_json": str(skills_json),
            "count": len(cands),
            "exclude_domains": exclude_domains,
            "candidates": [c.to_json() for c in cands],
        }

    def _tool_invent_write(self, args: dict[str, Any]) -> dict[str, Any]:
        skills_json = _as_path(args.get("skills_json"), self.skills_json)
        limit = _as_int(args.get("limit"), default=20, min_value=1, max_value=200)
        exclude_domains = _as_str_list(args.get("exclude_domains"))

        out_dir_raw = args.get("out_dir")
        if not isinstance(out_dir_raw, str) or not out_dir_raw.strip():
            raise ValueError("out_dir is required and must be a non-empty string")
        out_dir = Path(out_dir_raw).expanduser().resolve()
        confirm = args.get("confirm")
        if confirm is not None and not isinstance(confirm, str):
            raise ValueError("confirm must be a string when provided")
        self._enforce_write_policy(out_dir=out_dir, confirm=confirm)

        if not skills_json.exists():
            raise FileNotFoundError(f"skills_json not found: {skills_json}")

        skills = load_skills_json(skills_json)
        cands = propose_novel_skills(skills=skills, limit=limit, exclude_domains=exclude_domains)
        written = write_skill_stubs(cands, out_dir=out_dir)
        return {
            "skills_json": str(skills_json),
            "out_dir": str(out_dir),
            "requested": len(cands),
            "written": [str(p) for p in written],
            "exclude_domains": exclude_domains,
            "policy": {
                "allow_write_tools": self.allow_write_tools,
                "require_write_confirm": self.require_write_confirm,
                "allowed_write_roots": [str(p) for p in self.allowed_write_roots],
            },
        }

    def _tool_search(self, args: dict[str, Any]) -> dict[str, Any]:
        query = args.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query is required and must be a non-empty string")
        limit = _as_int(args.get("limit"), default=10, min_value=1, max_value=100)
        db_path = _as_path(args.get("db_path"), self.db_path)
        if not db_path.exists():
            raise FileNotFoundError(f"db_path not found: {db_path}")
        collapse_aliases = _as_bool(args.get("collapse_aliases"), default=True)
        strategy_raw = args.get("strategy")
        strategy = "auto"
        if strategy_raw is not None:
            if not isinstance(strategy_raw, str):
                raise ValueError("strategy must be a string when provided")
            strategy = strategy_raw.strip().lower() or "auto"
        if strategy not in {"auto", "classic", "context"}:
            raise ValueError("strategy must be one of: auto, classic, context")

        alias_json: Path | None = None
        if collapse_aliases:
            alias_raw = args.get("alias_json")
            if alias_raw is not None:
                if not isinstance(alias_raw, str):
                    raise ValueError("alias_json must be a string when provided")
                if alias_raw.strip():
                    alias_json = Path(alias_raw).expanduser().resolve()
            else:
                candidate = db_path.parent / "name_aliases.json"
                if candidate.exists():
                    alias_json = candidate

        context_alias_json: Path | None = None
        if alias_json is not None:
            context_alias_json = alias_json
        else:
            candidates = [
                (Path.cwd() / "sources" / "compat_aliases.json").resolve(),
                (db_path.parent / "compat_aliases.json").resolve(),
            ]
            for candidate in candidates:
                if candidate.exists():
                    context_alias_json = candidate
                    break

        query_stripped = query.strip()
        use_context = False
        query_context: dict[str, Any] | None = None
        if strategy == "context":
            use_context = True
        elif strategy == "classic":
            use_context = False
        else:
            qc = parse_query_context(query_stripped, alias_json=context_alias_json)
            query_context = qc.to_json()
            use_context = bool(qc.phase or qc.tools or qc.alias_hits)

        if use_context:
            context, results, alternatives = context_search_db(
                db_path=db_path,
                query=query_stripped,
                limit=limit,
                alias_json=context_alias_json,
            )
            return {
                "db_path": str(db_path),
                "alias_json": str(context_alias_json) if context_alias_json else None,
                "collapse_aliases": bool(collapse_aliases),
                "mode_used": "context",
                "query": query_stripped,
                "context": context,
                "count": len(results),
                "results": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "description": r.description,
                        "worth_score": r.worth_score,
                        "quality_score": r.quality_score,
                        "combined_score": r.score,
                        "match_terms": r.match_terms,
                        "confidence": r.confidence,
                        "why_selected": r.why_selected,
                        "source_kind": r.source_kind,
                        "kind": r.kind,
                        "phases": r.phases,
                        "tools": r.tools,
                        "score_breakdown": r.score_breakdown,
                    }
                    for r in results
                ],
                "alternatives": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "combined_score": r.score,
                        "why_selected": r.why_selected,
                    }
                    for r in alternatives
                ],
            }

        results = search_db(
            db_path=db_path,
            query=query_stripped,
            limit=limit,
            alias_json=alias_json,
            collapse_aliases=collapse_aliases,
        )
        return {
            "db_path": str(db_path),
            "alias_json": str(alias_json) if alias_json else None,
            "collapse_aliases": bool(collapse_aliases),
            "mode_used": "classic",
            "query": query_stripped,
            "context": query_context,
            "count": len(results),
            "results": [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "worth_score": r.worth_score,
                    "quality_score": r.quality_score,
                    "combined_score": r.combined_score,
                    "match_terms": r.match_terms,
                }
                for r in results
            ],
            "alternatives": [],
        }

    def _tool_context_search(self, args: dict[str, Any]) -> dict[str, Any]:
        query = args.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query is required and must be a non-empty string")
        limit = _as_int(args.get("limit"), default=10, min_value=1, max_value=100)
        db_path = _as_path(args.get("db_path"), self.db_path)
        if not db_path.exists():
            raise FileNotFoundError(f"db_path not found: {db_path}")

        alias_json: Path | None = None
        alias_raw = args.get("alias_json")
        if alias_raw is not None:
            if not isinstance(alias_raw, str):
                raise ValueError("alias_json must be a string when provided")
            if alias_raw.strip():
                alias_json = Path(alias_raw).expanduser().resolve()
        else:
            candidates = [
                (Path.cwd() / "sources" / "compat_aliases.json").resolve(),
                (db_path.parent / "compat_aliases.json").resolve(),
            ]
            for candidate in candidates:
                if candidate.exists():
                    alias_json = candidate
                    break

        context, results, alternatives = context_search_db(
            db_path=db_path,
            query=query.strip(),
            limit=limit,
            alias_json=alias_json,
        )

        return {
            "db_path": str(db_path),
            "alias_json": str(alias_json) if alias_json else None,
            "query": query.strip(),
            "context": context,
            "count": len(results),
            "results": [
                {
                    "id": r.id,
                    "name": r.name,
                    "description": r.description,
                    "worth_score": r.worth_score,
                    "quality_score": r.quality_score,
                    "score": r.score,
                    "confidence": r.confidence,
                    "why_selected": r.why_selected,
                    "source_kind": r.source_kind,
                    "kind": r.kind,
                    "phases": r.phases,
                    "tools": r.tools,
                    "match_terms": r.match_terms,
                    "score_breakdown": r.score_breakdown,
                }
                for r in results
            ],
            "alternatives": [
                {
                    "id": r.id,
                    "name": r.name,
                    "score": r.score,
                    "why_selected": r.why_selected,
                }
                for r in alternatives
            ],
        }

    async def run_stdio(self) -> None:
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


def run_stdio_server(
    *,
    skills_json: Path,
    db_path: Path,
    allow_write_tools: bool = False,
    allowed_write_roots: list[Path] | None = None,
    require_write_confirm: bool = True,
) -> int:
    server = AwesomeSkillsMCPServer(
        skills_json=skills_json,
        db_path=db_path,
        allow_write_tools=allow_write_tools,
        allowed_write_roots=allowed_write_roots,
        require_write_confirm=require_write_confirm,
    )
    asyncio.run(server.run_stdio())
    return 0


def _run_self_test(*, skills_json: Path, db_path: Path) -> int:
    read_only_server = AwesomeSkillsMCPServer(skills_json=skills_json, db_path=db_path)
    inv = read_only_server._tool_invent({"limit": 5, "exclude_domains": ["hytale"]})
    if int(inv.get("count", 0)) <= 0:
        raise SystemExit("self_test failed: invent produced no candidates")
    try:
        read_only_server._tool_invent_write(
            {
                "limit": 1,
                "exclude_domains": ["hytale"],
                "out_dir": str(skills_json.parent / "mcp_selftest_out"),
                "confirm": WRITE_CONFIRM_TOKEN,
            }
        )
        raise SystemExit("self_test failed: write policy should block writes when allow_write_tools=False")
    except PermissionError:
        pass

    write_root = (skills_json.parent / "mcp_selftest_out").resolve()
    write_server = AwesomeSkillsMCPServer(
        skills_json=skills_json,
        db_path=db_path,
        allow_write_tools=True,
        allowed_write_roots=[write_root.parent],
        require_write_confirm=True,
    )
    try:
        write_server._tool_invent_write(
            {
                "limit": 1,
                "exclude_domains": ["hytale"],
                "out_dir": str(write_root),
            }
        )
        raise SystemExit("self_test failed: write policy should require confirm token")
    except PermissionError:
        pass

    wr = write_server._tool_invent_write(
        {
            "limit": 2,
            "exclude_domains": ["hytale"],
            "out_dir": str(write_root),
            "confirm": WRITE_CONFIRM_TOKEN,
        }
    )
    if len(wr.get("written", [])) <= 0:
        raise SystemExit("self_test failed: invent_write produced no files")
    try:
        write_server._enforce_write_policy(out_dir=Path("/tmp/awesome-skills-selftest-denied"), confirm=WRITE_CONFIRM_TOKEN)
        raise SystemExit("self_test failed: write root policy did not reject /tmp path")
    except PermissionError:
        pass

    sr = write_server._tool_search(
        {
            "query": "playwright",
            "limit": 3,
            "db_path": str(db_path),
            "collapse_aliases": True,
            "strategy": "classic",
        }
    )
    results = sr.get("results", [])
    if len(results) <= 0:
        raise SystemExit("self_test failed: search produced no results")
    if "quality_score" not in results[0]:
        raise SystemExit("self_test failed: search result missing quality_score")
    auto_sr = write_server._tool_search(
        {
            "query": "debug flaky playwright test",
            "limit": 3,
            "db_path": str(db_path),
            "strategy": "auto",
        }
    )
    if auto_sr.get("mode_used") != "context":
        raise SystemExit("self_test failed: auto search did not route to context mode")
    csr = write_server._tool_context_search(
        {
            "query": "debug flaky playwright test",
            "limit": 3,
            "db_path": str(db_path),
        }
    )
    cresults = csr.get("results", [])
    if len(cresults) <= 0:
        raise SystemExit("self_test failed: context_search produced no results")
    if "context" not in csr:
        raise SystemExit("self_test failed: context_search missing context payload")
    if "score" not in cresults[0]:
        raise SystemExit("self_test failed: context_search result missing score")
    print("self_test ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="awesome_skills.mcp_server")
    parser.add_argument(
        "--skills-json",
        default="dist/skills.json",
        help="Path to skills.json (default: dist/skills.json).",
    )
    parser.add_argument(
        "--db",
        default="dist/awesome_skills.sqlite",
        help="Path to SQLite DB (default: dist/awesome_skills.sqlite).",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run internal server logic tests and exit (no stdio server).",
    )
    parser.add_argument(
        "--allow-write-tools",
        action="store_true",
        help="Enable write-capable tools (disabled by default for safety).",
    )
    parser.add_argument(
        "--write-root",
        action="append",
        default=[],
        help="Allowed write root for write tools (repeatable). Defaults to CWD and /tmp.",
    )
    parser.add_argument(
        "--disable-write-confirm-token",
        action="store_true",
        help=f"Disable confirm token requirement for writes (token is '{WRITE_CONFIRM_TOKEN}' by default).",
    )
    args = parser.parse_args(argv)

    skills_json = Path(args.skills_json).expanduser().resolve()
    db_path = Path(args.db).expanduser().resolve()

    if args.self_test:
        return _run_self_test(skills_json=skills_json, db_path=db_path)

    write_roots = [Path(p).expanduser().resolve() for p in args.write_root] if args.write_root else None
    return run_stdio_server(
        skills_json=skills_json,
        db_path=db_path,
        allow_write_tools=bool(args.allow_write_tools),
        allowed_write_roots=write_roots,
        require_write_confirm=not bool(args.disable_write_confirm_token),
    )


if __name__ == "__main__":
    raise SystemExit(main())

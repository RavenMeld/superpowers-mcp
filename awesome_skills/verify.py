from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .util import slugify


_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*--[0-9a-f]{10}$")
_EXPECTED_TOOLS = (
    "awesome_skills_invent",
    "awesome_skills_invent_write",
    "awesome_skills_search",
    "awesome_skills_context_search",
)


@dataclass(frozen=True)
class VerifyFinding:
    code: str
    severity: str  # error|warning
    message: str
    path: str | None = None
    skill_id: str | None = None

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


class _Collector:
    def __init__(self, max_findings: int = 500):
        self.max_findings = max(1, int(max_findings))
        self.findings: list[VerifyFinding] = []
        self.error_count = 0
        self.warning_count = 0
        self.truncated = False

    def add(
        self,
        *,
        code: str,
        severity: str,
        message: str,
        path: Path | None = None,
        skill_id: str | None = None,
    ) -> None:
        sev = severity.lower().strip()
        if sev not in ("error", "warning"):
            raise ValueError(f"invalid finding severity: {severity!r}")
        if sev == "error":
            self.error_count += 1
        else:
            self.warning_count += 1

        if len(self.findings) >= self.max_findings:
            self.truncated = True
            return
        self.findings.append(
            VerifyFinding(
                code=code,
                severity=sev,
                message=message,
                path=str(path) if path else None,
                skill_id=skill_id,
            )
        )


def _read_json(path: Path, col: _Collector) -> dict[str, Any] | None:
    if not path.exists():
        col.add(code="MISSING_FILE", severity="error", message=f"missing file: {path}", path=path)
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:  # noqa: BLE001 - caller receives structured error.
        col.add(code="INVALID_JSON", severity="error", message=f"invalid json: {e}", path=path)
        return None
    if not isinstance(data, dict):
        col.add(code="INVALID_ROOT", severity="error", message="skills.json root must be an object", path=path)
        return None
    return data


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and value.strip():
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


def _load_alias_manifest(path: Path | None, col: _Collector) -> tuple[dict[str, set[str]], str | None]:
    if path is None:
        return {}, None
    if not path.exists():
        return {}, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception as e:  # noqa: BLE001
        col.add(code="ALIASES_JSON_INVALID", severity="warning", message=f"invalid alias json: {e}", path=path)
        return {}, "invalid"

    if not isinstance(data, dict):
        col.add(code="ALIASES_JSON_INVALID", severity="warning", message="alias json root must be object", path=path)
        return {}, "invalid"
    aliases = data.get("aliases")
    if not isinstance(aliases, list):
        col.add(code="ALIASES_JSON_INVALID", severity="warning", message="alias json missing aliases[]", path=path)
        return {}, "invalid"

    out: dict[str, set[str]] = {}
    for row in aliases:
        if not isinstance(row, dict):
            continue
        key = slugify(str(row.get("name_key") or ""))
        members = row.get("member_ids") or []
        if not key or not isinstance(members, list):
            continue
        ids = {str(x).strip() for x in members if str(x).strip()}
        if not ids:
            continue
        out[key] = ids
    return out, "ok"


def _check_duplicate_name_keys(
    *,
    name_key_members: dict[str, list[str]],
    alias_members_by_key: dict[str, set[str]],
    col: _Collector,
) -> None:
    for key in sorted(name_key_members.keys()):
        member_ids = sorted({x for x in name_key_members.get(key, []) if x})
        if len(member_ids) <= 1:
            continue

        aliased = alias_members_by_key.get(key)
        if aliased and set(member_ids) == aliased:
            # Duplicate cluster explicitly canonicalized in aliases manifest.
            continue

        col.add(
            code="SKILL_NAME_NEAR_DUPLICATE",
            severity="warning",
            message=f"multiple skills normalize to same name key '{key}' ({len(member_ids)} members)",
            skill_id=member_ids[0],
        )


def _validate_skill_record(
    *,
    idx: int,
    skill: dict[str, Any],
    cards_dir: Path | None,
    col: _Collector,
    seen_ids: set[str],
    seen_sources: dict[str, str],
    name_key_members: dict[str, list[str]],
) -> None:
    sid = str(skill.get("id") or "").strip()
    if not sid:
        col.add(code="SKILL_ID_MISSING", severity="error", message=f"skills[{idx}] missing id")
    else:
        if not _ID_RE.match(sid):
            col.add(
                code="SKILL_ID_FORMAT",
                severity="error",
                message=f"skills[{idx}] id has unexpected format: {sid!r}",
                skill_id=sid,
            )
        if sid in seen_ids:
            col.add(code="SKILL_ID_DUPLICATE", severity="error", message=f"duplicate id: {sid}", skill_id=sid)
        seen_ids.add(sid)

    for field in ("name", "description", "root_label", "source_path"):
        val = skill.get(field)
        if not isinstance(val, str) or not val.strip():
            col.add(
                code="SKILL_FIELD_INVALID",
                severity="error",
                message=f"skills[{idx}] field '{field}' must be a non-empty string",
                skill_id=sid or None,
            )

    name = str(skill.get("name") or "").strip()
    if name:
        nkey = slugify(name)
        if sid:
            name_key_members.setdefault(nkey, []).append(sid)

    source_path = str(skill.get("source_path") or "").strip()
    if source_path:
        prev = seen_sources.get(source_path)
        if prev and prev != sid:
            col.add(
                code="SKILL_SOURCE_DUPLICATE",
                severity="warning",
                message=f"source_path appears multiple times: {source_path}",
                skill_id=sid or None,
            )
        seen_sources[source_path] = sid or source_path

    worth = _as_int(skill.get("worth_score"))
    if worth is None or worth < 0 or worth > 100:
        col.add(
            code="SKILL_WORTH_RANGE",
            severity="error",
            message=f"skills[{idx}] worth_score must be an integer in [0, 100]",
            skill_id=sid or None,
        )
    quality = _as_int(skill.get("quality_score"))
    if quality is None or quality < 0 or quality > 100:
        col.add(
            code="SKILL_QUALITY_RANGE",
            severity="error",
            message=f"skills[{idx}] quality_score must be an integer in [0, 100]",
            skill_id=sid or None,
        )

    tags = skill.get("tags")
    if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
        col.add(
            code="SKILL_TAGS_TYPE",
            severity="error",
            message=f"skills[{idx}] tags must be a string[]",
            skill_id=sid or None,
        )

    use_when = skill.get("use_when")
    workflow = skill.get("workflow")
    if not isinstance(use_when, list) or any(not isinstance(t, str) for t in use_when):
        col.add(
            code="SKILL_USE_WHEN_TYPE",
            severity="error",
            message=f"skills[{idx}] use_when must be a string[]",
            skill_id=sid or None,
        )
    if not isinstance(workflow, list) or any(not isinstance(t, str) for t in workflow):
        col.add(
            code="SKILL_WORKFLOW_TYPE",
            severity="error",
            message=f"skills[{idx}] workflow must be a string[]",
            skill_id=sid or None,
        )

    features = skill.get("features")
    if not isinstance(features, dict):
        col.add(
            code="SKILL_FEATURES_TYPE",
            severity="error",
            message=f"skills[{idx}] features must be an object",
            skill_id=sid or None,
        )
    else:
        bool_keys = ("has_description", "has_use_when", "has_workflow", "has_scripts", "has_references", "has_assets")
        int_keys = ("code_fence_count", "word_count")
        for k in bool_keys:
            if k not in features or not isinstance(features.get(k), bool):
                col.add(
                    code="SKILL_FEATURE_BOOL",
                    severity="error",
                    message=f"skills[{idx}] features.{k} must be boolean",
                    skill_id=sid or None,
                )
        for k in int_keys:
            v = _as_int(features.get(k))
            if v is None or v < 0:
                col.add(
                    code="SKILL_FEATURE_INT",
                    severity="error",
                    message=f"skills[{idx}] features.{k} must be a non-negative integer",
                    skill_id=sid or None,
                )
        wc = _as_int(features.get("word_count")) or 0
        if wc <= 0:
            col.add(
                code="SKILL_LOW_SIGNAL_WORD_COUNT",
                severity="warning",
                message=f"skills[{idx}] has non-positive word_count",
                skill_id=sid or None,
            )

    tagset = {t.strip().lower() for t in tags} if isinstance(tags, list) else set()
    if "mcp" in tagset:
        if isinstance(use_when, list) and len(use_when) == 0:
            col.add(
                code="MCP_SKILL_USE_WHEN_EMPTY",
                severity="warning",
                message="mcp-tagged skill has empty use_when",
                skill_id=sid or None,
            )
        if isinstance(workflow, list) and len(workflow) == 0:
            col.add(
                code="MCP_SKILL_WORKFLOW_EMPTY",
                severity="warning",
                message="mcp-tagged skill has empty workflow",
                skill_id=sid or None,
            )

    if cards_dir and sid:
        card = cards_dir / f"{sid}.md"
        if not card.exists():
            col.add(
                code="CARD_MISSING",
                severity="error",
                message=f"missing condensed card for skill id: {sid}",
                path=card,
                skill_id=sid,
            )
        else:
            text = card.read_text(encoding="utf-8", errors="replace")
            if f"id: `{sid}`" not in text:
                col.add(
                    code="CARD_ID_MISSING",
                    severity="warning",
                    message=f"card missing id marker for {sid}",
                    path=card,
                    skill_id=sid,
                )
            if "worth_using_score:" not in text:
                col.add(
                    code="CARD_SCORE_MISSING",
                    severity="warning",
                    message=f"card missing worth_using_score marker for {sid}",
                    path=card,
                    skill_id=sid,
                )
            if "quality_score:" not in text:
                col.add(
                    code="CARD_QUALITY_MISSING",
                    severity="warning",
                    message=f"card missing quality_score marker for {sid}",
                    path=card,
                    skill_id=sid,
                )


def _verify_readme_examples(readme_path: Path, col: _Collector) -> None:
    if not readme_path.exists():
        col.add(code="README_MISSING", severity="error", message=f"missing README path: {readme_path}", path=readme_path)
        return
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    for tool_name in _EXPECTED_TOOLS:
        pat = re.compile(
            rf"Tool:\s*`{re.escape(tool_name)}`(?P<body>.*?)(?=\nTool:\s*`|\Z)",
            re.IGNORECASE | re.DOTALL,
        )
        m = pat.search(text)
        if not m:
            col.add(
                code="README_TOOL_SECTION_MISSING",
                severity="error",
                message=f"README missing section for tool `{tool_name}`",
                path=readme_path,
            )
            continue
        body = m.group("body")
        if "Input:" not in body:
            col.add(
                code="README_TOOL_INPUT_MISSING",
                severity="warning",
                message=f"README tool section `{tool_name}` missing explicit Input line",
                path=readme_path,
            )
        json_examples = len(re.findall(r"```json\s*.*?```", body, flags=re.DOTALL | re.IGNORECASE))
        if json_examples < 3:
            col.add(
                code="README_TOOL_EXAMPLES_LOW",
                severity="error",
                message=f"README tool section `{tool_name}` has {json_examples} json examples; expected >= 3",
                path=readme_path,
            )


def _verify_mcp_policy(skills_json: Path, mcp_server_path: Path, col: _Collector) -> None:
    if not mcp_server_path.exists():
        col.add(
            code="MCP_SERVER_MISSING",
            severity="error",
            message=f"missing mcp server path: {mcp_server_path}",
            path=mcp_server_path,
        )
        return

    try:
        from . import mcp_server as mcp_mod  # Local import keeps this optional for non-MCP workflows.
    except Exception as e:  # noqa: BLE001 - verify should surface import issues as structured findings.
        col.add(
            code="MCP_POLICY_IMPORT_FAILED",
            severity="error",
            message=f"failed to import mcp_server for policy checks: {e}",
            path=mcp_server_path,
        )
        return

    module_path = Path(getattr(mcp_mod, "__file__", str(mcp_server_path))).resolve()
    if module_path != mcp_server_path.resolve():
        col.add(
            code="MCP_SERVER_PATH_MISMATCH",
            severity="warning",
            message=f"imported mcp server module from {module_path} (requested {mcp_server_path.resolve()})",
            path=mcp_server_path,
        )

    WRITE_CONFIRM_TOKEN = mcp_mod.WRITE_CONFIRM_TOKEN
    AwesomeSkillsMCPServer = mcp_mod.AwesomeSkillsMCPServer
    get_tool_specs = mcp_mod.get_tool_specs

    specs = get_tool_specs()
    spec_by_name = {str(s.get("name")): s for s in specs if isinstance(s, dict)}
    for expected in _EXPECTED_TOOLS:
        if expected not in spec_by_name:
            col.add(
                code="MCP_TOOL_MISSING",
                severity="error",
                message=f"mcp server missing expected tool `{expected}`",
                path=mcp_server_path,
            )

    def _check_schema_contains(tool: str, schema_key: str, prop: str) -> None:
        spec = spec_by_name.get(tool)
        if not spec:
            return
        schema = spec.get(schema_key)
        if not isinstance(schema, dict):
            col.add(
                code="MCP_TOOL_SCHEMA_MISSING",
                severity="error",
                message=f"tool `{tool}` missing `{schema_key}`",
                path=mcp_server_path,
            )
            return
        props = schema.get("properties")
        if not isinstance(props, dict) or prop not in props:
            col.add(
                code="MCP_TOOL_SCHEMA_PROP_MISSING",
                severity="error",
                message=f"tool `{tool}` missing `{prop}` in `{schema_key}.properties`",
                path=mcp_server_path,
            )

    def _check_ann(name: str, *, read_only: bool, destructive: bool) -> None:
        spec = spec_by_name.get(name)
        if not spec:
            return
        ann = spec.get("annotations")
        if not isinstance(ann, dict):
            col.add(
                code="MCP_TOOL_ANNOTATIONS_MISSING",
                severity="error",
                message=f"tool `{name}` missing annotations",
                path=mcp_server_path,
            )
            return
        if ann.get("readOnlyHint") is not read_only:
            col.add(
                code="MCP_TOOL_ANNOTATIONS_READONLY",
                severity="error",
                message=f"tool `{name}` readOnlyHint should be {read_only}",
                path=mcp_server_path,
            )
        if ann.get("destructiveHint") is not destructive:
            col.add(
                code="MCP_TOOL_ANNOTATIONS_DESTRUCTIVE",
                severity="error",
                message=f"tool `{name}` destructiveHint should be {destructive}",
                path=mcp_server_path,
            )

    _check_ann("awesome_skills_invent", read_only=True, destructive=False)
    _check_ann("awesome_skills_search", read_only=True, destructive=False)
    _check_ann("awesome_skills_context_search", read_only=True, destructive=False)
    _check_ann("awesome_skills_invent_write", read_only=False, destructive=True)

    _check_schema_contains("awesome_skills_search", "input_schema", "strategy")
    _check_schema_contains("awesome_skills_search", "output_schema", "mode_used")
    _check_schema_contains("awesome_skills_search", "output_schema", "context")
    _check_schema_contains("awesome_skills_search", "output_schema", "alternatives")
    _check_schema_contains("awesome_skills_context_search", "input_schema", "query")
    _check_schema_contains("awesome_skills_context_search", "output_schema", "context")

    server_read_only = AwesomeSkillsMCPServer(skills_json=skills_json, db_path=Path("/tmp/does-not-matter.sqlite"))
    try:
        server_read_only._enforce_write_policy(  # noqa: SLF001 - verify intentionally asserts internal policy enforcement.
            out_dir=Path("/tmp/awesome-skills-verify"),
            confirm=WRITE_CONFIRM_TOKEN,
        )
        col.add(
            code="MCP_POLICY_WRITE_DISABLED",
            severity="error",
            message="write policy unexpectedly allowed writes when allow_write_tools=False",
            path=mcp_server_path,
        )
    except PermissionError:
        pass

    server_write = AwesomeSkillsMCPServer(
        skills_json=skills_json,
        db_path=Path("/tmp/does-not-matter.sqlite"),
        allow_write_tools=True,
        allowed_write_roots=[Path("/tmp/awesome-skills-verify-root")],
        require_write_confirm=True,
    )
    try:
        server_write._enforce_write_policy(  # noqa: SLF001
            out_dir=Path("/tmp/awesome-skills-verify-root/out"),
            confirm=None,
        )
        col.add(
            code="MCP_POLICY_CONFIRM_REQUIRED",
            severity="error",
            message="write policy unexpectedly allowed write without confirm token",
            path=mcp_server_path,
        )
    except PermissionError:
        pass

    try:
        server_write._enforce_write_policy(  # noqa: SLF001
            out_dir=Path("/tmp/outside-allowed-root"),
            confirm=WRITE_CONFIRM_TOKEN,
        )
        col.add(
            code="MCP_POLICY_WRITE_ROOTS",
            severity="error",
            message="write policy unexpectedly allowed path outside write roots",
            path=mcp_server_path,
        )
    except PermissionError:
        pass


def verify_artifacts(
    *,
    skills_json: Path,
    cards_dir: Path | None = None,
    alias_json: Path | None = None,
    readme_path: Path | None = None,
    mcp_server_path: Path | None = None,
    check_readme_examples: bool = True,
    check_mcp_policy: bool = True,
    max_findings: int = 500,
) -> dict[str, Any]:
    col = _Collector(max_findings=max_findings)
    data = _read_json(skills_json, col)
    total_skills = 0
    resolved_alias_json = alias_json.expanduser().resolve() if alias_json else (skills_json.parent / "name_aliases.json")
    alias_lookup_path = resolved_alias_json if (alias_json is not None or resolved_alias_json.exists()) else None
    alias_members_by_key, alias_status = _load_alias_manifest(alias_lookup_path, col)

    if data is not None:
        schema_version = _as_int(data.get("schema_version"))
        if schema_version is None:
            col.add(
                code="SCHEMA_VERSION_MISSING",
                severity="error",
                message="skills.json missing integer schema_version",
                path=skills_json,
            )
        elif schema_version not in (1, 2):
            col.add(
                code="SCHEMA_VERSION_UNEXPECTED",
                severity="warning",
                message=f"skills.json schema_version={schema_version}, expected 1 or 2",
                path=skills_json,
            )

        skills = data.get("skills")
        if not isinstance(skills, list):
            col.add(
                code="SKILLS_LIST_MISSING",
                severity="error",
                message="skills.json missing skills[] list",
                path=skills_json,
            )
            skills = []
        total_skills = len(skills)

        declared_count = _as_int(data.get("count"))
        if declared_count is None:
            col.add(
                code="COUNT_MISSING",
                severity="error",
                message="skills.json missing integer count",
                path=skills_json,
            )
        elif declared_count != total_skills:
            col.add(
                code="COUNT_MISMATCH",
                severity="error",
                message=f"skills.json count={declared_count} but len(skills)={total_skills}",
                path=skills_json,
            )

        seen_ids: set[str] = set()
        seen_sources: dict[str, str] = {}
        name_key_members: dict[str, list[str]] = {}
        for idx, item in enumerate(skills):
            if not isinstance(item, dict):
                col.add(
                    code="SKILL_RECORD_TYPE",
                    severity="error",
                    message=f"skills[{idx}] must be an object",
                    path=skills_json,
                )
                continue
            _validate_skill_record(
                idx=idx,
                skill=item,
                cards_dir=cards_dir,
                col=col,
                seen_ids=seen_ids,
                seen_sources=seen_sources,
                name_key_members=name_key_members,
            )
        _check_duplicate_name_keys(
            name_key_members=name_key_members,
            alias_members_by_key=alias_members_by_key,
            col=col,
        )

    if check_readme_examples and readme_path is not None:
        _verify_readme_examples(readme_path, col)

    if check_mcp_policy and mcp_server_path is not None:
        _verify_mcp_policy(skills_json, mcp_server_path, col)

    return {
        "ok": col.error_count == 0,
        "error_count": col.error_count,
        "warning_count": col.warning_count,
        "findings": [f.to_json() for f in col.findings],
        "findings_truncated": col.truncated,
        "checked": {
            "skills_json": str(skills_json),
            "cards_dir": str(cards_dir) if cards_dir else None,
            "alias_json": str(resolved_alias_json) if alias_lookup_path else None,
            "alias_status": alias_status,
            "readme_path": str(readme_path) if readme_path else None,
            "mcp_server_path": str(mcp_server_path) if mcp_server_path else None,
            "total_skills": total_skills,
            "check_readme_examples": bool(check_readme_examples),
            "check_mcp_policy": bool(check_mcp_policy),
            "max_findings": int(max_findings),
        },
    }

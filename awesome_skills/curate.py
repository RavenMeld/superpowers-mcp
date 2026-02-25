from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .util import slugify


_WORTH_LINE = re.compile(r"^- worth_using_score:\s*`?\d+/100`?\s*$", re.MULTILINE)
_QUALITY_LINE = re.compile(r"^- quality_score:\s*`?\d+/100`?\s*$", re.MULTILINE)
_ID_LINE = re.compile(r"^- id:\s*`([^`]+)`\s*$")
_HEADING_QF = re.compile(r"^## Quick Facts\s*$", re.MULTILINE)

_ROOT_PRIORITY = {
    "codex_skills": 0,
    "agent_playground": 1,
    "agents_skills": 2,
    "external": 9,
}


@dataclass(frozen=True)
class CurateReport:
    skills_total: int
    mcp_total: int
    mcp_use_when_filled: int
    mcp_workflow_filled: int
    general_use_when_filled: int
    general_workflow_filled: int
    tags_normalized: int
    cards_checked: int
    cards_patched_score: int
    duplicate_name_keys: int
    duplicate_skills_total: int
    alias_entries: int
    fix_level: str
    write: bool
    skills_json: str
    cards_dir: str
    aliases_json: str

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid json root (expected object): {path}")
    return data


def _default_mcp_use_when(name: str, description: str) -> list[str]:
    lead = description.strip().rstrip(".")
    if not lead:
        lead = f"Use this skill when working with MCP workflows related to {name}."
    else:
        lead = f"Use when this MCP capability is relevant: {lead}."
    return [
        lead,
        "Prefer deterministic tool calls, explicit input validation, and structured error handling.",
    ]


def _default_mcp_workflow(name: str) -> list[str]:
    return [
        f"Identify the MCP task scope and the exact operation needed for `{name}`.",
        "Validate required inputs and apply safety checks before executing tool actions.",
        "Run the tool flow, verify outputs, and record follow-up steps or gaps.",
    ]


def _default_general_use_when(name: str, description: str) -> list[str]:
    lead = description.strip().rstrip(".")
    if not lead:
        lead = f"Use when working with `{name}` workflows."
    else:
        lead = f"Use when this applies: {lead}."
    return [
        lead,
        "Prefer minimal changes with explicit validation and reproducible outputs.",
    ]


def _default_general_workflow(name: str) -> list[str]:
    return [
        f"Define the concrete goal for `{name}` and expected success checks.",
        "Execute the smallest reliable workflow that satisfies the goal.",
        "Verify results and document follow-up actions or residual risks.",
    ]


def _ensure_mcp_guidance(skills: list[dict[str, Any]]) -> tuple[int, int, int]:
    mcp_total = 0
    filled_use = 0
    filled_workflow = 0
    for s in skills:
        tags = [str(t).strip().lower() for t in (s.get("tags") or []) if isinstance(t, str)]
        if "mcp" not in tags:
            continue
        mcp_total += 1

        name = str(s.get("name") or "skill").strip() or "skill"
        desc = str(s.get("description") or "").strip()

        use_when = s.get("use_when")
        if not isinstance(use_when, list):
            use_when = []
        use_when_clean = [str(x).strip() for x in use_when if str(x).strip()]
        if not use_when_clean:
            use_when_clean = _default_mcp_use_when(name, desc)
            filled_use += 1
        s["use_when"] = use_when_clean

        workflow = s.get("workflow")
        if not isinstance(workflow, list):
            workflow = []
        workflow_clean = [str(x).strip() for x in workflow if str(x).strip()]
        if not workflow_clean:
            workflow_clean = _default_mcp_workflow(name)
            filled_workflow += 1
        s["workflow"] = workflow_clean

    return mcp_total, filled_use, filled_workflow


def _aggressive_autofill_and_normalize(skills: list[dict[str, Any]]) -> tuple[int, int, int]:
    use_when_filled = 0
    workflow_filled = 0
    tags_normalized = 0

    for s in skills:
        name = str(s.get("name") or "skill").strip() or "skill"
        desc = str(s.get("description") or "").strip()

        use_when = s.get("use_when")
        if not isinstance(use_when, list):
            use_when = []
        use_when_clean = [str(x).strip() for x in use_when if str(x).strip()]
        if not use_when_clean:
            use_when_clean = _default_general_use_when(name, desc)
            use_when_filled += 1
        s["use_when"] = use_when_clean

        workflow = s.get("workflow")
        if not isinstance(workflow, list):
            workflow = []
        workflow_clean = [str(x).strip() for x in workflow if str(x).strip()]
        if not workflow_clean:
            workflow_clean = _default_general_workflow(name)
            workflow_filled += 1
        s["workflow"] = workflow_clean

        tags = s.get("tags")
        if isinstance(tags, list):
            seen: set[str] = set()
            out: list[str] = []
            changed = False
            for t in tags:
                tt = slugify(str(t))
                if not tt:
                    changed = True
                    continue
                if tt != str(t):
                    changed = True
                if tt in seen:
                    changed = True
                    continue
                seen.add(tt)
                out.append(tt)
            if changed:
                tags_normalized += 1
                s["tags"] = out

    return use_when_filled, workflow_filled, tags_normalized


def _inject_score_lines(card_text: str, *, worth_score: int, quality_score: int) -> str:
    if _WORTH_LINE.search(card_text) and _QUALITY_LINE.search(card_text):
        return card_text

    lines = card_text.splitlines()
    # Preferred location: right after id line inside "## Quick Facts".
    qf_idx = None
    for i, ln in enumerate(lines):
        if _HEADING_QF.match(ln):
            qf_idx = i
            break

    if qf_idx is None:
        # Fallback: append compact quick facts section.
        out = card_text.rstrip() + "\n\n## Quick Facts\n"
        out += f"- worth_using_score: `{int(worth_score)}/100`\n"
        out += f"- quality_score: `{int(quality_score)}/100`\n"
        return out

    insert_at = qf_idx + 1
    for i in range(qf_idx + 1, len(lines)):
        ln = lines[i]
        if ln.startswith("## "):
            break
        if _ID_LINE.match(ln.strip()):
            insert_at = i + 1
            break
        # Keep moving through quick-fact bullet area.
        if ln.startswith("- "):
            insert_at = i + 1

    inserts: list[str] = []
    if not _WORTH_LINE.search(card_text):
        inserts.append(f"- worth_using_score: `{int(worth_score)}/100`")
    if not _QUALITY_LINE.search(card_text):
        inserts.append(f"- quality_score: `{int(quality_score)}/100`")
    for offset, line in enumerate(inserts):
        lines.insert(insert_at + offset, line)
    return "\n".join(lines).rstrip() + "\n"


def _patch_cards(skills: list[dict[str, Any]], cards_dir: Path, write: bool) -> tuple[int, int]:
    by_id: dict[str, tuple[int, int]] = {}
    for s in skills:
        sid = str(s.get("id") or "").strip()
        if not sid:
            continue
        worth = int(s.get("worth_score") or 0)
        quality = int(s.get("quality_score") or 0)
        by_id[sid] = (worth, quality)

    checked = 0
    patched = 0
    for sid, (worth, quality) in by_id.items():
        card = cards_dir / f"{sid}.md"
        if not card.exists():
            continue
        checked += 1
        txt = card.read_text(encoding="utf-8", errors="replace")
        new_txt = _inject_score_lines(txt, worth_score=worth, quality_score=quality)
        if new_txt != txt:
            patched += 1
            if write:
                card.write_text(new_txt, encoding="utf-8", newline="\n")
    return checked, patched


def _root_rank(root_label: str) -> tuple[int, str]:
    key = str(root_label).strip().lower()
    return (_ROOT_PRIORITY.get(key, 5), key)


def _build_alias_manifest(skills: list[dict[str, Any]]) -> tuple[dict[str, Any], int, int]:
    by_name_key: dict[str, list[dict[str, Any]]] = {}
    for s in skills:
        sid = str(s.get("id") or "").strip()
        name = str(s.get("name") or "").strip()
        if not sid or not name:
            continue
        key = slugify(name)
        by_name_key.setdefault(key, []).append(s)

    aliases: list[dict[str, Any]] = []
    duplicate_name_keys = 0
    duplicate_skills_total = 0

    for key in sorted(by_name_key.keys()):
        cluster = by_name_key[key]
        if len(cluster) <= 1:
            continue
        duplicate_name_keys += 1
        duplicate_skills_total += len(cluster)

        ranked = sorted(
            cluster,
            key=lambda s: (
                -int(s.get("quality_score") or 0),
                -int(s.get("worth_score") or 0),
                _root_rank(str(s.get("root_label") or "")),
                str(s.get("id") or ""),
            ),
        )
        canonical = ranked[0]
        canonical_id = str(canonical.get("id") or "")
        aliases.append(
            {
                "name_key": key,
                "canonical_id": canonical_id,
                "member_ids": [str(s.get("id") or "") for s in ranked],
                "member_names": sorted(
                    {
                        str(s.get("name") or "")
                        for s in ranked
                        if isinstance(s.get("name"), str) and str(s.get("name") or "").strip()
                    }
                ),
                "selection_policy": "quality_score_desc,worth_score_desc,root_priority,id",
            }
        )

    manifest = {
        "schema_version": 1,
        "alias_count": len(aliases),
        "aliases": aliases,
    }
    return manifest, duplicate_name_keys, duplicate_skills_total


def curate_artifacts(
    *,
    skills_json: Path,
    cards_dir: Path,
    aliases_json: Path,
    write: bool = False,
    fix_level: str = "safe",
) -> dict[str, Any]:
    level = str(fix_level).strip().lower()
    if level not in ("safe", "aggressive"):
        raise ValueError("fix_level must be one of: safe, aggressive")

    data = _read_json(skills_json)
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("skills.json missing skills[] list")

    mcp_total, mcp_use_when_filled, mcp_workflow_filled = _ensure_mcp_guidance(skills)
    general_use_when_filled = 0
    general_workflow_filled = 0
    tags_normalized = 0
    if level == "aggressive":
        general_use_when_filled, general_workflow_filled, tags_normalized = _aggressive_autofill_and_normalize(skills)
    cards_checked, cards_patched_score = _patch_cards(skills=skills, cards_dir=cards_dir, write=write)
    aliases_manifest, duplicate_name_keys, duplicate_skills_total = _build_alias_manifest(skills)

    data["count"] = len(skills)
    data["curation"] = {
        "schema_version": 1,
        "fix_level": level,
        "mcp_use_when_filled": mcp_use_when_filled,
        "mcp_workflow_filled": mcp_workflow_filled,
        "general_use_when_filled": general_use_when_filled,
        "general_workflow_filled": general_workflow_filled,
        "tags_normalized": tags_normalized,
        "cards_patched_score": cards_patched_score,
        "duplicate_name_keys": duplicate_name_keys,
        "aliases_json": str(aliases_json),
    }

    if write:
        skills_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
        aliases_json.parent.mkdir(parents=True, exist_ok=True)
        aliases_json.write_text(
            json.dumps(aliases_manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
            newline="\n",
        )

    report = CurateReport(
        skills_total=len(skills),
        mcp_total=mcp_total,
        mcp_use_when_filled=mcp_use_when_filled,
        mcp_workflow_filled=mcp_workflow_filled,
        general_use_when_filled=general_use_when_filled,
        general_workflow_filled=general_workflow_filled,
        tags_normalized=tags_normalized,
        cards_checked=cards_checked,
        cards_patched_score=cards_patched_score,
        duplicate_name_keys=duplicate_name_keys,
        duplicate_skills_total=duplicate_skills_total,
        alias_entries=int(aliases_manifest.get("alias_count") or 0),
        fix_level=level,
        write=bool(write),
        skills_json=str(skills_json),
        cards_dir=str(cards_dir),
        aliases_json=str(aliases_json),
    )
    payload = report.to_json()
    payload["aliases_preview"] = aliases_manifest.get("aliases", [])[:20]
    return payload

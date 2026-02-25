from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .util import keywords_from_query


_PROCESS_SKILLS = {
    "brainstorming",
    "writing-plans",
    "executing-plans",
    "dispatching-parallel-agents",
    "test-driven-development",
    "systematic-debugging",
    "requesting-code-review",
    "receiving-code-review",
    "using-git-worktrees",
    "finishing-a-development-branch",
    "verification-before-completion",
    "subagent-driven-development",
    "using-superpowers",
}

_PHASE_TERMS: dict[str, set[str]] = {
    "debug": {"debug", "bug", "fix", "flaky", "failing", "error", "trace", "triage"},
    "plan": {"plan", "spec", "design", "brainstorm", "requirements"},
    "review": {"review", "audit", "pr", "code-review"},
    "implement": {"implement", "build", "create", "add", "write"},
    "ship": {"merge", "release", "deploy", "publish"},
}

_STRONG_PHASE_TERMS = {
    "debug": {"debug", "fix", "flaky", "error", "failing"},
    "plan": {"plan", "spec", "design", "brainstorm"},
    "review": {"review", "audit"},
}

_TOOL_TERMS: dict[str, set[str]] = {
    "playwright": {"playwright", "browser", "e2e"},
    "mcp": {"mcp", "model-context-protocol"},
    "docker": {"docker", "compose", "container"},
    "kubernetes": {"kubernetes", "k8s", "kubectl"},
    "python": {"python", "pytest", "ruff", "mypy"},
    "git": {"git", "github", "gh"},
}


@dataclass(frozen=True)
class AliasHit:
    phrase: str
    skill: str
    phase: str | None


@dataclass(frozen=True)
class QueryContext:
    query: str
    normalized_query: str
    phase: str | None
    strong_phase: bool
    tools: list[str]
    keywords: list[str]
    alias_hits: list[AliasHit]

    def to_json(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "normalized_query": self.normalized_query,
            "phase": self.phase,
            "strong_phase": self.strong_phase,
            "tools": self.tools,
            "keywords": self.keywords,
            "alias_hits": [
                {"phrase": h.phrase, "skill": h.skill, "phase": h.phase} for h in self.alias_hits
            ],
        }


@dataclass(frozen=True)
class SkillProfile:
    kind: str
    phases: list[str]
    tools: list[str]
    source_kind: str


def _normalize_query(query: str) -> str:
    return re.sub(r"\s+", " ", query.strip().lower())


def _term_in_text(term: str, normalized: str, tokens: set[str]) -> bool:
    if " " in term:
        return term in normalized
    return term in tokens


def _load_alias_rules(alias_json: Path | None) -> list[dict[str, Any]]:
    if not alias_json:
        return []
    if not alias_json.exists():
        return []
    try:
        data = json.loads(alias_json.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return []

    rules = data.get("aliases", []) if isinstance(data, dict) else []
    out: list[dict[str, Any]] = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        phrase = str(rule.get("phrase") or "").strip().lower()
        skill = str(rule.get("skill") or "").strip().lower()
        phase = str(rule.get("phase") or "").strip().lower() or None
        if phrase and skill:
            out.append({"phrase": phrase, "skill": skill, "phase": phase})
    return out


def parse_query_context(query: str, alias_json: Path | None = None) -> QueryContext:
    normalized = _normalize_query(query)
    keywords = keywords_from_query(normalized)
    token_set = set(keywords)

    phase_scores: dict[str, int] = {k: 0 for k in _PHASE_TERMS}
    strong_flags: dict[str, bool] = {k: False for k in _PHASE_TERMS}

    for phase, terms in _PHASE_TERMS.items():
        for term in terms:
            if _term_in_text(term, normalized, token_set):
                phase_scores[phase] += 1
    for phase, terms in _STRONG_PHASE_TERMS.items():
        strong_flags[phase] = any(_term_in_text(term, normalized, token_set) for term in terms)

    phase = None
    if any(v > 0 for v in phase_scores.values()):
        phase = sorted(phase_scores.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]

    tools: list[str] = []
    for tool, terms in _TOOL_TERMS.items():
        if any(_term_in_text(term, normalized, token_set) for term in terms):
            tools.append(tool)

    alias_hits: list[AliasHit] = []
    for rule in _load_alias_rules(alias_json):
        if rule["phrase"] in normalized:
            alias_hits.append(
                AliasHit(phrase=rule["phrase"], skill=rule["skill"], phase=rule["phase"])
            )

    alias_phases = [h.phase for h in alias_hits if h.phase]
    if alias_phases:
        if phase is None or phase not in alias_phases:
            phase = alias_phases[0]

    strong_phase = bool(phase and strong_flags.get(phase, False))
    return QueryContext(
        query=query,
        normalized_query=normalized,
        phase=phase,
        strong_phase=strong_phase,
        tools=tools,
        keywords=keywords,
        alias_hits=alias_hits,
    )


def detect_source_kind(source_path: str, root_label: str) -> str:
    src = source_path.replace("\\", "/").lower()
    if src.startswith("http://") or src.startswith("https://"):
        return "external"
    if "/skillpacks/superpowers/" in src:
        return "superpowers"
    if "/skillpacks/" in src:
        return "local"
    if root_label == "external":
        return "external"
    return "core"


def classify_skill(
    name: str,
    description: str,
    tags: str,
    use_when: str,
    workflow: str,
    source_kind: str,
) -> SkillProfile:
    name_l = name.strip().lower()
    blob = "\n".join([name, description, tags, use_when, workflow]).lower()
    blob_tokens = set(keywords_from_query(blob))

    kind = "domain"
    if name_l in _PROCESS_SKILLS:
        kind = "process"
    elif any(token in blob for token in ("workflow", "debug", "review", "plan")):
        kind = "process"
    elif source_kind == "superpowers":
        kind = "process"

    phases: list[str] = []
    for phase, terms in _PHASE_TERMS.items():
        if any(_term_in_text(term, blob, blob_tokens) for term in terms):
            phases.append(phase)
    if not phases and kind == "process":
        phases = ["implement"]

    tools: list[str] = []
    for tool, terms in _TOOL_TERMS.items():
        if any(_term_in_text(term, blob, blob_tokens) for term in terms):
            tools.append(tool)

    return SkillProfile(
        kind=kind,
        phases=sorted(set(phases)),
        tools=sorted(set(tools)),
        source_kind=source_kind,
    )

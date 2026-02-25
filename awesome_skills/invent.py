from __future__ import annotations

import json
import math
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .util import ensure_dir, keywords_from_query, slugify


ACTION_KEYWORDS: dict[str, tuple[str, ...]] = {
    "setup": ("setup", "install", "bootstrap", "initialize", "scaffold"),
    "debug": ("debug", "troubleshoot", "triage", "diagnose", "root cause"),
    "testing": ("test", "testing", "validation", "qa", "regression", "verify", "smoke"),
    "automation": ("automation", "automate", "batch", "pipeline", "workflow"),
    "hardening": ("hardening", "secure", "safety", "hygiene", "least-privilege"),
    "optimization": ("optimization", "optimize", "performance", "latency", "cost"),
    "migration": ("migration", "migrate", "upgrade", "transition", "port"),
    "review": ("review", "audit", "assessment", "checklist"),
    "operations": ("operations", "ops", "runbook", "oncall", "incident", "production"),
    "governance": ("governance", "policy", "compliance", "standard"),
    "recovery": ("recovery", "rollback", "restore", "drill", "failover"),
    "forensics": ("forensics", "trace", "investigation"),
}

CORE_ACTIONS = [
    "setup",
    "debug",
    "testing",
    "automation",
    "hardening",
    "optimization",
    "migration",
    "review",
    "operations",
]

DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "python": ("python", "fastapi", "django", "flask", "pydantic", "pandas", "polars"),
    "data": ("sql", "postgres", "mysql", "sqlite", "spark", "airflow", "dbt", "duckdb"),
    "llm": ("llm", "model", "prompt", "agent"),
    "rag": ("rag", "retrieval", "embedding", "vector"),
    "mcp": ("mcp", "tool schema", "context protocol"),
    "browser": ("playwright", "browser", "chrome", "firefox", "mozilla", "devtools"),
    "obsidian": ("obsidian", "vault", "dataview", "templater"),
    "cursor": ("cursor", "rules"),
    "warp": ("warp", "terminal"),
    "security": ("security", "oauth", "jwt", "secret", "slsa", "sbom", "threat", "compliance"),
    "devops": ("devops", "sre", "kubernetes", "docker", "terraform", "ci", "cd", "release"),
    "github": ("github", "git", "actions"),
    "wsl": ("wsl",),
    "windows": ("windows", "powershell"),
    "linux": ("linux", "systemd", "journalctl", "kernel"),
    "hytale": ("hytale", "hyimporter", "blockbench", "comfyui"),
}

DOMAIN_LABELS: dict[str, str] = {
    "python": "Python",
    "data": "Data Engineering",
    "llm": "LLM Engineering",
    "rag": "RAG Systems",
    "mcp": "MCP",
    "browser": "Browser Automation",
    "obsidian": "Obsidian",
    "cursor": "Cursor",
    "warp": "Warp",
    "security": "Security",
    "devops": "DevOps",
    "github": "GitHub",
    "wsl": "WSL",
    "windows": "Windows",
    "linux": "Linux",
    "hytale": "Hytale",
}

ACTION_LABELS: dict[str, str] = {
    "setup": "Setup",
    "debug": "Debug",
    "testing": "Testing",
    "automation": "Automation",
    "hardening": "Hardening",
    "optimization": "Optimization",
    "migration": "Migration",
    "review": "Review",
    "operations": "Operations",
    "governance": "Governance",
    "recovery": "Recovery",
    "forensics": "Forensics",
}


@dataclass(frozen=True)
class ProposedSkill:
    name: str
    title: str
    description: str
    rationale: str
    score: float
    domains: list[str]
    action: str
    kind: str
    metrics: dict[str, float | int]

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "rationale": self.rationale,
            "score": round(self.score, 4),
            "domains": list(self.domains),
            "action": self.action,
            "kind": self.kind,
            "metrics": self.metrics,
        }


def _text_blob(skill: dict[str, object]) -> str:
    tags = skill.get("tags") or []
    use_when = skill.get("use_when") or []
    workflow = skill.get("workflow") or []
    return "\n".join(
        [
            str(skill.get("name") or ""),
            str(skill.get("description") or ""),
            " ".join(str(x) for x in tags if isinstance(x, str)),
            " ".join(str(x) for x in use_when if isinstance(x, str)),
            " ".join(str(x) for x in workflow if isinstance(x, str)),
        ]
    ).lower()


def _extract_actions(skill: dict[str, object]) -> list[str]:
    text = _text_blob(skill)
    out: list[str] = []
    for action, kws in ACTION_KEYWORDS.items():
        if any(k in text for k in kws):
            out.append(action)
    # Lightweight fallback to avoid dropping sparse records entirely.
    if not out:
        tags = {str(t).lower() for t in (skill.get("tags") or []) if isinstance(t, str)}
        if "testing" in tags:
            out.append("testing")
        elif "security" in tags:
            out.append("hardening")
        elif "devops" in tags:
            out.append("operations")
    return sorted(set(out))


def _extract_domains(skill: dict[str, object]) -> list[str]:
    text = _text_blob(skill)
    tags = {str(t).lower() for t in (skill.get("tags") or []) if isinstance(t, str)}
    out: list[str] = []
    for domain, kws in DOMAIN_KEYWORDS.items():
        if domain in tags or any(k in text for k in kws):
            out.append(domain)
    return sorted(set(out))


def _domain_slug(domains: Iterable[str]) -> str:
    return "-".join(slugify(d) for d in domains)


def _action_gap_candidates(
    existing_names: set[str],
    domain_count: dict[str, int],
    domain_action_count: dict[tuple[str, str], int],
) -> list[ProposedSkill]:
    out: list[ProposedSkill] = []
    for domain, dcount in sorted(domain_count.items(), key=lambda kv: (-kv[1], kv[0])):
        if dcount < 8:
            continue
        for action in CORE_ACTIONS:
            covered = domain_action_count.get((domain, action), 0)
            if covered > max(6, int(dcount * 0.35)):
                continue

            scarcity = 1.0 / (1.0 + covered)
            score = math.log2(dcount + 2.0) * scarcity * 8.0
            name = f"{_domain_slug([domain])}-{action}-playbook"
            if name in existing_names:
                continue

            domain_label = DOMAIN_LABELS.get(domain, domain.title())
            action_label = ACTION_LABELS.get(action, action.title())
            title = f"{domain_label} {action_label} Playbook"
            description = (
                f"Generated gap-fill playbook for {domain_label}. Focuses on {action_label.lower()} "
                "workflows with deterministic validation and rollback guidance."
            )
            rationale = (
                f"Coverage gap: domain '{domain}' appears {dcount} times, but action '{action}' "
                f"appears only {covered} times within that domain."
            )
            out.append(
                ProposedSkill(
                    name=name,
                    title=title,
                    description=description,
                    rationale=rationale,
                    score=score,
                    domains=[domain],
                    action=action,
                    kind="domain-gap",
                    metrics={"domain_count": dcount, "domain_action_count": covered},
                )
            )
    return out


def _bridge_candidates(
    existing_names: set[str],
    domain_count: dict[str, int],
    domain_pair_count: dict[tuple[str, str], int],
    domain_action_count: dict[tuple[str, str], int],
) -> list[ProposedSkill]:
    out: list[ProposedSkill] = []
    domains = sorted(domain_count.keys())
    for i, a in enumerate(domains):
        for b in domains[i + 1 :]:
            fa = domain_count.get(a, 0)
            fb = domain_count.get(b, 0)
            if min(fa, fb) < 10:
                continue
            co = domain_pair_count.get((a, b), 0)
            novelty = 1.0 / (1.0 + co)
            importance = math.sqrt(fa * fb)
            if novelty < 0.2:
                continue

            # Choose an action that is weakly covered across both domains.
            best_action = None
            best_cov = None
            for action in CORE_ACTIONS:
                cov = domain_action_count.get((a, action), 0) + domain_action_count.get((b, action), 0)
                if best_cov is None or cov < best_cov:
                    best_cov = cov
                    best_action = action
            if best_action is None or best_cov is None:
                continue

            score = (importance * novelty) / (1.0 + best_cov * 0.5)
            name = f"{_domain_slug([a, b])}-{best_action}-playbook"
            if name in existing_names:
                continue

            a_label = DOMAIN_LABELS.get(a, a.title())
            b_label = DOMAIN_LABELS.get(b, b.title())
            action_label = ACTION_LABELS.get(best_action, best_action.title())
            title = f"{a_label} + {b_label} {action_label} Playbook"
            description = (
                f"Bridge playbook linking {a_label} and {b_label}. Focuses on "
                f"{action_label.lower()} concerns where these domains interact."
            )
            rationale = (
                f"Bridge opportunity: domains '{a}' ({fa}) and '{b}' ({fb}) are individually common but "
                f"co-occur only {co} times."
            )
            out.append(
                ProposedSkill(
                    name=name,
                    title=title,
                    description=description,
                    rationale=rationale,
                    score=score,
                    domains=[a, b],
                    action=best_action,
                    kind="bridge-gap",
                    metrics={
                        "domain_a_count": fa,
                        "domain_b_count": fb,
                        "pair_count": co,
                        "action_cov_pair": best_cov,
                    },
                )
            )
    return out


def propose_novel_skills(
    skills: list[dict[str, object]],
    limit: int = 20,
    exclude_domains: Iterable[str] = (),
) -> list[ProposedSkill]:
    exclude = {slugify(x) for x in exclude_domains if x}
    existing_names = {slugify(str(s.get("name") or "")) for s in skills if s.get("name")}

    domain_count: dict[str, int] = {}
    domain_action_count: dict[tuple[str, str], int] = {}
    domain_pair_count: dict[tuple[str, str], int] = {}

    for skill in skills:
        domains = [d for d in _extract_domains(skill) if d not in exclude]
        if not domains:
            continue
        actions = _extract_actions(skill)

        for d in domains:
            domain_count[d] = domain_count.get(d, 0) + 1
            for a in actions:
                domain_action_count[(d, a)] = domain_action_count.get((d, a), 0) + 1

        uniq = sorted(set(domains))
        for i, a in enumerate(uniq):
            for b in uniq[i + 1 :]:
                domain_pair_count[(a, b)] = domain_pair_count.get((a, b), 0) + 1

    candidates = _action_gap_candidates(existing_names, domain_count, domain_action_count)
    candidates.extend(_bridge_candidates(existing_names, domain_count, domain_pair_count, domain_action_count))

    # Strong dedupe: name uniqueness only.
    by_name: dict[str, ProposedSkill] = {}
    for c in candidates:
        key = slugify(c.name)
        prev = by_name.get(key)
        if prev is None or c.score > prev.score:
            by_name[key] = c

    ranked = sorted(
        by_name.values(),
        key=lambda c: (
            -c.score,
            c.kind,
            c.name,
        ),
    )
    return ranked[: max(0, limit)]


def render_skill_stub(c: ProposedSkill) -> str:
    domains_text = ", ".join(DOMAIN_LABELS.get(d, d.title()) for d in c.domains)
    action_label = ACTION_LABELS.get(c.action, c.action.title())
    body = f"""---
name: {c.name}
description: >
  {c.description}
---

# {c.title}

## Why This Exists
- Proposed automatically from corpus coverage gaps.
- Domains: {domains_text}
- Focus action: {action_label}

## Trigger Cues
- You are working in {domains_text} and need a structured {action_label.lower()} playbook.
- Existing skills cover the domain broadly but miss this exact workflow shape.

## Procedure
1. Capture baseline behavior and explicit success criteria.
2. Apply minimal changes scoped to the target issue.
3. Validate outcomes with deterministic checks.
4. Record residual risks and rollback steps.

## Validation Gates
- Baseline vs final evidence is preserved.
- Relevant tests/checks pass.
- Rollback path is documented and executable.

## Rationale
{c.rationale}
"""
    return textwrap.dedent(body).strip() + "\n"


def write_skill_stubs(candidates: list[ProposedSkill], out_dir: Path) -> list[Path]:
    ensure_dir(out_dir)
    written: list[Path] = []
    for c in candidates:
        skill_dir = out_dir / slugify(c.name)
        ensure_dir(skill_dir)
        path = skill_dir / "SKILL.md"
        path.write_text(render_skill_stub(c), encoding="utf-8", newline="\n")
        written.append(path)
    return written


def load_skills_json(skills_json: Path) -> list[dict[str, object]]:
    data = json.loads(skills_json.read_text(encoding="utf-8", errors="replace"))
    skills = data.get("skills", [])
    if not isinstance(skills, list):
        raise ValueError("skills.json missing skills[] list")
    out: list[dict[str, object]] = []
    for item in skills:
        if isinstance(item, dict):
            out.append(item)
    return out


def infer_exclude_domains_from_query(query: str) -> list[str]:
    """
    Optional helper: infer exclusions from user-like query terms.
    Example: "everything but hytale" -> ["hytale"].
    """
    terms = keywords_from_query(query)
    excludes: list[str] = []
    for t in terms:
        tslug = slugify(t)
        if tslug in DOMAIN_KEYWORDS:
            excludes.append(tslug)
    return excludes

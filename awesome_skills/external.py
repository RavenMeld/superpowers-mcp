from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .condense import SkillRecord
from .scoring import SkillFeatures, worth_using_score
from .util import redact_obvious_secrets, sha1_hex, slugify


@dataclass(frozen=True)
class ExternalCandidate:
    url: str
    section: str
    notes: list[str]


_TOP_URL = re.compile(r"^-\s+(https?://\S+)\s*$")
_HEADING = re.compile(r"^(#{2,3})\s+(.+?)\s*$")


def _candidate_name(url: str) -> str:
    # Stable-ish human name from URL (no network).
    m = re.match(r"^https?://github\.com/([^/]+)/([^/#?]+)", url)
    if m:
        return f"{m.group(1)}/{m.group(2)}"

    m = re.match(r"^https?://www\.reddit\.com/r/([^/]+)/comments/([^/]+)/?", url)
    if m:
        return f"reddit:r/{m.group(1)}:{m.group(2)}"

    m = re.match(r"^https?://([^/]+)/(.+)$", url)
    if m:
        host = m.group(1)
        tail = m.group(2).rstrip("/").split("/")[-1]
        tail = tail or host
        return f"{host}:{tail}"

    return url


def _infer_tags(text: str) -> list[str]:
    # Match condense.py's tag list (plus a couple extras) for consistent browsing.
    hay = text.lower()
    tags: list[str] = []
    for t in [
        "mcp",
        "github",
        "git",
        "ssh",
        "cursor",
        "playwright",
        "browser",
        "chrome",
        "firefox",
        "mozilla",
        "warp",
        "terminal",
        "obsidian",
        "security",
        "hytale",
        "blockbench",
        "hyimporter",
        "python",
        "sql",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "wsl",
        "windows",
        "linux",
        "powershell",
        "devops",
        "observability",
        "rag",
        "llm",
        "eval",
        "reddit",
        "registry",
        "course",
        "benchmark",
    ]:
        if t in hay:
            tags.append(t)
    return tags


def parse_external_candidates(md_text: str) -> list[ExternalCandidate]:
    section = ""
    cur_url: str | None = None
    cur_notes: list[str] = []
    out: list[ExternalCandidate] = []

    for raw in md_text.splitlines():
        hm = _HEADING.match(raw.strip())
        if hm:
            # Track last seen section heading for better tags/context.
            section = hm.group(2).strip()
            continue

        m = _TOP_URL.match(raw.rstrip())
        if m:
            if cur_url:
                out.append(ExternalCandidate(url=cur_url, section=section, notes=cur_notes))
            cur_url = m.group(1)
            cur_notes = []
            continue

        if cur_url and raw.startswith("  - "):
            note = raw.strip()[2:].strip()
            if note:
                cur_notes.append(note)

    if cur_url:
        out.append(ExternalCandidate(url=cur_url, section=section, notes=cur_notes))

    return out


def build_external_records(candidates_md: Path) -> tuple[list[SkillRecord], dict[str, str]]:
    """
    Convert `sources/external_candidates.md` into synthetic SkillRecords so they are searchable
    alongside real SKILL.md content, without adding any network calls.
    """
    text = candidates_md.read_text(encoding="utf-8", errors="replace")
    candidates = parse_external_candidates(text)

    records: list[SkillRecord] = []
    cards: dict[str, str] = {}

    for c in candidates:
        name = _candidate_name(c.url)
        description = c.notes[0] if c.notes else ""
        # Put remaining notes in use_when for searchability.
        use_when = c.notes[1:] if len(c.notes) > 1 else []

        body_for_signals = "\n".join([name, c.section, description] + c.notes)
        word_count = len(re.findall(r"\S+", body_for_signals))

        features = SkillFeatures(
            has_description=bool(description),
            has_use_when=bool(use_when),
            has_workflow=False,
            code_fence_count=0,
            has_scripts=False,
            has_references=False,
            has_assets=False,
            word_count=word_count,
        )
        worth = worth_using_score(features)

        sid = f"{slugify(name)}--{sha1_hex(c.url)[:10]}"
        tags = _infer_tags(body_for_signals)

        rec = SkillRecord(
            id=sid,
            name=name,
            description=redact_obvious_secrets(description),
            root_label="external",
            source_path=c.url,
            rel_hint=str(candidates_md),
            worth_score=worth,
            features=features,
            tags=tags,
            use_when=[redact_obvious_secrets(x) for x in use_when],
            workflow=[],
        )
        records.append(rec)
        cards[sid] = _render_external_card(rec, c.section, c.url, c.notes)

    return records, cards


def _render_external_card(rec: SkillRecord, section: str, url: str, notes: list[str]) -> str:
    lines: list[str] = []
    lines.append(f"# {rec.name}")
    lines.append("")
    if rec.description:
        lines.append(rec.description)
        lines.append("")

    lines.append("## Quick Facts")
    lines.append(f"- id: `{rec.id}`")
    lines.append(f"- kind: `external`")
    if section:
        lines.append(f"- section: `{section}`")
    if rec.tags:
        lines.append(f"- tags: `{', '.join(rec.tags)}`")
    lines.append(f"- url: `{url}`")
    lines.append(f"- source_path: `{rec.source_path}`")
    lines.append("")

    if notes:
        lines.append("## Notes")
        for n in notes[:12]:
            lines.append(f"- {redact_obvious_secrets(n)}")
        lines.append("")

    # Features summary (keep consistent with normal cards).
    f = rec.features
    lines.append("## Signal Summary")
    lines.append(f"- has_description: `{bool(f.has_description)}`")
    lines.append(f"- has_use_when: `{bool(f.has_use_when)}`")
    lines.append(f"- has_workflow: `{bool(f.has_workflow)}`")
    lines.append(f"- code_examples: `{f.code_fence_count}`")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"

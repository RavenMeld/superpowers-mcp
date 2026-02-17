from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .frontmatter import parse_frontmatter
from .scoring import SkillFeatures, worth_using_score
from .util import normalize_path, redact_obvious_secrets, sha1_hex, slugify


_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_HEADING = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")
_FENCE = re.compile(r"^```", re.MULTILINE)


@dataclass(frozen=True)
class SkillRecord:
    id: str
    name: str
    description: str
    root_label: str
    source_path: str
    rel_hint: str
    worth_score: int
    features: SkillFeatures
    tags: list[str]
    use_when: list[str]
    workflow: list[str]

    def to_json(self) -> dict[str, Any]:
        d = asdict(self)
        # dataclass -> dict will inline features as dict already (since frozen dataclass).
        return d


def _first_paragraph(text: str) -> str:
    # Extract the first non-heading paragraph.
    lines = [ln.rstrip() for ln in text.splitlines()]
    # Skip initial headings and blank lines.
    i = 0
    while i < len(lines) and (not lines[i].strip() or lines[i].lstrip().startswith("#")):
        i += 1
    para: list[str] = []
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            break
        if ln.lstrip().startswith("#"):
            break
        para.append(ln)
        i += 1
    return " ".join(para).strip()


def _extract_section_lines(body: str, heading_keywords: list[str], max_lines: int) -> list[str]:
    """
    Extract a few lines under the first heading that matches any keyword.
    """
    kws = [k.lower() for k in heading_keywords]
    lines = body.splitlines()
    start = None
    base_level = None
    for i, raw in enumerate(lines):
        m = _HEADING.match(raw.strip())
        if not m:
            continue
        title = m.group("title").strip().lower()
        if any(k in title for k in kws):
            start = i + 1
            base_level = len(m.group("hashes"))
            break
    if start is None:
        return []

    out: list[str] = []
    for raw in lines[start:]:
        m = _HEADING.match(raw.strip())
        if m and base_level is not None and len(m.group("hashes")) <= base_level:
            break
        if len(out) >= max_lines:
            break
        s = raw.rstrip()
        if not s.strip():
            # keep at most one blank as a separator
            if out and out[-1] != "":
                out.append("")
            continue
        out.append(s)

    # Trim trailing blanks
    while out and out[-1] == "":
        out.pop()
    return out


def _extract_bullets(lines: list[str], max_items: int) -> list[str]:
    out: list[str] = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        if s.startswith(("-", "*")):
            item = s[1:].strip()
            if item:
                out.append(item)
        elif re.match(r"^\d+\.\s+", s):
            out.append(re.sub(r"^\d+\.\s+", "", s).strip())
        if len(out) >= max_items:
            break
    return out


def _infer_tags(name: str, description: str, body: str) -> list[str]:
    # Lightweight tags for better search UX.
    text = f"{name}\n{description}\n{body}".lower()
    tags: list[str] = []
    for t in [
        "mcp",
        "github",
        "playwright",
        "comfyui",
        "python",
        "typescript",
        "node",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "security",
        "testing",
        "ci",
        "docs",
        "figma",
        "obsidian",
    ]:
        if t in text:
            tags.append(t)
    return tags


def build_skill_record(root_label: str, skill_md: Path) -> tuple[SkillRecord, str]:
    raw = skill_md.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(raw)
    body = fm.body

    fm_name = fm.data.get("name")
    name = str(fm_name).strip() if isinstance(fm_name, str) and fm_name.strip() else ""
    if not name:
        m = _H1.search(body)
        if m:
            name = m.group(1).strip()
    if not name:
        name = skill_md.parent.name

    fm_desc = fm.data.get("description")
    description = str(fm_desc).strip() if isinstance(fm_desc, str) and fm_desc.strip() else ""
    if not description:
        description = _first_paragraph(body)
    description = description.strip()
    if len(description) > 400:
        description = description[:397].rstrip() + "..."

    # Extract use-when / trigger bullets (best-effort).
    use_lines = _extract_section_lines(
        body,
        heading_keywords=["use when", "triggers", "trigger", "when to use", "use this skill"],
        max_lines=80,
    )
    use_when = _extract_bullets(use_lines, max_items=10)

    # Extract workflow/process lines (best-effort).
    wf_lines = _extract_section_lines(
        body,
        heading_keywords=["workflow", "process", "steps", "procedure", "plan"],
        max_lines=60,
    )
    workflow = _extract_bullets(wf_lines, max_items=10)
    if not workflow:
        # Fallback: take first few non-empty lines from wf section if it exists.
        workflow = [ln.strip() for ln in wf_lines if ln.strip()][:6]

    code_fence_count = len(_FENCE.findall(body)) // 2

    skill_dir = skill_md.parent
    has_scripts = (skill_dir / "scripts").is_dir()
    has_references = (skill_dir / "references").is_dir()
    has_assets = (skill_dir / "assets").is_dir()
    word_count = len(re.findall(r"\\S+", body))

    features = SkillFeatures(
        has_description=bool(description),
        has_use_when=bool(use_when),
        has_workflow=bool(workflow),
        code_fence_count=code_fence_count,
        has_scripts=has_scripts,
        has_references=has_references,
        has_assets=has_assets,
        word_count=word_count,
    )
    worth_score = worth_using_score(features)

    # Stable-ish id based on (name + normalized source path).
    src_norm = normalize_path(skill_md)
    sid = f"{slugify(name)}--{sha1_hex(src_norm)[:10]}"

    tags = _infer_tags(name, description, body)

    rec = SkillRecord(
        id=sid,
        name=name,
        description=redact_obvious_secrets(description),
        root_label=root_label,
        source_path=str(skill_md),
        rel_hint=str(skill_md.parent),
        worth_score=worth_score,
        features=features,
        tags=tags,
        use_when=[redact_obvious_secrets(x) for x in use_when],
        workflow=[redact_obvious_secrets(x) for x in workflow],
    )

    card = render_card_markdown(rec)
    return rec, card


def render_card_markdown(rec: SkillRecord) -> str:
    lines: list[str] = []
    lines.append(f"# {rec.name}")
    lines.append("")
    lines.append(rec.description or "(no description found)")
    lines.append("")

    lines.append("## Quick Facts")
    lines.append(f"- id: `{rec.id}`")
    lines.append(f"- worth_using_score: `{rec.worth_score}/100`")
    if rec.tags:
        lines.append(f"- tags: `{', '.join(rec.tags)}`")
    lines.append(f"- source: `{rec.root_label}`")
    lines.append(f"- source_path: `{rec.source_path}`")
    lines.append("")

    if rec.use_when:
        lines.append("## Use When")
        for item in rec.use_when[:10]:
            lines.append(f"- {item}")
        lines.append("")

    if rec.workflow:
        lines.append("## Workflow / Steps")
        for item in rec.workflow[:10]:
            lines.append(f"- {item}")
        lines.append("")

    # Features summary (compact).
    f = rec.features
    lines.append("## Signal Summary")
    lines.append(f"- has_description: `{bool(f.has_description)}`")
    lines.append(f"- has_use_when: `{bool(f.has_use_when)}`")
    lines.append(f"- has_workflow: `{bool(f.has_workflow)}`")
    lines.append(f"- code_examples: `{f.code_fence_count}`")
    lines.append(f"- has_scripts: `{bool(f.has_scripts)}`")
    lines.append(f"- has_references: `{bool(f.has_references)}`")
    lines.append(f"- has_assets: `{bool(f.has_assets)}`")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"

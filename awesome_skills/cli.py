from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .condense import build_skill_record
from .db import build_db, list_top_worth, search_db
from .discover import discover_skill_mds
from .util import ensure_dir, slugify


def _default_roots() -> list[str]:
    # Best-effort defaults for this workspace; can be overridden via `--root`.
    return [
        "/home/wolvend/codex/agent_playground",
        "/home/wolvend/.codex/skills",
    ]


def _label_for_root(root: Path) -> str:
    p = str(root).replace("\\", "/")
    if p.endswith("/codex/agent_playground"):
        return "agent_playground"
    if p.endswith("/.codex/skills") or "/.codex/skills" in p:
        return "codex_skills"
    return slugify(root.name).replace("-", "_")


def cmd_build(args: argparse.Namespace) -> int:
    roots_raw: list[str] = args.root or _default_roots()
    roots: list[tuple[str, Path]] = []
    used: set[str] = set()
    for r in roots_raw:
        rp = Path(r).expanduser().resolve()
        label = _label_for_root(rp)
        if label in used:
            # Disambiguate.
            n = 2
            while f"{label}_{n}" in used:
                n += 1
            label = f"{label}_{n}"
        used.add(label)
        roots.append((label, rp))

    out_dir = Path(args.out).expanduser().resolve()
    cards_dir = out_dir / "cards"
    ensure_dir(cards_dir)
    # Avoid stale cards when a build input set changes.
    for p in cards_dir.glob("*.md"):
        try:
            p.unlink()
        except OSError:
            pass

    discovered = list(discover_skill_mds(roots))
    records = []
    card_by_id: dict[str, str] = {}

    for d in discovered:
        try:
            rec, card = build_skill_record(d.root_label, d.skill_md)
        except Exception as e:  # noqa: BLE001 - best-effort indexing
            print(f"[WARN] Failed to parse {d.skill_md}: {e}", file=sys.stderr)
            continue
        records.append(rec)
        card_by_id[rec.id] = card
        (cards_dir / f"{rec.id}.md").write_text(card, encoding="utf-8")

    # Stable sort for deterministic JSON.
    records.sort(key=lambda r: (r.name.lower(), r.id))

    skills_json = out_dir / "skills.json"
    payload = {
        "schema_version": 1,
        "count": len(records),
        "roots": [{"label": lbl, "path": str(p)} for (lbl, p) in roots],
        "skills": [r.to_json() for r in records],
    }
    skills_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # Human-friendly generated index.
    _write_index_md(out_dir, records)
    if out_dir.name == "dist":
        # Convenience for GitHub browsing (keep a top-level entrypoint).
        src = out_dir / "AWESOME_SKILLS.md"
        dst = out_dir.parent / "AWESOME_SKILLS.md"
        try:
            text = src.read_text(encoding="utf-8")
            # Fix relative links when mirrored to repo root.
            text = text.replace("(cards/", "(dist/cards/")
            dst.write_text(text, encoding="utf-8")
        except OSError:
            pass

    if not args.no_sqlite:
        db_path = out_dir / "awesome_skills.sqlite"
        build_db(db_path, records, card_by_id)

    print(f"Indexed {len(records)} skills into {out_dir}")
    return 0


def _write_index_md(out_dir: Path, records) -> None:
    # Group by tags for browsing.
    by_tag: dict[str, list] = {}
    for r in records:
        for t in r.tags:
            by_tag.setdefault(t, []).append(r)
    for t in list(by_tag.keys()):
        by_tag[t].sort(key=lambda r: (-r.worth_score, r.name.lower(), r.id))

    top = sorted(records, key=lambda r: (-r.worth_score, r.name.lower(), r.id))[:50]

    lines: list[str] = []
    lines.append("# Awesome SKILLS Database (Generated)")
    lines.append("")
    lines.append(f"- total_skills: `{len(records)}`")
    lines.append("")

    lines.append("## Top (Worth Using)")
    for r in top:
        lines.append(f"- [{r.name} (`{r.worth_score}/100`)](cards/{r.id}.md)")
    lines.append("")

    lines.append("## By Tag")
    for tag in sorted(by_tag.keys()):
        lines.append(f"### {tag}")
        for r in by_tag[tag][:30]:
            lines.append(f"- [{r.name} (`{r.worth_score}/100`)](cards/{r.id}.md)")
        lines.append("")

    (out_dir / "AWESOME_SKILLS.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _ensure_db(db_path: Path) -> bool:
    if db_path.exists():
        return True
    print(f"[ERROR] Missing DB: {db_path}. Run: python -m awesome_skills build", file=sys.stderr)
    return False


def cmd_search(args: argparse.Namespace) -> int:
    db_path = Path(args.db).expanduser().resolve()
    if not _ensure_db(db_path):
        return 2
    results = search_db(db_path, args.query, limit=args.limit)
    if args.json:
        print(
            json.dumps(
                [
                    {
                        "id": r.id,
                        "name": r.name,
                        "description": r.description,
                        "worth_score": r.worth_score,
                        "combined_score": r.combined_score,
                        "match_terms": r.match_terms,
                    }
                    for r in results
                ],
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    for i, r in enumerate(results, start=1):
        terms = f" (match: {', '.join(r.match_terms)})" if r.match_terms else ""
        print(f"{i}. {r.name}  [{r.worth_score}/100]{terms}")
        print(f"   id: {r.id}")
        if r.description:
            print(f"   {r.description}")
        print("")
    return 0


def cmd_top(args: argparse.Namespace) -> int:
    db_path = Path(args.db).expanduser().resolve()
    if not _ensure_db(db_path):
        return 2
    results = list_top_worth(db_path, limit=args.limit)
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r.name}  [{r.worth_score}/100]")
        print(f"   id: {r.id}")
        if r.description:
            print(f"   {r.description}")
        print("")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    card_path = Path(args.card).expanduser().resolve()
    if not card_path.exists():
        # Default location: dist/cards/<id>.md relative to cwd.
        card_path = (Path.cwd() / "dist" / "cards" / f"{args.id}.md").resolve()
    if not card_path.exists():
        print(f"[ERROR] Card not found for id={args.id}", file=sys.stderr)
        return 2
    sys.stdout.write(card_path.read_text(encoding="utf-8", errors="replace"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="awesome_skills")
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("build", help="Scan roots and build dist/ outputs.")
    pb.add_argument("--root", action="append", help="Root directory to scan (repeatable).")
    pb.add_argument("--out", default="dist", help="Output directory (default: dist).")
    pb.add_argument("--no-sqlite", action="store_true", help="Skip building SQLite FTS DB.")
    pb.set_defaults(func=cmd_build)

    ps = sub.add_parser("search", help="Search the SQLite FTS index.")
    ps.add_argument("query", help="FTS query (plain text is fine).")
    ps.add_argument("--db", default="dist/awesome_skills.sqlite", help="Path to SQLite DB.")
    ps.add_argument("--limit", type=int, default=10, help="Max results.")
    ps.add_argument("--json", action="store_true", help="JSON output.")
    ps.set_defaults(func=cmd_search)

    pt = sub.add_parser("top", help="List top skills by worth_using_score.")
    pt.add_argument("--db", default="dist/awesome_skills.sqlite", help="Path to SQLite DB.")
    pt.add_argument("--limit", type=int, default=20, help="Max results.")
    pt.set_defaults(func=cmd_top)

    pw = sub.add_parser("show", help="Show a condensed skill card by id.")
    pw.add_argument("id", help="Skill id.")
    pw.add_argument(
        "--card",
        default="",
        help="Optional explicit card path (default resolves to dist/cards/<id>.md).",
    )
    pw.set_defaults(func=cmd_show)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

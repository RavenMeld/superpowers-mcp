from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .bench import run_benchmark
from .curate import curate_artifacts
from .condense import build_skill_record
from .context import parse_query_context
from .db import build_db, context_search_db, list_top_worth, search_db
from .discover import discover_skill_mds
from .external import build_external_records
from .invent import load_skills_json, propose_novel_skills, write_skill_stubs
from .util import ensure_dir, slugify
from .verify import verify_artifacts


def _default_roots() -> list[str]:
    # Best-effort defaults for this workspace; can be overridden via `--root`.
    return [
        "/home/wolvend/codex/agent_playground",
        "/home/wolvend/.codex/skills",
        "/home/wolvend/.agents/skills",
    ]


def _label_for_root(root: Path) -> str:
    p = str(root).replace("\\", "/")
    if p.endswith("/codex/agent_playground"):
        return "agent_playground"
    if p.endswith("/.codex/skills") or "/.codex/skills" in p:
        return "codex_skills"
    if p.endswith("/.agents/skills") or "/.agents/skills" in p:
        return "agents_skills"
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

    # Optional: index a curated external candidate list (no network).
    candidates_md = (Path.cwd() / "sources" / "external_candidates.md").resolve()
    if candidates_md.exists():
        try:
            ext_records, ext_cards = build_external_records(candidates_md)
            for rec in ext_records:
                records.append(rec)
                card_by_id[rec.id] = ext_cards.get(rec.id, "")
                (cards_dir / f"{rec.id}.md").write_text(card_by_id[rec.id], encoding="utf-8")
        except Exception as e:  # noqa: BLE001 - best-effort indexing
            print(f"[WARN] Failed to index external candidates {candidates_md}: {e}", file=sys.stderr)

    # Stable sort for deterministic JSON.
    records.sort(key=lambda r: (r.name.lower(), r.id))

    skills_json = out_dir / "skills.json"
    payload = {
        "schema_version": 2,
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
    alias_json = None if args.no_alias_collapse else Path(args.alias_json).expanduser().resolve()
    strategy = str(args.strategy or "classic").strip().lower()
    if strategy not in {"auto", "classic", "context"}:
        print(f"[ERROR] invalid --strategy={strategy}; expected auto|classic|context", file=sys.stderr)
        return 2

    context_alias_json = Path(args.context_alias_json).expanduser().resolve()
    query_context: dict | None = None
    mode_used = "classic"
    use_context = strategy == "context"
    if strategy == "auto":
        qc = parse_query_context(args.query, alias_json=context_alias_json)
        query_context = qc.to_json()
        use_context = bool(qc.phase or qc.tools or qc.alias_hits)

    if use_context:
        context, ctx_results, alternatives = context_search_db(
            db_path,
            args.query,
            limit=args.limit,
            alias_json=context_alias_json,
        )
        mode_used = "context"
        if args.json:
            print(
                json.dumps(
                    {
                        "mode_used": mode_used,
                        "query": args.query,
                        "context": context,
                        "results": [
                            {
                                "id": r.id,
                                "name": r.name,
                                "description": r.description,
                                "worth_score": r.worth_score,
                                "quality_score": r.quality_score,
                                "combined_score": r.score,
                                "confidence": r.confidence,
                                "why_selected": r.why_selected,
                                "source_kind": r.source_kind,
                                "kind": r.kind,
                                "phases": r.phases,
                                "tools": r.tools,
                                "match_terms": r.match_terms,
                                "score_breakdown": r.score_breakdown,
                            }
                            for r in ctx_results
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
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        print(f"mode: {mode_used}")
        print(f"context.phase: {context.get('phase')!r}  strong={bool(context.get('strong_phase'))}")
        if context.get("tools"):
            print(f"context.tools: {', '.join(context['tools'])}")
        if context.get("alias_hits"):
            aliases = ", ".join(h.get("skill", "") for h in context["alias_hits"] if isinstance(h, dict))
            if aliases:
                print(f"context.alias_hits: {aliases}")
        print("")
        for i, r in enumerate(ctx_results, start=1):
            terms = f" (match: {', '.join(r.match_terms)})" if r.match_terms else ""
            print(
                f"{i}. {r.name}  [score={r.score:.3f}, confidence={r.confidence:.3f}, worth={r.worth_score}/100, quality={r.quality_score}/100]{terms}"
            )
            print(f"   id: {r.id}")
            print(f"   why: {r.why_selected}")
            if r.description:
                print(f"   {r.description}")
            print("")
        return 0

    results = search_db(
        db_path,
        args.query,
        limit=args.limit,
        alias_json=alias_json,
        collapse_aliases=not bool(args.no_alias_collapse),
    )
    if args.json:
        print(
            json.dumps(
                {
                    "mode_used": mode_used,
                    "query": args.query,
                    "context": query_context,
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
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    for i, r in enumerate(results, start=1):
        terms = f" (match: {', '.join(r.match_terms)})" if r.match_terms else ""
        print(f"{i}. {r.name}  [worth={r.worth_score}/100, quality={r.quality_score}/100]{terms}")
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
        print(f"{i}. {r.name}  [quality={r.quality_score}/100, worth={r.worth_score}/100]")
        print(f"   id: {r.id}")
        if r.description:
            print(f"   {r.description}")
        print("")
    return 0


def cmd_context_search(args: argparse.Namespace) -> int:
    db_path = Path(args.db).expanduser().resolve()
    if not _ensure_db(db_path):
        return 2

    alias_json = Path(args.alias_json).expanduser().resolve() if args.alias_json else None
    context, results, alternatives = context_search_db(
        db_path,
        args.query,
        limit=args.limit,
        alias_json=alias_json,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "query": args.query,
                    "context": context,
                    "results": [
                        {
                            "id": r.id,
                            "name": r.name,
                            "description": r.description,
                            "worth_score": r.worth_score,
                            "quality_score": r.quality_score,
                            "score": round(r.score, 3),
                            "confidence": round(r.confidence, 3),
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
                            "score": round(r.score, 3),
                            "why_selected": r.why_selected,
                        }
                        for r in alternatives
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    print(f"query: {args.query}")
    print(
        "context: "
        f"phase={context.get('phase') or '-'} "
        f"strong_phase={bool(context.get('strong_phase'))} "
        f"tools={','.join(context.get('tools') or []) or '-'}"
    )
    print("")

    for i, r in enumerate(results, start=1):
        print(
            f"{i}. {r.name}  "
            f"[score={r.score:.2f}, conf={r.confidence:.2f}, "
            f"quality={r.quality_score}/100, worth={r.worth_score}/100]"
        )
        print(f"   id: {r.id}")
        print(f"   type: {r.kind} / {r.source_kind}")
        print(f"   why: {r.why_selected}")
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


def cmd_stats(args: argparse.Namespace) -> int:
    skills_json = Path(args.skills_json).expanduser().resolve()
    if not skills_json.exists():
        print(f"[ERROR] Missing skills.json: {skills_json}. Run: python -m awesome_skills build", file=sys.stderr)
        return 2

    data = json.loads(skills_json.read_text(encoding="utf-8", errors="replace"))
    skills = data.get("skills", [])
    if not isinstance(skills, list):
        print(f"[ERROR] Invalid skills.json (missing skills[]): {skills_json}", file=sys.stderr)
        return 2

    by_root: dict[str, int] = {}
    by_tag: dict[str, int] = {}
    buckets = {"0-19": 0, "20-39": 0, "40-59": 0, "60-79": 0, "80-100": 0}

    for s in skills:
        root = str(s.get("root_label") or s.get("root") or "unknown")
        by_root[root] = by_root.get(root, 0) + 1

        score = 0
        try:
            score = int(s.get("worth_score") or 0)
        except Exception:
            score = 0

        if score < 20:
            buckets["0-19"] += 1
        elif score < 40:
            buckets["20-39"] += 1
        elif score < 60:
            buckets["40-59"] += 1
        elif score < 80:
            buckets["60-79"] += 1
        else:
            buckets["80-100"] += 1

        tags = s.get("tags") or []
        if isinstance(tags, list):
            for t in tags:
                tt = str(t).strip().lower()
                if not tt:
                    continue
                by_tag[tt] = by_tag.get(tt, 0) + 1

    payload = {
        "skills_json": str(skills_json),
        "total": len(skills),
        "by_root": dict(sorted(by_root.items(), key=lambda kv: (-kv[1], kv[0]))),
        "by_tag_top": [
            {"tag": k, "count": v} for k, v in sorted(by_tag.items(), key=lambda kv: (-kv[1], kv[0]))[:50]
        ],
        "worth_score_buckets": buckets,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"total_skills: {payload['total']}")
    print("")
    print("By root_label:")
    for k, v in payload["by_root"].items():
        print(f"- {k}: {v}")
    print("")
    print("Worth score buckets:")
    for k, v in buckets.items():
        print(f"- {k}: {v}")
    print("")
    print("Top tags:")
    for row in payload["by_tag_top"][:30]:
        print(f"- {row['tag']}: {row['count']}")
    return 0


def cmd_invent(args: argparse.Namespace) -> int:
    skills_json = Path(args.skills_json).expanduser().resolve()
    if not skills_json.exists():
        print(f"[ERROR] Missing skills.json: {skills_json}. Run: python -m awesome_skills build", file=sys.stderr)
        return 2

    try:
        skills = load_skills_json(skills_json)
    except Exception as e:  # noqa: BLE001 - user-facing CLI should not traceback for bad input.
        print(f"[ERROR] Failed to load skills.json: {e}", file=sys.stderr)
        return 2

    candidates = propose_novel_skills(
        skills=skills,
        limit=int(args.limit),
        exclude_domains=list(args.exclude_domain or []),
    )

    written: list[str] = []
    if args.write:
        out_dir = Path(args.out_dir).expanduser().resolve()
        paths = write_skill_stubs(candidates, out_dir=out_dir)
        written = [str(p) for p in paths]

    payload = {
        "skills_json": str(skills_json),
        "count": len(candidates),
        "exclude_domains": list(args.exclude_domain or []),
        "write": bool(args.write),
        "out_dir": str(Path(args.out_dir).expanduser().resolve()) if args.write else str(args.out_dir),
        "candidates": [c.to_json() for c in candidates],
        "written": written,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not candidates:
        print("No novel candidates found for the current corpus/exclusions.")
        return 0

    print(f"novel_candidates: {len(candidates)}")
    if args.exclude_domain:
        print(f"exclude_domains: {', '.join(args.exclude_domain)}")
    print("")
    for i, c in enumerate(candidates, start=1):
        print(f"{i}. {c.name}  [{c.score:.2f}] ({c.kind})")
        print(f"   title: {c.title}")
        print(f"   rationale: {c.rationale}")
        print("")

    if written:
        print("written_stubs:")
        for w in written:
            print(f"- {w}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    skills_json = Path(args.skills_json).expanduser().resolve()
    cards_dir = None if args.no_cards else Path(args.cards_dir).expanduser().resolve()
    alias_json = None if args.no_alias_check else Path(args.alias_json).expanduser().resolve()
    readme_path = None if args.no_readme_check else Path(args.readme).expanduser().resolve()
    mcp_server_path = None if args.no_mcp_check else Path(args.mcp_server).expanduser().resolve()

    report = verify_artifacts(
        skills_json=skills_json,
        cards_dir=cards_dir,
        alias_json=alias_json,
        readme_path=readme_path,
        mcp_server_path=mcp_server_path,
        check_readme_examples=not bool(args.no_readme_check),
        check_mcp_policy=not bool(args.no_mcp_check),
        max_findings=int(args.max_findings),
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"ok: {bool(report.get('ok'))}")
        print(f"errors: {int(report.get('error_count', 0))}")
        print(f"warnings: {int(report.get('warning_count', 0))}")
        checked = report.get("checked") or {}
        print("")
        print("checked:")
        for k in (
            "skills_json",
            "cards_dir",
            "alias_json",
            "alias_status",
            "readme_path",
            "mcp_server_path",
            "total_skills",
            "check_readme_examples",
            "check_mcp_policy",
            "max_findings",
        ):
            print(f"- {k}: {checked.get(k)}")
        findings = report.get("findings") or []
        if findings:
            print("")
            print("findings:")
            for row in findings:
                sev = str(row.get("severity") or "warning").upper()
                code = str(row.get("code") or "UNKNOWN")
                msg = str(row.get("message") or "")
                skill_id = row.get("skill_id")
                path = row.get("path")
                parts = [f"[{sev}] {code}: {msg}"]
                if skill_id:
                    parts.append(f"id={skill_id}")
                if path:
                    parts.append(f"path={path}")
                print(f"- {' | '.join(parts)}")
        if bool(report.get("findings_truncated")):
            print("")
            print("note: findings list truncated; increase --max-findings for full output")

    has_errors = int(report.get("error_count", 0)) > 0
    has_warnings = int(report.get("warning_count", 0)) > 0
    if has_errors:
        return 1
    if args.strict and has_warnings:
        return 1
    return 0


def cmd_curate(args: argparse.Namespace) -> int:
    skills_json = Path(args.skills_json).expanduser().resolve()
    cards_dir = Path(args.cards_dir).expanduser().resolve()
    aliases_json = Path(args.aliases_json).expanduser().resolve()

    try:
        report = curate_artifacts(
            skills_json=skills_json,
            cards_dir=cards_dir,
            aliases_json=aliases_json,
            write=bool(args.write),
            fix_level=str(args.fix_level),
        )
    except Exception as e:  # noqa: BLE001 - user-facing CLI should remain structured on failures.
        print(f"[ERROR] curate failed: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    print(f"write: {bool(report.get('write'))}")
    print(f"skills_total: {int(report.get('skills_total', 0))}")
    print(f"mcp_total: {int(report.get('mcp_total', 0))}")
    print(f"mcp_use_when_filled: {int(report.get('mcp_use_when_filled', 0))}")
    print(f"mcp_workflow_filled: {int(report.get('mcp_workflow_filled', 0))}")
    print(f"general_use_when_filled: {int(report.get('general_use_when_filled', 0))}")
    print(f"general_workflow_filled: {int(report.get('general_workflow_filled', 0))}")
    print(f"tags_normalized: {int(report.get('tags_normalized', 0))}")
    print(f"cards_checked: {int(report.get('cards_checked', 0))}")
    print(f"cards_patched_score: {int(report.get('cards_patched_score', 0))}")
    print(f"duplicate_name_keys: {int(report.get('duplicate_name_keys', 0))}")
    print(f"duplicate_skills_total: {int(report.get('duplicate_skills_total', 0))}")
    print(f"alias_entries: {int(report.get('alias_entries', 0))}")
    print("")
    print(f"skills_json: {report.get('skills_json')}")
    print(f"cards_dir: {report.get('cards_dir')}")
    print(f"aliases_json: {report.get('aliases_json')}")
    print(f"fix_level: {report.get('fix_level')}")
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    db_path = Path(args.db).expanduser().resolve()
    skills_json = Path(args.skills_json).expanduser().resolve()
    benchmark_json = Path(args.benchmark).expanduser().resolve()
    alias_json = None if args.no_alias_collapse else Path(args.alias_json).expanduser().resolve()

    try:
        report = run_benchmark(
            db_path=db_path,
            skills_json=skills_json,
            alias_json=alias_json,
            benchmark_json=benchmark_json,
            collapse_aliases=not bool(args.no_alias_collapse),
        )
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] bench failed: {e}", file=sys.stderr)
        return 2

    metrics = report.get("metrics") or {}
    hit = float(metrics.get("hit_rate_at_k") or 0.0)
    mrr = float(metrics.get("mrr") or 0.0)
    ndcg = float(metrics.get("mean_ndcg_at_k") or 0.0)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"query_count: {int(report.get('query_count', 0))}")
        print(f"evaluated_count: {int(report.get('evaluated_count', 0))}")
        print(f"skipped_count: {int(report.get('skipped_count', 0))}")
        print(f"hit_rate_at_k: {hit:.4f}")
        print(f"mrr: {mrr:.4f}")
        print(f"mean_ndcg_at_k: {ndcg:.4f}")

    if args.min_hit_rate is not None and hit < float(args.min_hit_rate):
        return 1
    if args.min_mrr is not None and mrr < float(args.min_mrr):
        return 1
    if args.min_ndcg is not None and ndcg < float(args.min_ndcg):
        return 1
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
    ps.add_argument("--alias-json", default="dist/name_aliases.json", help="Alias mapping for canonical collapse.")
    ps.add_argument("--no-alias-collapse", action="store_true", help="Disable alias-based dedupe of search results.")
    ps.add_argument(
        "--strategy",
        default="classic",
        choices=("auto", "classic", "context"),
        help="Search strategy (default: classic). auto routes to context mode for strong phase/tool/alias queries.",
    )
    ps.add_argument(
        "--context-alias-json",
        default="sources/compat_aliases.json",
        help="Phrase alias rules used by --strategy context/auto.",
    )
    ps.add_argument("--limit", type=int, default=10, help="Max results.")
    ps.add_argument("--json", action="store_true", help="JSON output.")
    ps.set_defaults(func=cmd_search)

    pcs = sub.add_parser("context-search", help="Context-aware search with phase/tool/source ranking.")
    pcs.add_argument("query", help="User query.")
    pcs.add_argument("--db", default="dist/awesome_skills.sqlite", help="Path to SQLite DB.")
    pcs.add_argument(
        "--alias-json",
        default="sources/compat_aliases.json",
        help="Optional alias mapping for phrase->skill boosts.",
    )
    pcs.add_argument("--limit", type=int, default=10, help="Max results.")
    pcs.add_argument("--json", action="store_true", help="JSON output.")
    pcs.set_defaults(func=cmd_context_search)

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

    pst = sub.add_parser("stats", help="Summarize the indexed corpus (counts, tags, worth_score buckets).")
    pst.add_argument("--skills-json", default="dist/skills.json", help="Path to dist/skills.json.")
    pst.add_argument("--json", action="store_true", help="JSON output.")
    pst.set_defaults(func=cmd_stats)

    pi = sub.add_parser("invent", help="Propose novel skills by mining corpus coverage gaps.")
    pi.add_argument("--skills-json", default="dist/skills.json", help="Path to dist/skills.json.")
    pi.add_argument("--limit", type=int, default=20, help="Max candidates to return.")
    pi.add_argument(
        "--exclude-domain",
        action="append",
        default=[],
        help="Domain slug to exclude (repeatable), e.g. --exclude-domain hytale",
    )
    pi.add_argument("--write", action="store_true", help="Write generated SKILL.md stubs.")
    pi.add_argument(
        "--out-dir",
        default="skillpacks/novel-synthesized",
        help="Output directory for --write (default: skillpacks/novel-synthesized).",
    )
    pi.add_argument("--json", action="store_true", help="JSON output.")
    pi.set_defaults(func=cmd_invent)

    pv = sub.add_parser("verify", help="Run deterministic quality and policy checks over the database artifacts.")
    pv.add_argument("--skills-json", default="dist/skills.json", help="Path to dist/skills.json.")
    pv.add_argument("--cards-dir", default="dist/cards", help="Path to generated card directory.")
    pv.add_argument("--no-cards", action="store_true", help="Skip card presence/content checks.")
    pv.add_argument(
        "--alias-json",
        default="dist/name_aliases.json",
        help="Path to alias metadata (auto-used if file exists).",
    )
    pv.add_argument("--no-alias-check", action="store_true", help="Skip alias-aware duplicate-name checks.")
    pv.add_argument("--readme", default="README.md", help="Path to README for MCP example checks.")
    pv.add_argument("--no-readme-check", action="store_true", help="Skip README MCP tool example checks.")
    pv.add_argument(
        "--mcp-server",
        default="awesome_skills/mcp_server.py",
        help="Path to mcp_server.py for policy checks.",
    )
    pv.add_argument("--no-mcp-check", action="store_true", help="Skip MCP tool annotation/policy checks.")
    pv.add_argument("--max-findings", type=int, default=500, help="Maximum findings to return.")
    pv.add_argument("--strict", action="store_true", help="Treat warnings as failures (exit code 1).")
    pv.add_argument("--json", action="store_true", help="JSON output.")
    pv.set_defaults(func=cmd_verify)

    pc = sub.add_parser("curate", help="Curate generated artifacts and emit alias metadata.")
    pc.add_argument("--skills-json", default="dist/skills.json", help="Path to dist/skills.json.")
    pc.add_argument("--cards-dir", default="dist/cards", help="Path to generated card directory.")
    pc.add_argument(
        "--aliases-json",
        default="dist/name_aliases.json",
        help="Where to write alias metadata (with --write).",
    )
    pc.add_argument(
        "--fix-level",
        choices=("safe", "aggressive"),
        default="safe",
        help="Fix strategy: safe (targeted) or aggressive (broader autofill/normalization).",
    )
    pc.add_argument("--write", action="store_true", help="Persist curated artifacts.")
    pc.add_argument("--json", action="store_true", help="JSON output.")
    pc.set_defaults(func=cmd_curate)

    pbench = sub.add_parser("bench", help="Run retrieval benchmark (hit@k, MRR, nDCG).")
    pbench.add_argument("--db", default="dist/awesome_skills.sqlite", help="Path to SQLite DB.")
    pbench.add_argument("--skills-json", default="dist/skills.json", help="Path to skills.json.")
    pbench.add_argument(
        "--benchmark",
        default="sources/benchmark_queries.json",
        help="Path to benchmark query spec JSON.",
    )
    pbench.add_argument("--alias-json", default="dist/name_aliases.json", help="Alias mapping for canonical collapse.")
    pbench.add_argument("--no-alias-collapse", action="store_true", help="Disable alias-based dedupe for benchmark runs.")
    pbench.add_argument("--min-hit-rate", type=float, default=None, help="Fail if hit_rate_at_k drops below threshold.")
    pbench.add_argument("--min-mrr", type=float, default=None, help="Fail if MRR drops below threshold.")
    pbench.add_argument("--min-ndcg", type=float, default=None, help="Fail if mean nDCG drops below threshold.")
    pbench.add_argument("--json", action="store_true", help="JSON output.")
    pbench.set_defaults(func=cmd_bench)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

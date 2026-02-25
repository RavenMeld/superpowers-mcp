#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from awesome_skills.db import context_search_db


def _load_queries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    queries = data.get("queries", [])
    if not isinstance(queries, list):
        return []
    out: list[dict] = []
    for item in queries:
        if not isinstance(item, dict):
            continue
        query = str(item.get("query") or "").strip()
        expects = item.get("expects_any") or []
        expects_any = [str(x).strip().lower() for x in expects if str(x).strip()]
        if query:
            out.append({"query": query, "expects_any": expects_any})
    return out


def _top_names(results) -> list[str]:
    return [r.name.strip().lower() for r in results]


def main() -> int:
    p = argparse.ArgumentParser(description="Benchmark awesome_skills context-search relevance + latency.")
    p.add_argument("--db", required=True, help="Path to awesome_skills.sqlite")
    p.add_argument("--queries", required=True, help="JSON file with benchmark queries")
    p.add_argument("--alias-json", default="sources/compat_aliases.json", help="Alias mapping file")
    p.add_argument("--limit", type=int, default=5, help="Top-N results to fetch")
    p.add_argument("--json", action="store_true", help="Emit JSON only")
    p.add_argument("--max-p95-ms", type=float, default=None, help="Fail if p95 exceeds threshold")
    p.add_argument("--min-hit-at-1", type=float, default=None, help="Fail if hit@1 below threshold")
    p.add_argument("--min-hit-at-3", type=float, default=None, help="Fail if hit@3 below threshold")
    args = p.parse_args()

    db_path = Path(args.db).expanduser().resolve()
    queries_path = Path(args.queries).expanduser().resolve()
    alias_json = Path(args.alias_json).expanduser().resolve() if args.alias_json else None

    items = _load_queries(queries_path)
    if not items:
        raise SystemExit("No valid benchmark queries found")

    latencies_ms: list[float] = []
    hit1 = 0
    hit3 = 0
    detailed: list[dict] = []

    for item in items:
        query = item["query"]
        expects_any = item["expects_any"]

        t0 = time.perf_counter()
        _ctx, results, _alts = context_search_db(
            db_path,
            query,
            limit=args.limit,
            alias_json=alias_json,
        )
        dt_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(dt_ms)

        names = _top_names(results)
        top1_name = names[0] if names else ""
        top3_names = names[:3]

        is_hit1 = True
        is_hit3 = True
        if expects_any:
            expect_set = set(expects_any)
            is_hit1 = top1_name in expect_set
            is_hit3 = bool(expect_set.intersection(top3_names))

        if is_hit1:
            hit1 += 1
        if is_hit3:
            hit3 += 1

        detailed.append(
            {
                "query": query,
                "expects_any": expects_any,
                "top1": top1_name,
                "top3": top3_names,
                "hit_at_1": is_hit1,
                "hit_at_3": is_hit3,
                "latency_ms": round(dt_ms, 3),
            }
        )

    total = len(items)
    hit_at_1 = hit1 / total
    hit_at_3 = hit3 / total

    p50 = statistics.median(latencies_ms)
    sorted_lats = sorted(latencies_ms)
    p95_idx = max(0, min(len(sorted_lats) - 1, int(round(0.95 * (len(sorted_lats) - 1)))))
    p95 = sorted_lats[p95_idx]

    summary = {
        "total_queries": total,
        "hit_at_1": round(hit_at_1, 4),
        "hit_at_3": round(hit_at_3, 4),
        "latency_ms": {
            "p50": round(p50, 3),
            "p95": round(p95, 3),
            "max": round(max(latencies_ms), 3),
        },
    }

    payload = {
        "summary": summary,
        "details": detailed,
    }

    fail = False
    fail_reasons: list[str] = []
    if args.max_p95_ms is not None and p95 > args.max_p95_ms:
        fail = True
        fail_reasons.append(f"p95 {p95:.3f}ms > max {args.max_p95_ms:.3f}ms")
    if args.min_hit_at_1 is not None and hit_at_1 < args.min_hit_at_1:
        fail = True
        fail_reasons.append(f"hit@1 {hit_at_1:.4f} < min {args.min_hit_at_1:.4f}")
    if args.min_hit_at_3 is not None and hit_at_3 < args.min_hit_at_3:
        fail = True
        fail_reasons.append(f"hit@3 {hit_at_3:.4f} < min {args.min_hit_at_3:.4f}")

    if args.json:
        if fail:
            payload["failed"] = True
            payload["fail_reasons"] = fail_reasons
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Context Search Benchmark")
        print(f"- total_queries: {summary['total_queries']}")
        print(f"- hit@1: {summary['hit_at_1']:.4f}")
        print(f"- hit@3: {summary['hit_at_3']:.4f}")
        print(
            "- latency_ms: "
            f"p50={summary['latency_ms']['p50']:.3f} "
            f"p95={summary['latency_ms']['p95']:.3f} "
            f"max={summary['latency_ms']['max']:.3f}"
        )
        if fail_reasons:
            print("- thresholds: FAIL")
            for reason in fail_reasons:
                print(f"  - {reason}")
        else:
            print("- thresholds: PASS")

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())

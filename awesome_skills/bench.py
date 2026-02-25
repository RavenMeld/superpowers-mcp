from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .db import search_db
from .util import slugify


@dataclass(frozen=True)
class QueryMetrics:
    query: str
    k: int
    gold_ids: list[str]
    top_ids: list[str]
    hit_at_k: float
    reciprocal_rank: float
    ndcg_at_k: float
    rank_first_hit: int | None
    skipped: bool
    skip_reason: str | None

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid json root in {path} (expected object)")
    return data


def _load_alias_canonical(alias_json: Path | None) -> dict[str, str]:
    if alias_json is None:
        return {}
    path = alias_json.expanduser().resolve()
    if not path.exists():
        return {}
    data = _read_json(path)
    aliases = data.get("aliases") or []
    if not isinstance(aliases, list):
        return {}
    out: dict[str, str] = {}
    for row in aliases:
        if not isinstance(row, dict):
            continue
        key = slugify(str(row.get("name_key") or ""))
        canonical = str(row.get("canonical_id") or "").strip()
        if key and canonical:
            out[key] = canonical
    return out


def _skills_index(skills_json: Path) -> dict[str, list[dict[str, Any]]]:
    data = _read_json(skills_json)
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("skills.json missing skills[] list")
    by_key: dict[str, list[dict[str, Any]]] = {}
    for s in skills:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("id") or "").strip()
        name = str(s.get("name") or "").strip()
        if not sid or not name:
            continue
        key = slugify(name)
        by_key.setdefault(key, []).append(s)
    for key in list(by_key.keys()):
        by_key[key].sort(
            key=lambda s: (
                -int(s.get("quality_score") or 0),
                -int(s.get("worth_score") or 0),
                str(s.get("id") or ""),
            )
        )
    return by_key


def _dcg(binary_rels: list[int]) -> float:
    total = 0.0
    for i, rel in enumerate(binary_rels):
        if rel <= 0:
            continue
        total += float(rel) / math.log2(i + 2)
    return total


def _resolve_gold_ids(
    *,
    row: dict[str, Any],
    by_name_key: dict[str, list[dict[str, Any]]],
    canonical_by_key: dict[str, str],
) -> tuple[list[str], str | None]:
    gold_ids: list[str] = []
    expected_ids = row.get("expected_ids") or []
    if isinstance(expected_ids, list):
        for x in expected_ids:
            sid = str(x).strip()
            if sid:
                gold_ids.append(sid)

    expected_name_keys = row.get("expected_name_keys") or []
    if isinstance(expected_name_keys, list):
        for x in expected_name_keys:
            key = slugify(str(x))
            if not key:
                continue
            canonical = canonical_by_key.get(key)
            if canonical:
                gold_ids.append(canonical)
                continue
            candidates = by_name_key.get(key) or []
            if candidates:
                gold_ids.append(str(candidates[0].get("id") or ""))

    out = [x for x in gold_ids if x]
    dedup: list[str] = []
    seen: set[str] = set()
    for sid in out:
        if sid in seen:
            continue
        seen.add(sid)
        dedup.append(sid)
    if not dedup:
        return [], "no_gold_ids_resolved"
    return dedup, None


def run_benchmark(
    *,
    db_path: Path,
    skills_json: Path,
    alias_json: Path | None,
    benchmark_json: Path,
    collapse_aliases: bool = True,
) -> dict[str, Any]:
    bench = _read_json(benchmark_json)
    queries = bench.get("queries")
    if not isinstance(queries, list) or not queries:
        raise ValueError(f"benchmark file missing queries[]: {benchmark_json}")
    default_k = int(bench.get("k") or 10)

    by_name_key = _skills_index(skills_json)
    canonical_by_key = _load_alias_canonical(alias_json)

    per_query: list[QueryMetrics] = []
    for row in queries:
        if not isinstance(row, dict):
            continue
        query = str(row.get("query") or "").strip()
        if not query:
            continue
        k = int(row.get("k") or default_k)
        if k < 1:
            k = 1
        if k > 100:
            k = 100

        gold_ids, skip_reason = _resolve_gold_ids(
            row=row,
            by_name_key=by_name_key,
            canonical_by_key=canonical_by_key,
        )
        if not gold_ids:
            per_query.append(
                QueryMetrics(
                    query=query,
                    k=k,
                    gold_ids=[],
                    top_ids=[],
                    hit_at_k=0.0,
                    reciprocal_rank=0.0,
                    ndcg_at_k=0.0,
                    rank_first_hit=None,
                    skipped=True,
                    skip_reason=skip_reason,
                )
            )
            continue

        results = search_db(
            db_path=db_path,
            query=query,
            limit=k,
            alias_json=alias_json,
            collapse_aliases=collapse_aliases,
        )
        top_ids = [r.id for r in results[:k]]
        gold_set = set(gold_ids)

        rank_first_hit = None
        for i, sid in enumerate(top_ids, start=1):
            if sid in gold_set:
                rank_first_hit = i
                break

        hit = 1.0 if rank_first_hit is not None else 0.0
        rr = 1.0 / float(rank_first_hit) if rank_first_hit is not None else 0.0
        rels = [1 if sid in gold_set else 0 for sid in top_ids]
        dcg = _dcg(rels)
        idcg = _dcg([1] * min(len(gold_set), k))
        ndcg = (dcg / idcg) if idcg > 0 else 0.0

        per_query.append(
            QueryMetrics(
                query=query,
                k=k,
                gold_ids=gold_ids,
                top_ids=top_ids,
                hit_at_k=hit,
                reciprocal_rank=rr,
                ndcg_at_k=ndcg,
                rank_first_hit=rank_first_hit,
                skipped=False,
                skip_reason=None,
            )
        )

    evaluated = [q for q in per_query if not q.skipped]
    skipped = [q for q in per_query if q.skipped]
    n_eval = len(evaluated)
    hit_rate = (sum(q.hit_at_k for q in evaluated) / n_eval) if n_eval else 0.0
    mrr = (sum(q.reciprocal_rank for q in evaluated) / n_eval) if n_eval else 0.0
    mean_ndcg = (sum(q.ndcg_at_k for q in evaluated) / n_eval) if n_eval else 0.0

    return {
        "ok": True,
        "benchmark_json": str(benchmark_json),
        "db_path": str(db_path),
        "skills_json": str(skills_json),
        "alias_json": str(alias_json) if alias_json else None,
        "collapse_aliases": bool(collapse_aliases),
        "query_count": len(per_query),
        "evaluated_count": n_eval,
        "skipped_count": len(skipped),
        "metrics": {
            "hit_rate_at_k": round(hit_rate, 6),
            "mrr": round(mrr, 6),
            "mean_ndcg_at_k": round(mean_ndcg, 6),
        },
        "queries": [q.to_json() for q in per_query],
    }


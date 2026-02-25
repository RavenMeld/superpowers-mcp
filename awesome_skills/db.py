from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .condense import SkillRecord
from .context import classify_skill, detect_source_kind, parse_query_context
from .util import keywords_from_query


SCHEMA_VERSION = 2


def _connect(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def build_db(db_path: Path, records: list[SkillRecord], card_by_id: dict[str, str]) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()

    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=NORMAL;")

        cur.execute(
            """
            CREATE TABLE meta (
              key TEXT PRIMARY KEY,
              value TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE skills (
              id TEXT PRIMARY KEY,
              name TEXT NOT NULL,
              description TEXT NOT NULL,
              root_label TEXT NOT NULL,
              source_path TEXT NOT NULL,
              worth_score INTEGER NOT NULL,
              quality_score INTEGER NOT NULL,
              tags TEXT NOT NULL,
              use_when TEXT NOT NULL,
              workflow TEXT NOT NULL,
              features_json TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE VIRTUAL TABLE skills_fts USING fts5(
              id UNINDEXED,
              name,
              description,
              tags,
              use_when,
              workflow,
              content,
              tokenize='unicode61'
            );
            """
        )

        cur.execute(
            "INSERT INTO meta(key, value) VALUES (?, ?), (?, ?);",
            ("schema_version", str(SCHEMA_VERSION), "count", str(len(records))),
        )

        for r in records:
            tags = ",".join(r.tags)
            use_when = "\n".join(r.use_when)
            workflow = "\n".join(r.workflow)
            features_json = json.dumps(
                {
                    "has_description": r.features.has_description,
                    "has_use_when": r.features.has_use_when,
                    "has_workflow": r.features.has_workflow,
                    "code_fence_count": r.features.code_fence_count,
                    "has_scripts": r.features.has_scripts,
                    "has_references": r.features.has_references,
                    "has_assets": r.features.has_assets,
                    "word_count": r.features.word_count,
                },
                sort_keys=True,
            )
            cur.execute(
                """
                INSERT INTO skills(id, name, description, root_label, source_path, worth_score, quality_score, tags, use_when, workflow, features_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    r.id,
                    r.name,
                    r.description,
                    r.root_label,
                    r.source_path,
                    int(r.worth_score),
                    int(r.quality_score),
                    tags,
                    use_when,
                    workflow,
                    features_json,
                ),
            )
            card_md = card_by_id.get(r.id, "")
            cur.execute(
                """
                INSERT INTO skills_fts(id, name, description, tags, use_when, workflow, content)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (r.id, r.name, r.description, tags, use_when, workflow, card_md),
            )

        conn.commit()
    finally:
        conn.close()


@dataclass(frozen=True)
class SearchResult:
    id: str
    name: str
    description: str
    worth_score: int
    quality_score: int
    combined_score: float
    match_terms: list[str]


@dataclass(frozen=True)
class ContextSearchResult:
    id: str
    name: str
    description: str
    worth_score: int
    quality_score: int
    score: float
    confidence: float
    why_selected: str
    match_terms: list[str]
    source_kind: str
    kind: str
    phases: list[str]
    tools: list[str]
    score_breakdown: dict[str, float]


def _safe_fts_query(query: str) -> str:
    """
    Convert a plain-text query to a conservative FTS5 query.

    FTS5 treats some punctuation as operators. The main offender for our use-case
    is `-` inside tokens (e.g. `mcp-builder`), which can trigger confusing
    "no such column" errors unless quoted.
    """
    toks = []
    for t in keywords_from_query(query):
        if "-" in t:
            toks.append(f"\"{t}\"")
        else:
            toks.append(t)
    return " ".join(toks) if toks else query


def _or_fts_query(query: str) -> str:
    """
    Build an OR-based FTS query for broader recall in context-search.
    """
    terms: list[str] = []
    for t in keywords_from_query(query):
        if "-" in t:
            terms.append(f'"{t}"')
        else:
            terms.append(t)
    if not terms:
        return _safe_fts_query(query)
    return " OR ".join(terms)


def _load_alias_map(alias_json: Path | None) -> dict[str, str]:
    if alias_json is None:
        return {}
    path = alias_json.expanduser().resolve()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    aliases = data.get("aliases")
    if not isinstance(aliases, list):
        return {}

    out: dict[str, str] = {}
    for row in aliases:
        if not isinstance(row, dict):
            continue
        canonical = str(row.get("canonical_id") or "").strip()
        members = row.get("member_ids") or []
        if not canonical or not isinstance(members, list):
            continue
        for mid in members:
            sid = str(mid).strip()
            if sid:
                out[sid] = canonical
    return out


def _fetch_skill_row(conn: sqlite3.Connection, skill_id: str) -> tuple[str, str, int, int] | None:
    cur = conn.cursor()
    if _skills_has_quality_score(conn):
        row = cur.execute(
            "SELECT name, description, worth_score, quality_score FROM skills WHERE id = ?;",
            (skill_id,),
        ).fetchone()
    else:
        row = cur.execute(
            "SELECT name, description, worth_score, worth_score AS quality_score FROM skills WHERE id = ?;",
            (skill_id,),
        ).fetchone()
    if row is None:
        return None
    return (str(row["name"]), str(row["description"]), int(row["worth_score"]), int(row["quality_score"]))


def _skills_has_quality_score(conn: sqlite3.Connection) -> bool:
    cur = conn.cursor()
    rows = cur.execute("PRAGMA table_info(skills);").fetchall()
    for row in rows:
        # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
        if str(row["name"]) == "quality_score":
            return True
    return False


def _merge_terms(a: list[str], b: list[str], max_terms: int = 8) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for t in list(a) + list(b):
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
        if len(out) >= max_terms:
            break
    return out


def _collapse_alias_results(
    *,
    conn: sqlite3.Connection,
    results: list[SearchResult],
    alias_map: dict[str, str],
) -> list[SearchResult]:
    if not alias_map:
        return results
    canonical_cache: dict[str, tuple[str, str, int, int] | None] = {}
    by_canonical: dict[str, SearchResult] = {}

    for r in results:
        canonical_id = alias_map.get(r.id, r.id)
        existing = by_canonical.get(canonical_id)
        if existing is None:
            if canonical_id != r.id:
                meta = canonical_cache.get(canonical_id)
                if meta is None:
                    meta = _fetch_skill_row(conn, canonical_id)
                    canonical_cache[canonical_id] = meta
                if meta is not None:
                    name, desc, worth, quality = meta
                    by_canonical[canonical_id] = SearchResult(
                        id=canonical_id,
                        name=name,
                        description=desc,
                        worth_score=worth,
                        quality_score=quality,
                        combined_score=r.combined_score,
                        match_terms=list(r.match_terms),
                    )
                else:
                    by_canonical[canonical_id] = SearchResult(
                        id=canonical_id,
                        name=r.name,
                        description=r.description,
                        worth_score=r.worth_score,
                        quality_score=r.quality_score,
                        combined_score=r.combined_score,
                        match_terms=list(r.match_terms),
                    )
            else:
                by_canonical[canonical_id] = r
            continue

        if r.combined_score > existing.combined_score:
            by_canonical[canonical_id] = SearchResult(
                id=existing.id,
                name=existing.name,
                description=existing.description,
                worth_score=existing.worth_score,
                quality_score=existing.quality_score,
                combined_score=r.combined_score,
                match_terms=_merge_terms(existing.match_terms, r.match_terms),
            )
        else:
            by_canonical[canonical_id] = SearchResult(
                id=existing.id,
                name=existing.name,
                description=existing.description,
                worth_score=existing.worth_score,
                quality_score=existing.quality_score,
                combined_score=existing.combined_score,
                match_terms=_merge_terms(existing.match_terms, r.match_terms),
            )

    out = list(by_canonical.values())
    out.sort(key=lambda r: r.combined_score, reverse=True)
    return out


def search_db(
    db_path: Path,
    query: str,
    limit: int = 10,
    *,
    alias_json: Path | None = None,
    collapse_aliases: bool = True,
) -> list[SearchResult]:
    """
    Search the SQLite FTS index and re-rank by worth_score + exact-ish matches.
    """
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        has_quality_score = _skills_has_quality_score(conn)
        quality_select = (
            "s.quality_score AS quality_score"
            if has_quality_score
            else "s.worth_score AS quality_score"
        )
        # Pull a larger candidate set then rerank in Python.
        cand_limit = max(50, limit * 10)
        sql = f"""
        SELECT
          s.id AS id,
          s.name AS name,
          s.description AS description,
          s.worth_score AS worth_score,
          {quality_select},
          bm25(skills_fts) AS rank
        FROM skills_fts
        JOIN skills s ON s.id = skills_fts.id
        WHERE skills_fts MATCH ?
        ORDER BY rank
        LIMIT ?;
        """
        try:
            rows = cur.execute(sql, (query, cand_limit)).fetchall()
        except sqlite3.OperationalError:
            rows = cur.execute(sql, (_safe_fts_query(query), cand_limit)).fetchall()

        q_terms = keywords_from_query(query)

        results: list[SearchResult] = []
        for row in rows:
            rid = str(row["id"])
            name = str(row["name"])
            desc = str(row["description"])
            worth = int(row["worth_score"])
            quality = int(row["quality_score"])
            rank = float(row["rank"])

            hay = f"{name}\n{desc}".lower()
            match_terms = [t for t in q_terms if t in hay][:8]

            exact = 1.0 if name.strip().lower() == query.strip().lower() else 0.0
            prefix = 1.0 if name.strip().lower().startswith(query.strip().lower()) else 0.0

            # FTS: lower rank is better. Convert to a bounded score contribution.
            fts_score = 1.0 / (rank + 0.25)  # stable-ish; avoids huge values
            combined = (fts_score * 52.0) + (worth * 0.6) + (quality * 0.9) + (exact * 30.0) + (prefix * 10.0)
            results.append(
                SearchResult(
                    id=rid,
                    name=name,
                    description=desc,
                    worth_score=worth,
                    quality_score=quality,
                    combined_score=combined,
                    match_terms=match_terms,
                )
            )

        results.sort(key=lambda r: r.combined_score, reverse=True)
        if collapse_aliases:
            results = _collapse_alias_results(conn=conn, results=results, alias_map=_load_alias_map(alias_json))
        return results[:limit]
    finally:
        conn.close()


def context_search_db(
    db_path: Path,
    query: str,
    limit: int = 10,
    alias_json: Path | None = None,
) -> tuple[dict[str, Any], list[ContextSearchResult], list[ContextSearchResult]]:
    """
    Context-aware search with:
    - fast lane when phase intent is strong
    - alias boost from compatibility alias map
    - source-priority policy by skill kind
    """
    ctx = parse_query_context(query, alias_json=alias_json)
    alias_skills = {h.skill for h in ctx.alias_hits}
    alias_terms = " ".join(h.skill.replace("-", " ") for h in ctx.alias_hits)
    expanded_query = f"{query} {alias_terms}".strip()

    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        has_quality_score = _skills_has_quality_score(conn)
        quality_select = (
            "s.quality_score AS quality_score"
            if has_quality_score
            else "s.worth_score AS quality_score"
        )
        cand_limit = max(80, limit * 20)

        sql_fts = f"""
        SELECT
          s.id AS id,
          s.name AS name,
          s.description AS description,
          s.worth_score AS worth_score,
          {quality_select},
          s.root_label AS root_label,
          s.source_path AS source_path,
          s.tags AS tags,
          s.use_when AS use_when,
          s.workflow AS workflow,
          bm25(skills_fts) AS rank
        FROM skills_fts
        JOIN skills s ON s.id = skills_fts.id
        WHERE skills_fts MATCH ?
        ORDER BY rank
        LIMIT ?;
        """

        rows: list[sqlite3.Row] = []
        recall_query = _or_fts_query(expanded_query)
        try:
            rows = cur.execute(sql_fts, (recall_query, cand_limit)).fetchall()
        except sqlite3.OperationalError:
            rows = cur.execute(sql_fts, (_safe_fts_query(expanded_query), cand_limit)).fetchall()

        if not rows:
            rows = cur.execute(
                f"""
                SELECT
                  id, name, description, worth_score,
                  {"quality_score" if has_quality_score else "worth_score AS quality_score"},
                  root_label, source_path,
                  tags, use_when, workflow, 999.0 AS rank
                FROM skills
                ORDER BY quality_score DESC, worth_score DESC, name ASC
                LIMIT ?;
                """,
                (cand_limit,),
            ).fetchall()

        q_terms = keywords_from_query(ctx.normalized_query)
        scored: list[ContextSearchResult] = []
        for idx, row in enumerate(rows):
            rid = str(row["id"])
            name = str(row["name"])
            desc = str(row["description"])
            worth = int(row["worth_score"])
            quality = int(row["quality_score"])
            root_label = str(row["root_label"])
            source_path = str(row["source_path"])
            tags = str(row["tags"])
            use_when = str(row["use_when"])
            workflow = str(row["workflow"])
            _rank = float(row["rank"])

            source_kind = detect_source_kind(source_path=source_path, root_label=root_label)
            profile = classify_skill(
                name=name,
                description=desc,
                tags=tags,
                use_when=use_when,
                workflow=workflow,
                source_kind=source_kind,
            )

            if ctx.phase and ctx.strong_phase and ctx.phase not in profile.phases:
                # Fast lane: enforce phase filter when intent is explicit.
                continue

            name_l = name.strip().lower()
            hay = f"{name}\n{desc}\n{tags}\n{use_when}\n{workflow}".lower()
            match_terms = [t for t in q_terms if t in hay][:8]

            fts_component = 60.0 / (idx + 1)
            exact = 1.0 if name_l == ctx.normalized_query else 0.0
            prefix = 1.0 if name_l.startswith(ctx.normalized_query) else 0.0

            phase_bonus = 0.0
            if ctx.phase and ctx.phase in profile.phases:
                phase_bonus = 16.0
            elif ctx.phase and not ctx.strong_phase:
                phase_bonus = -4.0

            tool_overlap = sorted(set(ctx.tools).intersection(profile.tools))
            tool_bonus = float(5 * len(tool_overlap))
            match_bonus = float(4 * len(match_terms))

            alias_bonus = 0.0
            if name_l in alias_skills:
                alias_bonus = 40.0
            elif any(skill.replace("-", " ") in name_l for skill in alias_skills):
                alias_bonus = 16.0

            phase_kind_bonus = 0.0
            if ctx.phase in {"debug", "plan", "review"}:
                if profile.kind == "process":
                    phase_kind_bonus = 10.0
                elif ctx.strong_phase:
                    phase_kind_bonus = -6.0

            source_bonus = 0.0
            if profile.kind == "process":
                if source_kind == "superpowers":
                    source_bonus = 12.0
                elif source_kind == "local":
                    source_bonus = -2.0
            else:
                if source_kind == "local":
                    source_bonus = 8.0
                elif source_kind == "superpowers":
                    source_bonus = -2.0

            score_breakdown = {
                "fts": round(fts_component, 3),
                "worth": round(worth * 0.55, 3),
                "quality": round(quality * 0.55, 3),
                "exact": round(exact * 30.0, 3),
                "prefix": round(prefix * 10.0, 3),
                "phase": round(phase_bonus, 3),
                "tool": round(tool_bonus, 3),
                "match": round(match_bonus, 3),
                "alias": round(alias_bonus, 3),
                "phase_kind": round(phase_kind_bonus, 3),
                "source": round(source_bonus, 3),
            }
            total = sum(score_breakdown.values())

            reasons: list[str] = []
            if phase_bonus > 0 and ctx.phase:
                reasons.append(f"phase={ctx.phase} match")
            if tool_overlap:
                reasons.append(f"tool match: {', '.join(tool_overlap)}")
            if alias_bonus > 0:
                reasons.append("alias rule match")
            if phase_kind_bonus > 0:
                reasons.append("process skill favored for phase intent")
            if source_bonus > 0 and profile.kind == "process" and source_kind == "superpowers":
                reasons.append("preferred superpowers process skill")
            if source_bonus > 0 and profile.kind == "domain" and source_kind == "local":
                reasons.append("preferred local domain skill")
            if not reasons:
                reasons.append("best blended relevance score")

            confidence = max(0.05, min(0.99, total / 180.0))
            scored.append(
                ContextSearchResult(
                    id=rid,
                    name=name,
                    description=desc,
                    worth_score=worth,
                    quality_score=quality,
                    score=total,
                    confidence=confidence,
                    why_selected="; ".join(reasons),
                    match_terms=match_terms,
                    source_kind=source_kind,
                    kind=profile.kind,
                    phases=profile.phases,
                    tools=profile.tools,
                    score_breakdown=score_breakdown,
                )
            )

        scored.sort(key=lambda r: (-r.score, r.name.lower(), r.id))
        top = scored[:limit]
        alternatives = scored[limit : limit + min(3, limit)]
        return ctx.to_json(), top, alternatives
    finally:
        conn.close()


def list_top_worth(db_path: Path, limit: int = 20) -> list[SearchResult]:
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        rows = cur.execute(
            """
            SELECT id, name, description, worth_score
            , quality_score
            FROM skills
            ORDER BY quality_score DESC, worth_score DESC, name ASC
            LIMIT ?;
            """,
            (limit,),
        ).fetchall()
        out: list[SearchResult] = []
        for row in rows:
            out.append(
                SearchResult(
                    id=str(row["id"]),
                    name=str(row["name"]),
                    description=str(row["description"]),
                    worth_score=int(row["worth_score"]),
                    quality_score=int(row["quality_score"]),
                    combined_score=float(row["quality_score"]),
                    match_terms=[],
                )
            )
        return out
    finally:
        conn.close()

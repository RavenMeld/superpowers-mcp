from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .condense import SkillRecord
from .util import keywords_from_query


SCHEMA_VERSION = 1


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
              tokenize='porter'
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
                INSERT INTO skills(id, name, description, root_label, source_path, worth_score, tags, use_when, workflow, features_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    r.id,
                    r.name,
                    r.description,
                    r.root_label,
                    r.source_path,
                    int(r.worth_score),
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
    combined_score: float
    match_terms: list[str]


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


def search_db(db_path: Path, query: str, limit: int = 10) -> list[SearchResult]:
    """
    Search the SQLite FTS index and re-rank by worth_score + exact-ish matches.
    """
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        # Pull a larger candidate set then rerank in Python.
        cand_limit = max(50, limit * 10)
        sql = """
        SELECT
          s.id AS id,
          s.name AS name,
          s.description AS description,
          s.worth_score AS worth_score,
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
            rank = float(row["rank"])

            hay = f"{name}\n{desc}".lower()
            match_terms = [t for t in q_terms if t in hay][:8]

            exact = 1.0 if name.strip().lower() == query.strip().lower() else 0.0
            prefix = 1.0 if name.strip().lower().startswith(query.strip().lower()) else 0.0

            # FTS: lower rank is better. Convert to a bounded score contribution.
            fts_score = 1.0 / (rank + 0.25)  # stable-ish; avoids huge values
            combined = (fts_score * 60.0) + (worth * 0.7) + (exact * 30.0) + (prefix * 10.0)
            results.append(
                SearchResult(
                    id=rid,
                    name=name,
                    description=desc,
                    worth_score=worth,
                    combined_score=combined,
                    match_terms=match_terms,
                )
            )

        results.sort(key=lambda r: r.combined_score, reverse=True)
        return results[:limit]
    finally:
        conn.close()


def list_top_worth(db_path: Path, limit: int = 20) -> list[SearchResult]:
    conn = _connect(db_path)
    try:
        cur = conn.cursor()
        rows = cur.execute(
            """
            SELECT id, name, description, worth_score
            FROM skills
            ORDER BY worth_score DESC, name ASC
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
                    combined_score=float(row["worth_score"]),
                    match_terms=[],
                )
            )
        return out
    finally:
        conn.close()

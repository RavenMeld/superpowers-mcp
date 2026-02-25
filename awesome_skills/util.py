from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    s = text.strip().lower()
    s = _SLUG_RE.sub("-", s).strip("-")
    return s or "skill"


def sha1_hex(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()


def stable_skill_id(name: str, key: str, slug_max: int = 80, hash_len: int = 10) -> str:
    """
    Stable, filename-safe skill id.

    Keeps ids deterministic while bounding slug length to avoid OS filename limits
    when writing `<id>.md` card files.
    """
    slug = slugify(name)
    if len(slug) > slug_max:
        slug = slug[:slug_max].rstrip("-")
    if not slug:
        slug = "skill"
    return f"{slug}--{sha1_hex(key)[:hash_len]}"


def normalize_path(p: str | Path) -> str:
    # Normalize for hashing/ids; keep it stable on this host.
    return os.path.normpath(os.path.abspath(str(p)))


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9][a-z0-9_-]{1,}", text.lower())


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "can",
    "do",
    "for",
    "from",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "so",
    "that",
    "the",
    "then",
    "this",
    "to",
    "use",
    "we",
    "what",
    "when",
    "with",
    "you",
    "your",
}


def keywords_from_query(query: str) -> list[str]:
    toks = [t for t in tokenize(query) if t not in STOPWORDS and len(t) >= 2]
    # Preserve order but unique.
    seen: set[str] = set()
    out: list[str] = []
    for t in toks:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def read_text(path: Path) -> str:
    # Assume UTF-8; most SKILL.md is UTF-8.
    return path.read_text(encoding="utf-8", errors="replace")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def redact_obvious_secrets(text: str) -> str:
    # Keep this intentionally conservative; we only redact common token prefixes.
    patterns: list[tuple[re.Pattern[str], str]] = [
        (re.compile(r"\bsk-[A-Za-z0-9]{10,}\b"), "sk-REDACTED"),
        (re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"), "ghp_REDACTED"),
        (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "github_pat_REDACTED"),
        (re.compile(r"\bAIza[0-9A-Za-z\\-_]{20,}\b"), "AIzaREDACTED"),
        (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "xox-REDACTED"),
    ]
    out = text
    for pat, repl in patterns:
        out = pat.sub(repl, out)
    return out


@dataclass(frozen=True)
class Root:
    label: str
    path: Path


def infer_roots(raw_roots: Iterable[str | Path]) -> list[Root]:
    roots: list[Root] = []
    for r in raw_roots:
        p = Path(r).expanduser()
        label = slugify(str(p)).replace("-", "_")
        roots.append(Root(label=label, path=p))
    return roots

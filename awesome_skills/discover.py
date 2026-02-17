from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


@dataclass(frozen=True)
class DiscoveredSkill:
    root_label: str
    skill_md: Path


def discover_skill_mds(roots: Iterable[tuple[str, Path]]) -> Iterator[DiscoveredSkill]:
    """
    Discover SKILL.md files under roots.

    - Skips `.git` folders.
    - Returns absolute Paths.
    """
    seen: set[str] = set()
    for label, root in roots:
        root = root.expanduser().resolve()
        if not root.exists():
            continue

        for dirpath, dirnames, filenames in os.walk(root):
            # Prune `.git` and common bulky dirs.
            dirnames[:] = [
                d
                for d in dirnames
                if d not in {".git", ".venv", "node_modules", "__pycache__"}
                and not d.startswith(".pytest_cache")
            ]
            if "SKILL.md" not in filenames:
                continue
            p = (Path(dirpath) / "SKILL.md").resolve()
            key = str(p)
            if key in seen:
                continue
            seen.add(key)
            yield DiscoveredSkill(root_label=label, skill_md=p)


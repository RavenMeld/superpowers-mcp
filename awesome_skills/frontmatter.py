from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


_FM_BOUNDARY = re.compile(r"^---\s*$")
_KEYVAL = re.compile(r"^(?P<k>[A-Za-z0-9_.-]+)\s*:\s*(?P<v>.*)\s*$")


@dataclass(frozen=True)
class FrontmatterParse:
    data: dict[str, Any]
    body: str


def _coerce_scalar(v: str) -> Any:
    s = v.strip()
    if s == "":
        return ""
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", s):
        try:
            return int(s)
        except ValueError:
            return s
    # Strip simple quotes.
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s


def parse_frontmatter(text: str) -> FrontmatterParse:
    """
    Parse a minimal YAML frontmatter block.

    Supported:
    - `key: value` scalars
    - `key:` followed by `- item` list lines

    If parsing fails or no frontmatter exists, returns empty data and the original text as body.
    """
    lines = text.splitlines(keepends=True)
    if not lines or not _FM_BOUNDARY.match(lines[0]):
        return FrontmatterParse(data={}, body=text)

    # Find closing boundary.
    end = None
    for i in range(1, min(len(lines), 5000)):
        if _FM_BOUNDARY.match(lines[i]):
            end = i
            break
    if end is None:
        return FrontmatterParse(data={}, body=text)

    fm_lines = [ln.rstrip("\n\r") for ln in lines[1:end]]
    body = "".join(lines[end + 1 :])

    data: dict[str, Any] = {}
    cur_key: str | None = None
    cur_list: list[Any] | None = None

    for raw in fm_lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("- ") and cur_key and cur_list is not None:
            cur_list.append(_coerce_scalar(line[2:]))
            continue

        m = _KEYVAL.match(line)
        if not m:
            # Unknown syntax; stop list accumulation but keep parsing.
            cur_key = None
            cur_list = None
            continue

        k = m.group("k")
        v = m.group("v")
        if v == "":
            # Start a list.
            data[k] = []
            cur_key = k
            cur_list = data[k]
            continue

        data[k] = _coerce_scalar(v)
        cur_key = None
        cur_list = None

    return FrontmatterParse(data=data, body=body)


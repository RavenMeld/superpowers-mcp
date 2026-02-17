from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


_FM_BOUNDARY = re.compile(r"^---\s*$")
_KEYVAL = re.compile(r"^(?P<k>[A-Za-z0-9_.-]+)\s*:\s*(?P<v>.*)\s*$")
_BLOCK_START = re.compile(r"^(?P<style>[|>])(?P<chomp>[+-])?(?P<indent>\d+)?\s*$")


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


def _fold_block(lines: list[str]) -> str:
    """
    Approximate YAML `>` folding:
    - within paragraphs, join lines with spaces
    - preserve blank lines as paragraph breaks
    """
    out_lines: list[str] = []
    para: list[str] = []
    for ln in lines:
        if ln.strip() == "":
            if para:
                out_lines.append(" ".join(x.strip() for x in para).strip())
                para = []
            out_lines.append("")
            continue
        para.append(ln)
    if para:
        out_lines.append(" ".join(x.strip() for x in para).strip())
    return "\n".join(out_lines)


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
    i = 0
    while i < len(fm_lines):
        raw = fm_lines[i]
        line = raw.strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        if line.startswith("- ") and cur_key and cur_list is not None:
            cur_list.append(_coerce_scalar(line[2:]))
            i += 1
            continue

        m = _KEYVAL.match(line)
        if not m:
            # Unknown syntax; stop list accumulation but keep parsing.
            cur_key = None
            cur_list = None
            i += 1
            continue

        k = m.group("k")
        v = m.group("v")

        # Block scalars (common in frontmatter: `description: |`).
        bm = _BLOCK_START.match(v.strip())
        if bm:
            style = bm.group("style")
            explicit_indent = bm.group("indent")

            # Determine indentation from either explicit indicator or the next non-empty line.
            indent = int(explicit_indent) if explicit_indent else None
            j = i + 1
            if indent is None:
                while j < len(fm_lines):
                    nxt = fm_lines[j]
                    if nxt.strip() == "":
                        j += 1
                        continue
                    indent = len(nxt) - len(nxt.lstrip(" "))
                    break
                if indent is None:
                    indent = 0

            block_lines: list[str] = []
            j = i + 1
            while j < len(fm_lines):
                nxt = fm_lines[j]
                if nxt.strip() == "":
                    block_lines.append("")
                    j += 1
                    continue
                lead = len(nxt) - len(nxt.lstrip(" "))
                if lead < indent:
                    break
                block_lines.append(nxt[indent:])
                j += 1

            if style == ">":
                data[k] = _fold_block(block_lines)
            else:
                data[k] = "\n".join(block_lines)

            cur_key = None
            cur_list = None
            i = j
            continue

        if v == "":
            # Start a list.
            data[k] = []
            cur_key = k
            cur_list = data[k]
            i += 1
            continue

        data[k] = _coerce_scalar(v)
        cur_key = None
        cur_list = None
        i += 1

    return FrontmatterParse(data=data, body=body)

#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(repo_root))
    from awesome_skills.mcp_server import main as mcp_main

    return int(mcp_main())


if __name__ == "__main__":
    raise SystemExit(main())


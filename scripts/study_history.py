#!/usr/bin/env python3
"""List past Daily study topics so the routine can avoid repeats."""
import json
from pathlib import Path

docs = Path(__file__).resolve().parent.parent / "docs" / "issues"
for f in sorted(docs.glob("*/issue.json"))[-90:]:
    s = json.loads(f.read_text())["sections"]["study"]
    print(f"{f.parent.name} | {s['track']} | {s['title']}")

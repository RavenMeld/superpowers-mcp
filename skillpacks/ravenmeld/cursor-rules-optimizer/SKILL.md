---
name: cursor-rules-optimizer
description: |
  Improve Cursor rules using observed failure patterns, repeated review comments, and workflow friction points.
---

# Cursor Rules Optimizer

## Use When

- Cursor suggestions repeatedly violate local standards.
- PR reviews show recurring mistakes that rules should prevent.
- You want a measurable loop for improving `.cursor/rules` quality.

## Workflow

1. Collect recurring failure patterns from recent diffs/reviews.
2. Convert each pattern into a concrete rule with an example.
3. Keep rules short, testable, and scoped to repository conventions.
4. Validate rule impact on a small batch of representative tasks.
5. Keep a changelog for rule additions/removals and observed impact.

## Copy/Paste Examples

```bash
rg -n "TODO|FIXME|@ts-ignore" src tests
```

```bash
git log --oneline --decorate -20
```

```bash
rg -n "rule|rules" .cursor || true
```

## Rule Quality Heuristics

- Each rule should have a trigger condition and expected output style.
- Prefer "do/don't" language over vague advice.
- Remove stale rules that no longer map to real failures.

## Safety Notes

- Avoid rules that hard-code secrets or private infrastructure details.
- Do not overfit rules to one-off incidents.

# ExecPlan: Awesome Skills Bridge Performance Layer

## Objective
Improve `search_awesome_skills` latency and load profile by adding:
- in-memory TTL cache for repeated identical queries
- in-flight request coalescing for concurrent identical queries

## Scope
- `src/tools/awesomeSkillsBridge.ts`
- `src/tools/awesomeSkillsBridge.test.ts`
- `README.md`

## Progress
- [x] Cleanup leftover local branch/worktree binding.
- [x] Implement cache + in-flight dedupe.
- [x] Add tests for cache hit, coalescing, TTL expiry.
- [x] Update docs/env vars.
- [x] Run full validation.

## Decisions
- Cache key includes command/query/strategy/limit/db/contextAlias.
- Cache is optional; enabled by default with bounded size and TTL.
- In-flight dedupe returns same promise for identical keys.
- Cache key also scopes by runner identity to avoid collisions in tests/custom runners.
- Cache stores only successful responses (errors are not memoized).

## Validation Commands
- `XDG_CONFIG_HOME=/tmp npm test -- src/tools/awesomeSkillsBridge.test.ts`
- `XDG_CONFIG_HOME=/tmp npm test`
- `npm run build`

## Validation Results
- `XDG_CONFIG_HOME=/tmp npm test -- src/tools/awesomeSkillsBridge.test.ts` -> pass (`8 tests`)
- `XDG_CONFIG_HOME=/tmp npm test` -> pass (`73 tests`)
- `npm run build` -> pass (`tsc`)
- Added follow-up cache hardening tests for env defaults, clamping, and cache-disabled mode.
- Re-validated:
  - `XDG_CONFIG_HOME=/tmp npm test -- src/tools/awesomeSkillsBridge.test.ts` -> pass (`11 tests`)
  - `XDG_CONFIG_HOME=/tmp npm test` -> pass (`76 tests`)
  - `npm run build` -> pass (`tsc`)
- Added additional cache behavior tests for:
  - in-flight coalescing with cache disabled
  - max-entry eviction behavior
- Re-validated again:
  - `XDG_CONFIG_HOME=/tmp npm test -- src/tools/awesomeSkillsBridge.test.ts` -> pass (`13 tests`)
  - `XDG_CONFIG_HOME=/tmp npm test` -> pass (`78 tests`)
  - `npm run build` -> pass (`tsc`)
- Added bridge performance telemetry flags in tool output:
  - `bridge.cache_hit`
  - `bridge.coalesced`
- Added README smoke-test recipe for validating cache and coalescing behavior from MCP clients.
- Verified tool contract + bridge tests:
  - `XDG_CONFIG_HOME=/tmp npm test -- src/tools/awesomeSkillsBridge.test.ts src/tools/register.test.ts` -> pass (`23 tests`)
  - `XDG_CONFIG_HOME=/tmp npm test` -> pass (`78 tests`)
  - `npm run build` -> pass (`tsc`)

## Repro Steps
1. `cd /home/wolvend/codex/agent_playground/worktrees/superpowers-mcp-main-merge`
2. `XDG_CONFIG_HOME=/tmp npm test -- src/tools/awesomeSkillsBridge.test.ts`
3. `XDG_CONFIG_HOME=/tmp npm test`
4. `npm run build`

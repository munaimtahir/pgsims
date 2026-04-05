# 2026-04-03 Frontend Build Policy Alignment

## Scope

Remove the remaining frontend delivery-policy drift:

- `next build` must enforce lint and TypeScript failures instead of bypassing them.
- standalone output must be started with the standalone server, not `next start`.

## Changes

- Removed `eslint.ignoreDuringBuilds` from `frontend/next.config.mjs`
- Removed `typescript.ignoreBuildErrors` from `frontend/next.config.mjs`
- Changed `frontend/package.json` so `start:next` matches standalone runtime behavior
- Added `typecheck` script to `frontend/package.json`
- Updated authoritative docs:
  - `frontend/README.md`
  - `docs/contracts/TRUTH_TESTS.md`

## Commands Run

```bash
cd frontend && npm run lint
cd frontend && npm run typecheck
cd frontend && npm run build
cd frontend && rm -rf .next tsconfig.tsbuildinfo && npm run typecheck
cd frontend && PORT=3201 INTERNAL_API_URL=http://127.0.0.1:8200 NEXT_PUBLIC_API_URL=/api npm run start:next
curl -I -s http://127.0.0.1:3201/login | head -n 5
```

## Result

- Lint passed.
- TypeScript check passed.
- `next build` passed with lint/type enforcement active.
- Cold `npm run typecheck` also passed after deleting `.next` and `tsconfig.tsbuildinfo`.
- Standalone runtime served successfully through `npm run start:next` without the prior `next start` standalone warning.

## Verification Note

An earlier `tsc` failure in this session was caused by running `tsc` and `next build` in parallel while `.next/types` was being rewritten. The frontend type gate is valid when run sequentially, which is now the documented contract.

## Boundary

This pass changes delivery policy only. It does not widen product scope or alter active workflow behavior.

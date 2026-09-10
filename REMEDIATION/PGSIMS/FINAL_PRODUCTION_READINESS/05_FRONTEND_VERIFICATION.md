# Frontend verification

- `npm ci`: PASS.
- `npm run lint`: PASS, no warnings/errors.
- `npm run typecheck`: PASS.
- Jest: PASS, 39 suites / 243 tests.
- `npm run build`: PASS on Next 14.2.35; 79 static pages generated.
- `npm audit --omit=dev`: 1 high and 1 critical remain via Next/PostCSS; fix requires Next 16.

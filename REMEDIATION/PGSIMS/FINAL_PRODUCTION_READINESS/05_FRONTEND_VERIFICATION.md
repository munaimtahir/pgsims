# Frontend verification

- `npm ci`: PASS.
- `npm run lint`: PASS, no warnings/errors.
- `npm run typecheck`: PASS.
- Jest: PASS, 39 suites / 243 tests.
- `npm run build`: PASS on Next 14.2.35; 79 static pages generated.
- VPS checkout verification: PASS for `npm ci`, lint, typecheck, 39 Jest suites / 243 tests, and
  production build.
- `npm audit --omit=dev`: 1 high and 1 critical remain via Next/PostCSS; fix requires Next 16.

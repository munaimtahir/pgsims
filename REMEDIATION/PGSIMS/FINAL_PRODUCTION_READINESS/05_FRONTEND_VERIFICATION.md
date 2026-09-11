# Frontend verification

- `npm ci`: PASS.
- `npm run lint`: PASS, no warnings/errors.
- `npm run typecheck`: PASS.
- Jest: PASS, 39 suites / 240 tests after retiring obsolete public-registration form tests.
- `npm run build`: PASS on Next 16.3.4 / React 19.2.0; 78 static pages generated.
- VPS checkout verification under Node 20.20.2: PASS for `npm ci`, lint, typecheck, 39 Jest suites
  / 240 tests, and production build.
- `npm audit --omit=dev`: PASS, 0 vulnerabilities.
- Full `npm audit`: 1 indirect high `glob` advisory confined to dev/build tooling; not present in
  the production dependency tree.
- Build note: Next reports the existing `middleware` convention deprecation; runtime behavior is
  unchanged and migration is deferred as non-blocking.

# Dependency remediation

Backend: `Django>=5.2,<5.3`; resolved verification version `5.2.17`.

Frontend: Next, React, and eslint-config-next were upgraded to `16.3.4`, `19.2.0`, and `16.3.4`.
The upgrade included the required async catch-all route params, React 19 JSX typing, ESLint 9 flat
configuration, and React 19-compatible test waits. `npm audit --omit=dev` is now zero.
The full audit has one indirect high `glob` advisory in dev/build tooling only; it is absent from
the production dependency tree. No `npm audit fix --force` was used.

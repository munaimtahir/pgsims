# Dependency remediation

Backend: `Django>=5.2,<5.3`; resolved verification version `5.2.17`.

Frontend: `npm ci` passed. `npm audit fix` was run without `--force`; Next and eslint-config-next
were updated within the Next 14 line to `14.2.35`. Production audit remains `1 high, 1 critical`
through Next/PostCSS and reports a fix only via breaking Next 16. No breaking upgrade was applied
without compatibility work and explicit review.

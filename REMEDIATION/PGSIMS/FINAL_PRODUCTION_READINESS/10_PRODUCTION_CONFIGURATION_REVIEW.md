# Production configuration review

No deployment or production configuration was changed. `manage.py check --deploy` exposed existing
warnings; they require deployment-specific secret, HTTPS, host, and proxy values and were not
silenced with repository defaults. Docker/compose and VPS runtime verification must be completed
against the actual deployment checkout before certification.
`docker compose -f docker/docker-compose.yml config` passed, with warnings for intentionally unset
`SECRET_KEY` and `DB_PASSWORD`.
The VPS checkout was verified clean on the remediation branch; no production service was restarted.

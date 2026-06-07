from pathlib import Path

from django.test import SimpleTestCase


REPO_ROOT = Path(__file__).resolve().parents[3]


class DeploymentDomainConfigTests(SimpleTestCase):
    def test_canonical_caddyfile_routes_both_domains(self):
        caddyfile = (REPO_ROOT / "deploy" / "Caddyfile.pgsims").read_text(encoding="utf-8")

        self.assertIn("pg.fmu.edu.pk", caddyfile)
        self.assertIn("pgsims.alshifalab.pk", caddyfile)
        self.assertIn("reverse_proxy 127.0.0.1:8014", caddyfile)
        self.assertIn("reverse_proxy 127.0.0.1:8082", caddyfile)

    def test_production_settings_and_compose_defaults_include_new_domain(self):
        files = [
            REPO_ROOT / "backend" / "sims_project" / "settings.py",
            REPO_ROOT / "docker" / "docker-compose.yml",
            REPO_ROOT / "docker" / "docker-compose.dev.yml",
            REPO_ROOT / "docker" / "docker-compose.prod.yml",
            REPO_ROOT / "docker" / "docker-compose.phc.yml",
            REPO_ROOT / "backend" / ".env.example",
            REPO_ROOT / "backend" / ".env.coolify.example",
            REPO_ROOT / "docs" / "DEPLOYMENT.md",
            REPO_ROOT / "README.md",
        ]

        for path in files:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("pg.fmu.edu.pk", text)
                self.assertIn("pgsims.alshifalab.pk", text)

    def test_primary_frontend_api_url_defaults_to_new_domain_in_production_variants(self):
        for path in [
            REPO_ROOT / "docker" / "docker-compose.dev.yml",
            REPO_ROOT / "docker" / "docker-compose.prod.yml",
        ]:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-https://pg.fmu.edu.pk}", text)

from pathlib import Path

from django.test import SimpleTestCase


REPO_ROOT = Path(__file__).resolve().parents[3]


class DeploymentDomainConfigTests(SimpleTestCase):
    def test_canonical_caddyfile_routes_both_domains(self):
        caddy_path = REPO_ROOT / "deploy" / "Caddyfile.pgsims"
        if not caddy_path.exists():
            self.skipTest("Caddyfile not accessible (running in container)")
        caddyfile = caddy_path.read_text(encoding="utf-8")

        self.assertIn("pg.vexel.pk", caddyfile)
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

        # In container context, we might only have settings.py but not repo root sibling files
        if not (REPO_ROOT / "docker" / "docker-compose.yml").exists():
            self.skipTest("Repo files not accessible (running in container)")

        for path in files:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("pg.vexel.pk", text)
                self.assertIn("pgsims.alshifalab.pk", text)

    def test_primary_frontend_api_url_defaults_to_new_domain_in_production_variants(self):
        paths = [
            REPO_ROOT / "docker" / "docker-compose.dev.yml",
            REPO_ROOT / "docker" / "docker-compose.prod.yml",
        ]
        if not paths[0].exists():
            self.skipTest("Docker compose files not accessible (running in container)")

        for path in paths:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL:-https://pg.vexel.pk}", text)

    def test_shared_caddy_update_preserves_other_sites(self):
        import importlib.util
        helper = REPO_ROOT / "ops" / "caddy_update_site.py"
        if not helper.exists():
            self.skipTest("Repository helper not accessible")
        spec = importlib.util.spec_from_file_location("caddy_update_site", helper)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        before = "android.pgsims.alshifalab.pk {\n    respond ok\n}\n\n"
        after = "\nlast.example {\n    respond fine\n}\n"
        old = "pgsims.alshifalab.pk {\n    handle {\n        respond old\n    }\n}"
        site = "pg.vexel.pk, pgsims.alshifalab.pk {\n    respond new\n}\n"
        updated = module.update_site(before + old + after, site)
        self.assertTrue(updated.startswith(before))
        self.assertTrue(updated.endswith(after))
        self.assertIn(site, updated)
        self.assertNotIn("respond old", updated)
        for invalid in (before, old + "\n" + old):
            with self.assertRaises(ValueError):
                module.update_site(invalid, site)

    def test_canonical_routes_health_and_protects_media(self):
        path = REPO_ROOT / "deploy" / "Caddyfile.pgsims"
        if not path.exists():
            self.skipTest("Repository config not accessible")
        text = path.read_text()
        self.assertIn("handle /healthz*", text)
        self.assertIn("handle /media/* {\n\t\treverse_proxy 127.0.0.1:8014", text)
        self.assertIn("pgsims.pmc.edu.pk", text)

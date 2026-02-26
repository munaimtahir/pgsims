from pathlib import Path

from django.test import SimpleTestCase


class DriftGuardTests(SimpleTestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[4]

    def _iter_py_files(self):
        for path in self.repo_root.rglob("*.py"):
            if any(part in {".venv", "node_modules", "__pycache__"} for part in path.parts):
                continue
            if "docs" in path.parts or "scripts" in path.parts:
                continue
            if path.name == "test_drift_guards.py":
                continue
            yield path

    def test_forbidden_notification_create_legacy_keys_not_used(self):
        violations = []
        forbidden = ("user=", "message=", "type=", "related_object_id=")
        for path in self._iter_py_files():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "Notification.objects.create(" not in text:
                continue
            non_comment_lines = [
                line for line in text.splitlines() if not line.lstrip().startswith("#")
            ]
            cleaned = "\n".join(non_comment_lines)
            if "Notification.objects.create(" not in cleaned:
                continue
            if any(key in cleaned for key in forbidden):
                violations.append(str(path.relative_to(self.repo_root)))
        self.assertEqual(
            violations,
            [],
            f"Forbidden Notification.objects.create legacy keys found in: {violations}",
        )

    def test_duplicate_department_model_not_reintroduced(self):
        violations = []
        rotations_models = self.repo_root / "backend" / "sims" / "rotations" / "models.py"
        if rotations_models.exists():
            text = rotations_models.read_text(encoding="utf-8", errors="ignore")
            if "class Department(models.Model)" in text:
                violations.append("backend/sims/rotations/models.py:class Department")
        for path in self._iter_py_files():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "RotationDepartment" in text or "AcademicDepartment" in text:
                violations.append(str(path.relative_to(self.repo_root)))
        self.assertEqual(violations, [], f"Duplicate department model drift detected: {violations}")

import os
from pathlib import Path

from django.test import SimpleTestCase


class DriftGuardTests(SimpleTestCase):
    def setUp(self):
        self.repo_root = Path(__file__).resolve().parents[4]

    def _iter_py_files(self):
        # The guards inspect authored Python only.  Generated reports and virtual
        # environments can contain thousands of Python files, which makes this
        # otherwise small check disproportionately expensive and nondeterministic.
        excluded = {
            ".venv", "venv", "node_modules", "__pycache__", ".git", ".gradle",
            ".next", ".pytest_cache", ".mypy_cache", "build", "coverage",
            "htmlcov", "output", "docs", "scripts", ".claude", ".gemini",
            ".e2e_upload_tmp", ".idea",
        }
        # The clean-room guards apply to the maintained Django application.  Archived
        # modules, migration history, and repository tooling have separate governance
        # checks and must not turn this source guard into a repository-wide crawl.
        source_root = self.repo_root / "backend" / "sims"
        excluded.update({"_legacy", "migrations", "tests"})
        for directory, directories, filenames in os.walk(source_root):
            directories[:] = [name for name in directories if name not in excluded]
            for name in filenames:
                if (
                    name.endswith(".py")
                    and name != "test_drift_guards.py"
                    and not name.startswith("test_")
                    and not name.endswith("_test.py")
                    and name != "tests.py"
                ):
                    yield Path(directory) / name

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
            if any(key in block for block in self._notification_create_blocks(cleaned) for key in forbidden):
                violations.append(str(path.relative_to(self.repo_root)))
        self.assertEqual(
            violations,
            [],
            f"Forbidden Notification.objects.create legacy keys found in: {violations}",
        )

    def _notification_create_blocks(self, text: str):
        marker = "Notification.objects.create("
        start = 0
        while True:
            index = text.find(marker, start)
            if index == -1:
                return
            depth = 0
            started = False
            for cursor in range(index, len(text)):
                char = text[cursor]
                if char == "(":
                    depth += 1
                    started = True
                elif char == ")":
                    depth -= 1
                    if started and depth == 0:
                        yield text[index : cursor + 1]
                        start = cursor + 1
                        break
            else:
                yield text[index:]
                return

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

"""Tests for the small, deterministic utility functions in sims/backup_center/services.py
that had zero prior coverage: hashing helpers, engine detection, and summary builders. The
large backup/restore orchestration functions (create_routine_application_data_backup,
restore_routine_application_data_backup, etc.) are intentionally not targeted here - they run
real pg_dump/filesystem operations and are already exercised by the shell-script-level backup
verification (scripts/backup_pgms_db.sh, verify_pgms_backup.sh); a shallow unit test with heavy
mocking would add more risk of false confidence than value.
"""

import hashlib
import zipfile
from pathlib import Path

from django.test import TestCase

from sims.backup_center.services import (
    _compute_tree_sha256,
    _sha256_file,
    _sha256_zip_member,
    detect_database_engine,
    get_app_metadata,
    get_media_summary,
    get_table_counts,
)


class Sha256FileTests(TestCase):
    def test_matches_stdlib_hash(self, tmp_path=None):
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"hello pgsims backup")
            path = Path(f.name)
        try:
            expected = hashlib.sha256(b"hello pgsims backup").hexdigest()
            self.assertEqual(_sha256_file(path), expected)
        finally:
            path.unlink()

    def test_empty_file_matches_empty_hash(self):
        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = Path(f.name)
        try:
            self.assertEqual(_sha256_file(path), hashlib.sha256(b"").hexdigest())
        finally:
            path.unlink()


class Sha256ZipMemberTests(TestCase):
    def test_matches_stdlib_hash_of_member_content(self):
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            zip_path = Path(f.name)
        try:
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("data.txt", b"backup contents here")
            with zipfile.ZipFile(zip_path, "r") as zf:
                digest = _sha256_zip_member(zf, "data.txt")
            self.assertEqual(digest, hashlib.sha256(b"backup contents here").hexdigest())
        finally:
            zip_path.unlink()


class ComputeTreeSha256Tests(TestCase):
    def test_deterministic_for_same_tree(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "a.txt").write_bytes(b"aaa")
            (root / "b.txt").write_bytes(b"bbb")
            (root / "sub").mkdir()
            (root / "sub" / "c.txt").write_bytes(b"ccc")

            digest1, count1 = _compute_tree_sha256(root)
            digest2, count2 = _compute_tree_sha256(root)

            self.assertEqual(digest1, digest2)
            self.assertEqual(count1, 3)

    def test_different_content_produces_different_digest(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            root1, root2 = Path(d1), Path(d2)
            (root1 / "a.txt").write_bytes(b"aaa")
            (root2 / "a.txt").write_bytes(b"different content")

            digest1, _ = _compute_tree_sha256(root1)
            digest2, _ = _compute_tree_sha256(root2)

            self.assertNotEqual(digest1, digest2)

    def test_empty_directory_has_zero_file_count(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            _, count = _compute_tree_sha256(Path(d))
            self.assertEqual(count, 0)


class DetectDatabaseEngineTests(TestCase):
    def test_returns_configured_engine_string(self):
        engine = detect_database_engine()
        self.assertIsInstance(engine, str)
        self.assertNotEqual(engine, "")


class GetAppMetadataTests(TestCase):
    def test_returns_expected_keys(self):
        metadata = get_app_metadata()
        self.assertEqual(metadata["app_name"], "PGSIMS")
        self.assertIn("app_version", metadata)
        self.assertIn("branch", metadata)
        self.assertIn("commit_hash", metadata)


class GetTableCountsTests(TestCase):
    def test_returns_nonnegative_counts_for_known_models(self):
        counts = get_table_counts()
        self.assertIn("users.user", counts)
        self.assertGreaterEqual(counts["users.user"], 0)


class GetMediaSummaryTests(TestCase):
    def test_returns_summary_shape(self):
        summary = get_media_summary()
        self.assertIn("file_count", summary)
        self.assertIn("total_size_bytes", summary)
        self.assertIn("media_root_exists", summary)
        self.assertIsInstance(summary["file_count"], int)

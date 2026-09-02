"""Tests for sims/backup_center/encryption.py -- previously only indirectly exercised.

Covers key resolution (env var, key-file fallback, django settings fallback, missing-key
error), and the file/string encrypt-decrypt round trips including failure when the wrong key
is used to decrypt (the exact failure mode that would silently corrupt a disaster-recovery
restore if it went unnoticed).
"""

import os
from unittest import mock

import pytest
from cryptography.fernet import InvalidToken
from django.test import TestCase, override_settings

from sims.backup_center.encryption import (
    decrypt_file,
    decrypt_string,
    encrypt_file,
    encrypt_string,
    get_encryption_key,
)


class GetEncryptionKeyTests(TestCase):
    def test_reads_from_environment_variable(self):
        with mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "my-secret"}, clear=False):
            key1 = get_encryption_key()
            key2 = get_encryption_key()
        # Deterministic derivation: same raw key always yields the same Fernet key.
        self.assertEqual(key1, key2)

    def test_different_raw_keys_yield_different_derived_keys(self):
        with mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "key-one"}, clear=False):
            key1 = get_encryption_key()
        with mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "key-two"}, clear=False):
            key2 = get_encryption_key()
        self.assertNotEqual(key1, key2)

    def test_reads_from_key_file_when_env_var_absent(self):
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".key") as f:
            f.write("key-from-file\n")
            key_file_path = f.name
        try:
            env = {k: v for k, v in os.environ.items() if k != "PGSIMS_BACKUP_ENCRYPTION_KEY"}
            env["PGSIMS_BACKUP_ENCRYPTION_KEY_FILE"] = key_file_path
            with mock.patch.dict(os.environ, env, clear=True):
                key_from_file = get_encryption_key()
            with mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "key-from-file"}, clear=False):
                key_from_env = get_encryption_key()
            self.assertEqual(key_from_file, key_from_env)
        finally:
            os.unlink(key_file_path)

    def test_falls_back_to_django_settings(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith("PGSIMS_BACKUP_ENCRYPTION_KEY")}
        with mock.patch.dict(os.environ, env, clear=True):
            with override_settings(PGSIMS_BACKUP_ENCRYPTION_KEY="from-settings"):
                key = get_encryption_key()
        self.assertIsNotNone(key)

    def test_raises_when_no_key_configured_anywhere(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith("PGSIMS_BACKUP_ENCRYPTION_KEY")}
        with mock.patch.dict(os.environ, env, clear=True):
            with override_settings(PGSIMS_BACKUP_ENCRYPTION_KEY=None):
                with self.assertRaises(ValueError):
                    get_encryption_key()

    def test_nonexistent_key_file_path_is_ignored(self):
        env = {k: v for k, v in os.environ.items() if not k.startswith("PGSIMS_BACKUP_ENCRYPTION_KEY")}
        env["PGSIMS_BACKUP_ENCRYPTION_KEY_FILE"] = "/nonexistent/path/to/key.txt"
        with mock.patch.dict(os.environ, env, clear=True):
            with override_settings(PGSIMS_BACKUP_ENCRYPTION_KEY=None):
                with self.assertRaises(ValueError):
                    get_encryption_key()


@mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "test-fixed-key"}, clear=False)
class EncryptDecryptStringTests(TestCase):
    def test_roundtrip(self):
        original = "super-secret-oauth-token"
        encrypted = encrypt_string(original)
        self.assertNotEqual(encrypted, original)
        self.assertEqual(decrypt_string(encrypted), original)

    def test_encrypt_none_raises(self):
        with self.assertRaises(ValueError):
            encrypt_string(None)

    def test_decrypt_none_raises(self):
        with self.assertRaises(ValueError):
            decrypt_string(None)

    def test_decrypt_with_wrong_key_fails(self):
        encrypted = encrypt_string("some-value")
        with mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "a-different-key"}):
            with self.assertRaises(InvalidToken):
                decrypt_string(encrypted)


@mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "test-fixed-key"}, clear=False)
class EncryptDecryptFileTests(TestCase):
    def test_roundtrip(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "plain.txt")
            enc = os.path.join(d, "plain.enc")
            dec = os.path.join(d, "plain.dec")
            with open(src, "wb") as f:
                f.write(b"backup file contents \x00\x01\x02")

            encrypt_file(src, enc)
            self.assertTrue(os.path.exists(enc))
            with open(enc, "rb") as f:
                encrypted_bytes = f.read()
            self.assertNotEqual(encrypted_bytes, b"backup file contents \x00\x01\x02")

            decrypt_file(enc, dec)
            with open(dec, "rb") as f:
                self.assertEqual(f.read(), b"backup file contents \x00\x01\x02")

    def test_decrypt_with_wrong_key_fails(self):
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "plain.txt")
            enc = os.path.join(d, "plain.enc")
            dec = os.path.join(d, "plain.dec")
            with open(src, "wb") as f:
                f.write(b"sensitive backup data")
            encrypt_file(src, enc)

            with mock.patch.dict(os.environ, {"PGSIMS_BACKUP_ENCRYPTION_KEY": "wrong-key"}):
                with self.assertRaises(InvalidToken):
                    decrypt_file(enc, dec)

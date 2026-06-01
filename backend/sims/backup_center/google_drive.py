import datetime
import hashlib
import json
import os
import secrets
import tempfile
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
from django.core import signing
from django.core.cache import cache
from django.utils import timezone

from .models import BackupCloudConnection, BackupCloudCopy, BackupJob
from .encryption import decrypt_file, encrypt_file


GOOGLE_OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_OAUTH_TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_OAUTH_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

GOOGLE_DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"
GOOGLE_DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files"


@dataclass(frozen=True)
class GoogleDriveConfig:
    enabled: bool
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: str
    backup_folder_name: str
    backup_folder_id: str


class GoogleDriveBackupProvider:
    STATE_SALT = "backup-center-google-drive-oauth-state"
    STATE_CACHE_PREFIX = "backup_center:google_drive_oauth_state:"
    STATE_TTL_SECONDS = 10 * 60

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> GoogleDriveConfig:
        enabled = os.environ.get("GOOGLE_DRIVE_BACKUP_ENABLED", "false").lower() in ("1", "true", "yes")
        return GoogleDriveConfig(
            enabled=enabled,
            client_id=os.environ.get("GOOGLE_DRIVE_CLIENT_ID", "").strip(),
            client_secret=os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET", "").strip(),
            redirect_uri=os.environ.get("GOOGLE_DRIVE_REDIRECT_URI", "").strip(),
            scopes=os.environ.get("GOOGLE_DRIVE_SCOPES", "https://www.googleapis.com/auth/drive.file").strip(),
            backup_folder_name=os.environ.get("GOOGLE_DRIVE_BACKUP_FOLDER_NAME", "PGSIMS Backups").strip(),
            backup_folder_id=os.environ.get("GOOGLE_DRIVE_BACKUP_FOLDER_ID", "").strip(),
        )

    def _require_enabled(self) -> None:
        if not self.config.enabled:
            raise ValueError("Google Drive backup is disabled. Set GOOGLE_DRIVE_BACKUP_ENABLED=true.")

    def _require_oauth_config(self) -> None:
        missing = []
        if not self.config.client_id:
            missing.append("GOOGLE_DRIVE_CLIENT_ID")
        if not self.config.client_secret:
            missing.append("GOOGLE_DRIVE_CLIENT_SECRET")
        if not self.config.redirect_uri:
            missing.append("GOOGLE_DRIVE_REDIRECT_URI")
        if missing:
            raise ValueError(f"Missing Google OAuth configuration: {', '.join(missing)}")

    def _state_cache_key(self, nonce: str) -> str:
        return f"{self.STATE_CACHE_PREFIX}{nonce}"

    def _generate_state(self, user_id: int) -> str:
        nonce = secrets.token_urlsafe(32)
        cache.set(self._state_cache_key(nonce), str(user_id), timeout=self.STATE_TTL_SECONDS)
        return signing.dumps({"n": nonce, "u": user_id}, salt=self.STATE_SALT)

    def _validate_state(self, state: str) -> int:
        data = signing.loads(state, salt=self.STATE_SALT, max_age=self.STATE_TTL_SECONDS)
        nonce = data.get("n")
        user_id = data.get("u")
        if not nonce or not user_id:
            raise ValueError("Invalid OAuth state")
        cached_user_id = cache.get(self._state_cache_key(nonce))
        if not cached_user_id or str(cached_user_id) != str(user_id):
            raise ValueError("Invalid or expired OAuth state")
        cache.delete(self._state_cache_key(nonce))
        return int(user_id)

    def build_authorization_url(self, *, user_id: int) -> str:
        self._require_enabled()
        self._require_oauth_config()

        state = self._generate_state(user_id)
        params = {
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "response_type": "code",
            "scope": self.config.scopes,
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "consent",
            "state": state,
        }
        return f"{GOOGLE_OAUTH_AUTH_URL}?{urlencode(params)}"

    def exchange_code_for_tokens(self, *, code: str) -> Dict[str, Any]:
        self._require_enabled()
        self._require_oauth_config()

        resp = requests.post(
            GOOGLE_OAUTH_TOKEN_URL,
            data={
                "code": code,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "redirect_uri": self.config.redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=20,
        )
        if resp.status_code != 200:
            raise ValueError(f"Token exchange failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()

    def refresh_access_token(self, connection: BackupCloudConnection) -> BackupCloudConnection:
        self._require_enabled()
        self._require_oauth_config()

        refresh_token = connection.get_refresh_token()
        resp = requests.post(
            GOOGLE_OAUTH_TOKEN_URL,
            data={
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
            timeout=20,
        )
        if resp.status_code != 200:
            raise ValueError(f"Token refresh failed: {resp.status_code} {resp.text[:200]}")
        data = resp.json()
        expires_in = int(data.get("expires_in", 0))
        expiry = timezone.now() + datetime.timedelta(seconds=expires_in) if expires_in else None
        access_token = data.get("access_token")
        if not access_token:
            raise ValueError("Token refresh did not return access_token")

        connection.set_tokens(
            access_token=access_token,
            refresh_token=None,  # refresh token typically not returned on refresh
            token_expiry=expiry,
            scopes=connection.scopes,
        )
        connection.status = "connected"
        connection.last_error = None
        connection.save(update_fields=["access_token_encrypted", "token_expiry", "status", "last_error", "updated_at"])
        return connection

    def get_valid_access_token(self, connection: BackupCloudConnection) -> str:
        token = connection.get_access_token()
        if connection.is_token_expired():
            connection = self.refresh_access_token(connection)
            token = connection.get_access_token()
        return token

    def fetch_account_email_if_possible(self, *, access_token: str) -> Optional[str]:
        # Best-effort: only works if configured scopes allow it.
        try:
            resp = requests.get(
                GOOGLE_OAUTH_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=20,
            )
            if resp.status_code == 200:
                data = resp.json()
                email = data.get("email")
                if email:
                    return str(email)
        except Exception:
            return None
        # Fallback best-effort: tokeninfo sometimes includes email depending on scopes.
        try:
            resp = requests.get(GOOGLE_OAUTH_TOKENINFO_URL, params={"access_token": access_token}, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                email = data.get("email")
                if email:
                    return str(email)
        except Exception:
            return None
        return None

    def handle_oauth_callback(self, *, code: str, state: str) -> BackupCloudConnection:
        self._require_enabled()
        user_id = self._validate_state(state)

        token_data = self.exchange_code_for_tokens(code=code)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = int(token_data.get("expires_in", 0))
        scope = token_data.get("scope")
        expiry = timezone.now() + datetime.timedelta(seconds=expires_in) if expires_in else None
        if not access_token:
            raise ValueError("Token exchange did not return access_token")

        connection, _ = BackupCloudConnection.objects.get_or_create(provider="google_drive")
        connection.connected_by_user_id = user_id
        connection.status = "connected"
        connection.last_error = None
        connection.set_tokens(
            access_token=access_token,
            refresh_token=refresh_token,
            token_expiry=expiry,
            scopes=scope or self.config.scopes,
        )

        email = self.fetch_account_email_if_possible(access_token=access_token)
        if email:
            connection.account_email = email

        connection.save()
        return connection

    def _auth_headers(self, access_token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {access_token}"}

    def health_check(self, connection: BackupCloudConnection) -> Dict[str, Any]:
        self._require_enabled()
        token = self.get_valid_access_token(connection)
        resp = requests.get(
            GOOGLE_DRIVE_FILES_URL,
            headers=self._auth_headers(token),
            params={"pageSize": 1, "fields": "files(id)"},
            timeout=20,
        )
        ok = resp.status_code == 200
        connection.last_health_check_at = timezone.now()
        if ok:
            connection.status = "connected"
            connection.last_error = None
        else:
            connection.status = "failed"
            connection.last_error = f"Drive health check failed: {resp.status_code} {resp.text[:200]}"
        connection.save(update_fields=["last_health_check_at", "status", "last_error", "updated_at"])
        return {"status": "healthy" if ok else "failed", "http_status": resp.status_code}

    def ensure_backup_folder(self, connection: BackupCloudConnection) -> BackupCloudConnection:
        self._require_enabled()
        token = self.get_valid_access_token(connection)

        # 1) Explicit folder ID via environment variable wins.
        if self.config.backup_folder_id:
            connection.backup_folder_id = self.config.backup_folder_id
            if not connection.backup_folder_name:
                connection.backup_folder_name = self.config.backup_folder_name
            connection.save(update_fields=["backup_folder_id", "backup_folder_name", "updated_at"])
            return connection

        # 2) Previously stored folder
        if connection.backup_folder_id:
            return connection

        folder_name = self.config.backup_folder_name or "PGSIMS Backups"

        # 3) Find app-created folder
        escaped_folder_name = folder_name.replace("'", "\\'")
        q = (
            "mimeType='application/vnd.google-apps.folder' "
            f"and name='{escaped_folder_name}' and trashed=false"
        )
        resp = requests.get(
            GOOGLE_DRIVE_FILES_URL,
            headers=self._auth_headers(token),
            params={"q": q, "fields": "files(id,name)", "pageSize": 10},
            timeout=20,
        )
        if resp.status_code != 200:
            raise ValueError(f"Drive folder lookup failed: {resp.status_code} {resp.text[:200]}")

        files = resp.json().get("files", [])
        if files:
            folder = files[0]
            connection.backup_folder_id = folder.get("id")
            connection.backup_folder_name = folder.get("name") or folder_name
            connection.save(update_fields=["backup_folder_id", "backup_folder_name", "updated_at"])
            return connection

        # 4) Create folder
        create_resp = requests.post(
            GOOGLE_DRIVE_FILES_URL,
            headers={**self._auth_headers(token), "Content-Type": "application/json"},
            data=json.dumps({"name": folder_name, "mimeType": "application/vnd.google-apps.folder"}),
            timeout=20,
        )
        if create_resp.status_code not in (200, 201):
            raise ValueError(f"Drive folder create failed: {create_resp.status_code} {create_resp.text[:200]}")

        folder = create_resp.json()
        connection.backup_folder_id = folder.get("id")
        connection.backup_folder_name = folder.get("name") or folder_name
        connection.save(update_fields=["backup_folder_id", "backup_folder_name", "updated_at"])
        return connection

    def _init_resumable_upload(self, *, access_token: str, metadata: Dict[str, Any]) -> str:
        init_resp = requests.post(
            GOOGLE_DRIVE_UPLOAD_URL,
            headers={
                **self._auth_headers(access_token),
                "Content-Type": "application/json; charset=UTF-8",
                "X-Upload-Content-Type": "application/octet-stream",
            },
            params={"uploadType": "resumable", "fields": "id"},
            data=json.dumps(metadata),
            timeout=20,
            allow_redirects=False,
        )
        if init_resp.status_code not in (200, 201):
            raise ValueError(f"Drive resumable init failed: {init_resp.status_code} {init_resp.text[:200]}")
        upload_url = init_resp.headers.get("Location")
        if not upload_url:
            raise ValueError("Drive resumable init missing Location header")
        return upload_url

    def upload_file(
        self,
        *,
        connection: BackupCloudConnection,
        local_path: str,
        remote_name: str,
        folder_id: str,
        mime_type: str = "application/octet-stream",
        description: str | None = None,
    ) -> Dict[str, Any]:
        self._require_enabled()
        token = self.get_valid_access_token(connection)

        metadata: Dict[str, Any] = {"name": remote_name, "parents": [folder_id]}
        if description:
            metadata["description"] = description

        upload_url = self._init_resumable_upload(access_token=token, metadata=metadata)
        file_size = os.path.getsize(local_path)

        with open(local_path, "rb") as f:
            put_resp = requests.put(
                upload_url,
                headers={
                    **self._auth_headers(token),
                    "Content-Type": mime_type,
                    "Content-Length": str(file_size),
                },
                data=f,
                timeout=60 * 10,
            )

        if put_resp.status_code not in (200, 201):
            raise ValueError(f"Drive upload failed: {put_resp.status_code} {put_resp.text[:200]}")

        drive_file = put_resp.json()
        file_id = drive_file.get("id")
        if not file_id:
            raise ValueError("Drive upload did not return file id")
        return {"id": file_id}

    def get_file_metadata(self, *, connection: BackupCloudConnection, file_id: str) -> Dict[str, Any]:
        token = self.get_valid_access_token(connection)
        resp = requests.get(
            f"{GOOGLE_DRIVE_FILES_URL}/{file_id}",
            headers=self._auth_headers(token),
            params={"fields": "id,name,size,md5Checksum,modifiedTime"},
            timeout=20,
        )
        if resp.status_code != 200:
            raise ValueError(f"Drive metadata fetch failed: {resp.status_code} {resp.text[:200]}")
        return resp.json()

    def verify_uploaded_file(
        self,
        *,
        connection: BackupCloudConnection,
        drive_file_id: str,
        expected_size: int | None = None,
        expected_md5: str | None = None,
    ) -> Dict[str, Any]:
        meta = self.get_file_metadata(connection=connection, file_id=drive_file_id)
        if expected_size is not None and str(meta.get("size")) != str(expected_size):
            raise ValueError("Remote file size mismatch")
        if expected_md5 is not None and meta.get("md5Checksum") and meta.get("md5Checksum") != expected_md5:
            raise ValueError("Remote file checksum mismatch")
        return meta

    def _sha256_file(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _md5_file(self, path: str) -> str:
        h = hashlib.md5()  # nosec - checksum only (not for cryptographic security)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def upload_backup(self, *, backup_record: BackupJob) -> BackupCloudCopy:
        self._require_enabled()

        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection or connection.status != "connected":
            raise ValueError("Google Drive is not connected")

        if not backup_record.file_path or not os.path.exists(backup_record.file_path):
            raise FileNotFoundError("Backup file not found on disk")

        connection = self.ensure_backup_folder(connection)
        folder_id = connection.backup_folder_id
        if not folder_id:
            raise ValueError("Backup folder is not configured")

        backup_id_str = str(backup_record.id).zfill(6)
        date_str = timezone.now().strftime("%Y%m%d")

        base_name = f"backup-{backup_id_str}-{date_str}"
        encrypted_name = f"{base_name}-{backup_record.backup_kind}.pgsimsbak.enc"
        manifest_name = f"{base_name}-manifest.json"
        checksum_name = f"{base_name}-checksum.sha256"

        tmp_dir = tempfile.mkdtemp(prefix="pgsims-drive-backup-")
        encrypted_path = os.path.join(tmp_dir, encrypted_name)
        manifest_path = os.path.join(tmp_dir, manifest_name)
        checksum_path = os.path.join(tmp_dir, checksum_name)

        cloud_copy = BackupCloudCopy.objects.create(
            backup_record=backup_record,
            provider="google_drive",
            connection=connection,
            remote_folder_id=folder_id,
            remote_file_name=encrypted_name,
            upload_status="uploading",
        )

        try:
            encrypt_file(backup_record.file_path, encrypted_path)

            manifest = backup_record.manifest_json or {}
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, sort_keys=True)

            sha256_val = self._sha256_file(encrypted_path)
            with open(checksum_path, "w", encoding="utf-8") as f:
                f.write(f"{sha256_val}  {encrypted_name}\n")

            md5_val = self._md5_file(encrypted_path)
            size_val = os.path.getsize(encrypted_path)

            backup_file = self.upload_file(
                connection=connection,
                local_path=encrypted_path,
                remote_name=encrypted_name,
                folder_id=folder_id,
                mime_type="application/octet-stream",
                description=f"PGSIMS encrypted backup ({backup_record.backup_kind})",
            )
            manifest_file = self.upload_file(
                connection=connection,
                local_path=manifest_path,
                remote_name=manifest_name,
                folder_id=folder_id,
                mime_type="application/json",
                description="PGSIMS backup manifest",
            )
            checksum_file = self.upload_file(
                connection=connection,
                local_path=checksum_path,
                remote_name=checksum_name,
                folder_id=folder_id,
                mime_type="text/plain",
                description="PGSIMS backup checksum (sha256 of encrypted file)",
            )

            self.verify_uploaded_file(
                connection=connection, drive_file_id=backup_file["id"], expected_size=size_val, expected_md5=md5_val
            )

            cloud_copy.remote_file_id = backup_file["id"]
            cloud_copy.remote_manifest_file_id = manifest_file["id"]
            cloud_copy.remote_checksum_file_id = checksum_file["id"]
            cloud_copy.remote_size = size_val
            cloud_copy.local_checksum = sha256_val
            cloud_copy.remote_checksum = md5_val
            cloud_copy.upload_status = "uploaded"
            cloud_copy.uploaded_at = timezone.now()
            cloud_copy.verification_status = "verified"
            cloud_copy.verified_at = timezone.now()
            cloud_copy.save()
            return cloud_copy
        except Exception as e:
            cloud_copy.upload_status = "upload_failed"
            cloud_copy.verification_status = "verification_failed"
            cloud_copy.error_message = str(e)
            cloud_copy.save(update_fields=["upload_status", "verification_status", "error_message", "updated_at"])
            raise
        finally:
            try:
                for p in (encrypted_path, manifest_path, checksum_path):
                    if os.path.exists(p):
                        os.remove(p)
                if os.path.exists(tmp_dir):
                    os.rmdir(tmp_dir)
            except Exception:
                pass

    def download_backup(self, *, cloud_copy: BackupCloudCopy, destination_path: str) -> str:
        self._require_enabled()

        connection = cloud_copy.connection
        if connection.provider != "google_drive":
            raise ValueError("Cloud copy is not Google Drive")
        if not cloud_copy.remote_file_id:
            raise ValueError("Cloud copy missing remote file id")

        token = self.get_valid_access_token(connection)
        temp_enc_path = f"{destination_path}.enc"

        cloud_copy.download_status = "downloading"
        cloud_copy.save(update_fields=["download_status", "updated_at"])

        try:
            with requests.get(
                f"{GOOGLE_DRIVE_FILES_URL}/{cloud_copy.remote_file_id}",
                headers=self._auth_headers(token),
                params={"alt": "media"},
                stream=True,
                timeout=60 * 10,
            ) as resp:
                if resp.status_code != 200:
                    raise ValueError(f"Drive download failed: {resp.status_code} {resp.text[:200]}")
                with open(temp_enc_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)

            # Verify sha256 against stored checksum of encrypted file.
            if cloud_copy.local_checksum:
                sha = self._sha256_file(temp_enc_path)
                if sha != cloud_copy.local_checksum:
                    raise ValueError("Downloaded file checksum verification failed")

            decrypt_file(temp_enc_path, destination_path)

            cloud_copy.download_status = "downloaded"
            cloud_copy.downloaded_at = timezone.now()
            cloud_copy.save(update_fields=["download_status", "downloaded_at", "updated_at"])
            return destination_path
        except Exception as e:
            cloud_copy.download_status = "download_failed"
            cloud_copy.error_message = str(e)
            cloud_copy.save(update_fields=["download_status", "error_message", "updated_at"])
            raise
        finally:
            if os.path.exists(temp_enc_path):
                try:
                    os.remove(temp_enc_path)
                except Exception:
                    pass

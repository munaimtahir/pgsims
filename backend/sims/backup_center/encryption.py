import os
import base64
import hashlib
import logging
from django.conf import settings
from cryptography.fernet import Fernet

logger = logging.getLogger('sims.backup_center')

def get_encryption_key() -> bytes:
    """
    Retrieves or derives a 32-byte Fernet key from environment variables.
    """
    raw_key = os.environ.get("PGSIMS_BACKUP_ENCRYPTION_KEY")
    if not raw_key:
        key_file = os.environ.get("PGSIMS_BACKUP_ENCRYPTION_KEY_FILE")
        if key_file and os.path.exists(key_file):
            try:
                with open(key_file, "r") as f:
                    raw_key = f.read().strip()
            except Exception as e:
                logger.error(f"Failed to read encryption key file: {e}")
                
    if not raw_key:
        # Fallback to django settings if defined there
        raw_key = getattr(settings, "PGSIMS_BACKUP_ENCRYPTION_KEY", None)

    if not raw_key:
        raise ValueError("Backup encryption key is not configured. Set PGSIMS_BACKUP_ENCRYPTION_KEY or PGSIMS_BACKUP_ENCRYPTION_KEY_FILE.")

    # Derive a valid Fernet key from the raw key using SHA-256
    hasher = hashlib.sha256()
    hasher.update(raw_key.encode("utf-8"))
    key_32bytes = hasher.digest()
    return base64.urlsafe_b64encode(key_32bytes)

def encrypt_file(source_path: str, dest_path: str) -> None:
    """
    Encrypts source_path and writes encrypted contents to dest_path using Fernet.
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    
    with open(source_path, "rb") as f_in:
        data = f_in.read()
        
    encrypted_data = fernet.encrypt(data)
    
    with open(dest_path, "wb") as f_out:
        f_out.write(encrypted_data)

def decrypt_file(source_path: str, dest_path: str) -> None:
    """
    Decrypts source_path and writes decrypted contents to dest_path using Fernet.
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    
    with open(source_path, "rb") as f_in:
        data = f_in.read()
        
    decrypted_data = fernet.decrypt(data)
    
    with open(dest_path, "wb") as f_out:
        f_out.write(decrypted_data)

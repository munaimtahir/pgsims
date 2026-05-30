import os
import json
import zipfile
import hashlib
import tempfile
import subprocess
import shutil
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from .models import BackupJob, BackupAuditLog, RestoreJob
from django.core.files.base import ContentFile

def detect_database_engine():
    db_config = settings.DATABASES.get('default', {})
    return db_config.get('ENGINE', 'unknown')

def create_full_backup(user=None, notes=None):
    job = BackupJob.objects.create(
        status='running',
        backup_type='full',
        database_engine=detect_database_engine(),
        created_by=user,
        media_included=True
    )
    
    BackupAuditLog.objects.create(
        action='backup_created',
        actor=user,
        backup_job=job,
        details_json={'notes': notes, 'step': 'started'}
    )
    
    try:
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = settings.SIMS_SETTINGS.get('BACKUP_LOCATION', getattr(settings, 'BASE_DIR', '') / 'pilot_data' / 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        file_name = f"pgsims_backup_{timestamp}.zip"
        file_path = os.path.join(backup_dir, file_name)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Dump database
            db_engine = job.database_engine
            db_dump_path = os.path.join(tmpdir, 'database_dump.sql')
            
            if 'postgresql' in db_engine:
                db_config = settings.DATABASES['default']
                env = os.environ.copy()
                env['PGPASSWORD'] = db_config.get('PASSWORD', '')
                
                cmd = [
                    'pg_dump',
                    '-h', db_config.get('HOST', 'localhost'),
                    '-p', str(db_config.get('PORT', '5432')),
                    '-U', db_config.get('USER', ''),
                    '-F', 'c', # Custom format
                    '-f', db_dump_path,
                    db_config.get('NAME', '')
                ]
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"pg_dump failed: {result.stderr}")
            elif 'sqlite' in db_engine:
                db_path = settings.DATABASES['default']['NAME']
                shutil.copy2(db_path, db_dump_path)
            else:
                raise Exception(f"Unsupported database engine for automatic backup: {db_engine}")
            
            # 2. Copy Media
            media_included = False
            media_tmp_dir = os.path.join(tmpdir, 'media')
            if hasattr(settings, 'MEDIA_ROOT') and os.path.exists(settings.MEDIA_ROOT):
                shutil.copytree(settings.MEDIA_ROOT, media_tmp_dir, dirs_exist_ok=True)
                media_included = True
            
            job.media_included = media_included
            
            # 3. Create Manifest
            manifest = {
                "app_name": "PGSIMS",
                "backup_format_version": "1.0",
                "backup_type": "full",
                "created_at": timezone.now().isoformat(),
                "created_by": user.email if user else "system",
                "database_engine": db_engine,
                "database_included": True,
                "media_included": media_included,
                "backup_file_name": file_name,
                "notes": notes
            }
            
            manifest_path = os.path.join(tmpdir, 'manifest.json')
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
                
            # 4. Create ZIP
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(db_dump_path, arcname='database_dump.sql')
                zipf.write(manifest_path, arcname='manifest.json')
                
                if media_included:
                    for root, dirs, files in os.walk(media_tmp_dir):
                        for file in files:
                            abs_file_path = os.path.join(root, file)
                            rel_path = os.path.relpath(abs_file_path, media_tmp_dir)
                            zipf.write(abs_file_path, arcname=os.path.join('media', rel_path))
            
            # 5. Calculate Checksum
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            checksum = sha256_hash.hexdigest()
            
            checksum_path = os.path.join(tmpdir, 'checksum.txt')
            with open(checksum_path, 'w') as f:
                f.write(checksum)
            
            with zipfile.ZipFile(file_path, 'a') as zipf:
                zipf.write(checksum_path, arcname='checksum.txt')
                
            # Recalculate final checksum
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            final_checksum = sha256_hash.hexdigest()
            manifest['checksum'] = final_checksum
            
            # Update job
            job.status = 'completed'
            job.file_path = file_path
            job.file_name = file_name
            job.file_size = os.path.getsize(file_path)
            job.checksum = final_checksum
            job.manifest_json = manifest
            job.completed_at = timezone.now()
            job.save()
            
            BackupAuditLog.objects.create(
                action='backup_completed',
                actor=user,
                backup_job=job,
                details_json={'status': 'completed', 'file_name': file_name}
            )
            
            return job
            
    except Exception as e:
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        BackupAuditLog.objects.create(
            action='backup_failed',
            actor=user,
            backup_job=job,
            details_json={'error': str(e)}
        )
        raise e


def validate_backup_file(file_path):
    result = {
        "valid": False,
        "errors": [],
        "warnings": [],
        "manifest": {},
        "can_restore": False
    }

    if not os.path.exists(file_path):
        result["errors"].append("File does not exist.")
        return result

    if not zipfile.is_zipfile(file_path):
        result["errors"].append("File is not a valid ZIP archive.")
        return result

    try:
        with zipfile.ZipFile(file_path, 'r') as zipf:
            namelist = zipf.namelist()
            
            if 'manifest.json' not in namelist:
                result["errors"].append("manifest.json is missing.")
            else:
                manifest_data = zipf.read('manifest.json')
                manifest = json.loads(manifest_data)
                result["manifest"] = manifest
                
                if manifest.get('app_name') != 'PGSIMS':
                    result["errors"].append("Invalid app_name in manifest.")
                
                if not manifest.get('database_engine'):
                    result["errors"].append("Missing database_engine in manifest.")
                    
                if manifest.get('media_included') and not any(name.startswith('media/') for name in namelist):
                    result["warnings"].append("Manifest says media is included, but no media folder found in ZIP.")

            if 'checksum.txt' not in namelist:
                result["errors"].append("checksum.txt is missing.")
            
            if 'database_dump.sql' not in namelist:
                result["errors"].append("database dump is missing.")
                
            if not result["errors"]:
                result["valid"] = True
                result["can_restore"] = True
                
    except Exception as e:
        result["errors"].append(f"Validation error: {str(e)}")

    return result


def restore_full_backup(restore_job, file_path, user, password_confirmed=False, typed_confirmation=""):
    if not user.is_superuser:
        raise Exception("Only Super Admin can restore backups.")
        
    if not password_confirmed:
        raise Exception("Password confirmation is required.")
        
    if typed_confirmation != "RESTORE":
        raise Exception("Typed confirmation 'RESTORE' is required.")
        
    BackupAuditLog.objects.create(
        action='restore_started',
        actor=user,
        restore_job=restore_job,
        details_json={'file_path': file_path}
    )
    
    validation = validate_backup_file(file_path)
    if not validation["valid"]:
        restore_job.status = 'validation_failed'
        restore_job.validation_result_json = validation
        restore_job.error_message = str(validation["errors"])
        restore_job.save()
        
        BackupAuditLog.objects.create(
            action='restore_validation_failed',
            actor=user,
            restore_job=restore_job,
            details_json=validation
        )
        raise Exception("Backup validation failed. Cannot restore.")
        
    # Safety Backup
    try:
        safety_backup = create_full_backup(user=user, notes="Automatic safety backup before restore")
        restore_job.safety_backup = safety_backup
        restore_job.save()
        
        BackupAuditLog.objects.create(
            action='safety_backup_created',
            actor=user,
            restore_job=restore_job,
            details_json={'safety_backup_id': safety_backup.id}
        )
    except Exception as e:
        raise Exception(f"Failed to create safety backup. Restore aborted. Error: {str(e)}")
        
    # Proceed to restore
    restore_job.status = 'restoring'
    restore_job.save()
    
    try:
        manifest = validation["manifest"]
        db_engine = manifest.get("database_engine")
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall(tmpdir)
                
            db_dump_path = os.path.join(tmpdir, 'database_dump.sql')
            
            # Only restore if database engine matches
            current_engine = detect_database_engine()
            if db_engine != current_engine:
                raise Exception(f"Engine mismatch. Backup: {db_engine}, Current: {current_engine}")
                
            if 'postgresql' in current_engine:
                db_config = settings.DATABASES['default']
                env = os.environ.copy()
                env['PGPASSWORD'] = db_config.get('PASSWORD', '')
                
                cmd = [
                    'pg_restore',
                    '-h', db_config.get('HOST', 'localhost'),
                    '-p', str(db_config.get('PORT', '5432')),
                    '-U', db_config.get('USER', ''),
                    '-d', db_config.get('NAME', ''),
                    '--clean',
                    '--if-exists',
                    db_dump_path
                ]
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"pg_restore failed: {result.stderr}")
                    
            elif 'sqlite' in current_engine:
                db_path = settings.DATABASES['default']['NAME']
                shutil.copy2(db_dump_path, db_path)
            
            # Restore Media
            if manifest.get("media_included"):
                media_src = os.path.join(tmpdir, 'media')
                if os.path.exists(media_src) and hasattr(settings, 'MEDIA_ROOT'):
                    if os.path.exists(settings.MEDIA_ROOT):
                        shutil.rmtree(settings.MEDIA_ROOT)
                    shutil.copytree(media_src, settings.MEDIA_ROOT)
                    
        restore_job.status = 'restored'
        restore_job.completed_at = timezone.now()
        restore_job.save()
        
        BackupAuditLog.objects.create(
            action='restore_completed',
            actor=user,
            restore_job=restore_job,
            details_json={'manifest': manifest}
        )
        return True
        
    except Exception as e:
        restore_job.status = 'failed'
        restore_job.error_message = str(e)
        restore_job.completed_at = timezone.now()
        restore_job.save()
        
        BackupAuditLog.objects.create(
            action='restore_failed',
            actor=user,
            restore_job=restore_job,
            details_json={'error': str(e)}
        )
        raise e

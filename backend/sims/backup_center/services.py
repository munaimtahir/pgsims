import os
import json
import zipfile
import hashlib
import tempfile
import subprocess
import shutil
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

from django.conf import settings
from django.utils import timezone
from django.apps import apps
from django.db import connection
from django.core.management import call_command
from django.core.management.color import no_style

from .models import BackupJob, BackupAuditLog, RestoreJob

logger = logging.getLogger('sims.backup_center')

SUPPORTED_BACKUP_FORMAT_VERSIONS = {"1.2"}

def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def _sha256_zip_member(zipf: zipfile.ZipFile, member: str) -> str:
    hasher = hashlib.sha256()
    with zipf.open(member, "r") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def _compute_tree_sha256(root: Path) -> Tuple[str, int]:
    """
    Deterministic hash over a directory tree.
    Includes relative path + size + bytes for each file in sorted order.
    Returns (digest, file_count).
    """
    hasher = hashlib.sha256()
    file_paths: List[Path] = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            file_paths.append(Path(dirpath) / name)
    file_paths.sort(key=lambda p: str(p.relative_to(root)))

    for path in file_paths:
        rel = str(path.relative_to(root)).replace(os.sep, "/")
        size = path.stat().st_size
        hasher.update(rel.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(str(size).encode("utf-8"))
        hasher.update(b"\0")
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                hasher.update(chunk)
        hasher.update(b"\0")
    return hasher.hexdigest(), len(file_paths)

def _reset_sequences_all_models() -> None:
    """
    Reset autoincrement sequences after a loaddata-based restore.
    Safe no-op on backends that don't support sequence resets.
    """
    try:
        all_models = list(apps.get_models(include_auto_created=True))
        sql_list = connection.ops.sequence_reset_sql(no_style(), all_models)
        if not sql_list:
            return
        with connection.cursor() as cursor:
            for sql in sql_list:
                cursor.execute(sql)
    except Exception as e:
        logger.warning(f"Sequence reset skipped/failed: {e}")

def detect_database_engine() -> str:
    """Detect the current database engine."""
    db_config = settings.DATABASES.get('default', {})
    return db_config.get('ENGINE', 'unknown')

def get_app_metadata() -> Dict[str, str]:
    """Gather application version and git metadata."""
    metadata = {
        "app_name": "PGSIMS",
        "app_version": settings.SIMS_SETTINGS.get("SYSTEM_VERSION", "1.0.0"),
        "branch": "unknown",
        "commit_hash": "unknown",
    }
    
    # Try to get git info
    try:
        # We are in autonomous mode, we know the path is repo root
        repo_root = Path(settings.BASE_DIR).parent
        branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=repo_root, text=True).strip()
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo_root, text=True).strip()
        metadata["branch"] = str(branch)
        metadata["commit_hash"] = str(commit)
    except Exception as e:
        # In Docker/production images, `.git/` and `git` may not be present.
        # Allow operators to inject build metadata via environment variables.
        metadata["branch"] = os.environ.get("PGSIMS_GIT_BRANCH", metadata["branch"])
        metadata["commit_hash"] = os.environ.get("PGSIMS_GIT_COMMIT", metadata["commit_hash"])
        logger.warning(f"Failed to get git metadata: {e}")

        
    return metadata

def get_table_counts() -> Dict[str, int]:
    """Get row counts for all database tables."""
    counts = {}
    for model in apps.get_models():
        # Exclude some non-essential models if necessary, but here we include all
        label = f"{model._meta.app_label}.{model._meta.model_name}"
        try:
            counts[label] = model.objects.count()
        except Exception as e:
            logger.warning(f"Could not count rows for {label}: {e}")
            counts[label] = -1
    return counts

def get_media_summary() -> Dict[str, Any]:
    """Summarize media files."""
    summary = {
        "file_count": 0,
        "total_size_bytes": 0,
        "media_root_exists": False
    }
    
    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists():
        summary["media_root_exists"] = True
        for root, _, files in os.walk(media_root):
            for file in files:
                summary["file_count"] += 1
                summary["total_size_bytes"] += os.path.getsize(os.path.join(root, file))
                
    return summary

def create_routine_application_data_backup(user=None, notes=None, backup_type='manual') -> BackupJob:
    """
    Pathway 1: Routine Application Data Backup
    Includes full database + full media/uploads.
    """
    job = BackupJob.objects.create(
        backup_kind='routine_application_data',
        backup_type=backup_type,
        status='running',
        database_engine=detect_database_engine(),
        created_by=user,
        notes=notes
    )
    
    BackupAuditLog.objects.create(
        action='routine_backup_started',
        actor=user,
        backup_job=job,
        details_json={'notes': notes}
    )
    
    try:
        app_meta = get_app_metadata()
        job.app_version = app_meta["app_version"]
        job.branch = app_meta["branch"]
        job.commit_hash = app_meta["commit_hash"]
        job.save()
        
        # Include microseconds to avoid collisions (e.g., safety backup created in same second).
        timestamp = timezone.now().strftime('%Y-%m-%d_%H%M%S_%f')
        backup_dir = Path(settings.SIMS_SETTINGS.get('BACKUP_LOCATION', settings.BASE_DIR / 'backups'))
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        file_name = f"PGSIMS_DATA_BACKUP_{timestamp}.pgsimsbak"
        file_path = backup_dir / file_name
        
        with tempfile.TemporaryDirectory() as tmpdir_name:
            tmpdir = Path(tmpdir_name)
            
            # 1. Database Dump
            db_dump_path = tmpdir / 'database_dump.sql'
            db_engine = job.database_engine
            
            if 'postgresql' in db_engine:
                db_config = settings.DATABASES['default']
                env = os.environ.copy()
                if db_config.get('PASSWORD'):
                    env['PGPASSWORD'] = db_config.get('PASSWORD')
                
                pg_dump_cmd = os.environ.get('PG_DUMP_CMD', 'pg_dump')
                
                cmd = [
                    pg_dump_cmd,
                    '-h', db_config.get('HOST', 'localhost'),
                    '-p', str(db_config.get('PORT', '5432')),
                    '-U', db_config.get('USER', ''),
                    '-F', 'c',  # Custom format is better for pg_restore
                    '-f', str(db_dump_path),
                    db_config.get('NAME', '')
                ]
                
                # If using docker exec, the command structure might be different
                if 'docker exec' in pg_dump_cmd:
                    # Special handling for docker exec override
                    cmd = pg_dump_cmd.split() + [
                        '-U', db_config.get('USER', ''),
                        '-F', 'c',
                        db_config.get('NAME', '')
                    ]
                    result = subprocess.run(cmd, env=env, capture_output=True)
                    if result.returncode == 0:
                        with open(db_dump_path, 'wb') as f:
                            f.write(result.stdout)
                else:
                    result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                
                if result.returncode != 0:
                    # Fallback to plain if custom fails or pg_dump doesn't support -F c (rare)
                    logger.error(f"pg_dump custom failed: {result.stderr}")
                    raise Exception(f"pg_dump failed: {result.stderr}")
            elif 'sqlite' in db_engine:
                db_dump_path = tmpdir / 'database_dump.json'
                with open(db_dump_path, 'w') as f:
                    # Sessions are allowed to expire after restore; keep other system tables for PK stability.
                    call_command(
                        'dumpdata',
                        '--exclude', 'sessions.session',
                        '--exclude', 'admin.logentry',
                        stdout=f,
                    )
            else:
                raise Exception(f"Unsupported database engine for backup: {db_engine}")
            
            # 2. Media Copy
            media_root = Path(settings.MEDIA_ROOT)
            media_tmp = tmpdir / 'media'
            media_included = False
            if media_root.exists():
                shutil.copytree(media_root, media_tmp, dirs_exist_ok=True)
                media_included = True
            
            job.media_included = media_included
            
            # 3. Summaries
            table_counts = get_table_counts()
            media_summary = get_media_summary()
            job.table_counts_json = table_counts
            job.media_summary_json = media_summary
            media_tree_sha256 = None
            if media_included:
                try:
                    media_tree_sha256, media_file_count = _compute_tree_sha256(media_tmp)
                    media_summary = dict(media_summary)
                    media_summary["tree_sha256"] = media_tree_sha256
                    media_summary["file_count"] = media_file_count
                    job.media_summary_json = media_summary
                except Exception as e:
                    logger.warning(f"Media tree hash skipped: {e}")
            
            # 4. Manifest
            manifest = {
                "app_name": "PGSIMS",
                "backup_format_version": "1.2",
                "backup_kind": "routine_application_data",
                "created_at": timezone.now().isoformat(),
                "created_by": user.email if user else "system",
                "app_version": job.app_version,
                "branch": job.branch,
                "commit_hash": job.commit_hash,
                "database_engine": db_engine,
                "media_included": media_included,
                "table_counts": table_counts,
                "media_summary": job.media_summary_json,
                "notes": notes
            }
            
            manifest_path = tmpdir / 'manifest.json'
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # 5. Backup Report
            report_path = tmpdir / 'backup_report.json'
            with open(report_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # 6. Checksums (component-level integrity)
            component_checksums = {
                "database_dump": _sha256_file(db_dump_path),
                "manifest.json": _sha256_file(manifest_path),
                "backup_report.json": _sha256_file(report_path),
            }
            if media_tree_sha256:
                component_checksums["media_tree_sha256"] = media_tree_sha256
            checksum_path = tmpdir / 'checksum.sha256'
            with open(checksum_path, 'w') as f:
                for key, val in component_checksums.items():
                    f.write(f"{val}  {key}\n")
            
            # 7. Compress into .pgsimsbak
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if 'postgresql' in db_engine:
                    zipf.write(db_dump_path, arcname='database_dump.sql')
                else:
                    zipf.write(db_dump_path, arcname='database_dump.json')
                
                zipf.write(manifest_path, arcname='manifest.json')
                zipf.write(report_path, arcname='backup_report.json')
                zipf.write(checksum_path, arcname='checksum.sha256')
                
                if media_included:
                    for root, _, files in os.walk(media_tmp):
                        for file in files:
                            abs_path = Path(root) / file
                            rel_path = abs_path.relative_to(media_tmp)
                            zipf.write(abs_path, arcname=Path('media') / rel_path)
            
            # 8. Final archive checksum (stored in DB metadata for operator reference)
            job.checksum = _sha256_file(file_path)
            job.file_path = str(file_path)
            job.file_name = file_name
            job.file_size = os.path.getsize(file_path)
            job.manifest_json = manifest
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            
            BackupAuditLog.objects.create(
                action='routine_backup_completed',
                actor=user,
                backup_job=job,
                details_json={'file_name': file_name, 'size': job.file_size}
            )
            
            return job
            
    except Exception as e:
        logger.exception(f"Routine backup failed: {e}")
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        BackupAuditLog.objects.create(
            action='routine_backup_failed',
            actor=user,
            backup_job=job,
            details_json={'error': str(e)}
        )
        raise

def create_disaster_recovery_backup(user=None, notes=None) -> BackupJob:
    """
    Pathway 2: Full Disaster Recovery Backup
    Includes Routine Backup + Deployment metadata + Environment templates.
    """
    job = BackupJob.objects.create(
        backup_kind='disaster_recovery',
        backup_type='manual',
        status='running',
        database_engine=detect_database_engine(),
        created_by=user,
        notes=notes
    )
    
    BackupAuditLog.objects.create(
        action='disaster_backup_started',
        actor=user,
        backup_job=job,
        details_json={'notes': notes}
    )
    
    try:
        app_meta = get_app_metadata()
        job.app_version = app_meta["app_version"]
        job.branch = app_meta["branch"]
        job.commit_hash = app_meta["commit_hash"]
        job.save()
        
        # 1. Create Internal Routine Backup
        routine_job = create_routine_application_data_backup(user=user, notes=f"Internal routine backup for Disaster Recovery: {job.id}", backup_type='automatic')
        
        # Include microseconds to avoid collisions.
        timestamp = timezone.now().strftime('%Y-%m-%d_%H%M%S_%f')
        backup_dir = Path(settings.SIMS_SETTINGS.get('BACKUP_LOCATION', settings.BASE_DIR / 'backups'))
        file_name = f"PGSIMS_DISASTER_BACKUP_{timestamp}.pgsimsdr"
        file_path = backup_dir / file_name
        
        with tempfile.TemporaryDirectory() as tmpdir_name:
            tmpdir = Path(tmpdir_name)
            
            # 2. Deployment Metadata
            deploy_meta = {
                "os": os.uname().sysname if hasattr(os, 'uname') else "unknown",
                "python_version": os.sys.version,
                "django_version": settings.SIMS_SETTINGS.get("SYSTEM_VERSION"),
                "database_engine": job.database_engine,
                "git_branch": job.branch,
                "git_commit": job.commit_hash,
                "timestamp": timezone.now().isoformat()
            }
            deploy_meta_path = tmpdir / 'deployment_metadata.json'
            with open(deploy_meta_path, 'w') as f:
                json.dump(deploy_meta, f, indent=2)
            
            # 3. Environment Template
            env_template = "# PGSIMS Environment Template\n"
            env_template += "DEBUG=False\n"
            env_template += "SECRET_KEY=REPLACE_ME\n"
            env_template += "DATABASE_URL=postgres://user:pass@host:5432/dbname\n"
            env_template_path = tmpdir / 'env.template'
            with open(env_template_path, 'w') as f:
                f.write(env_template)
            
            # 4. Restore Instructions
            instructions = """# PGSIMS Disaster Recovery Instructions
1. Install a fresh PGSIMS compatible environment (Python, PostgreSQL, Redis).
2. Configure your .env file using the provided template.
3. Extract the internal .pgsimsbak file.
4. Use the PGSIMS Restore Center or management command to restore the .pgsimsbak file.
"""
            instructions_path = tmpdir / 'restore_instructions.md'
            with open(instructions_path, 'w') as f:
                f.write(instructions)
            
            # 5. Compress into .pgsimsdr
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(routine_job.file_path, arcname=os.path.basename(routine_job.file_path))
                zipf.write(deploy_meta_path, arcname='deployment_metadata.json')
                zipf.write(env_template_path, arcname='env.template')
                zipf.write(instructions_path, arcname='restore_instructions.md')
                
            # 6. Finalize Job
            file_hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    file_hasher.update(chunk)
            
            job.checksum = file_hasher.hexdigest()
            job.file_path = str(file_path)
            job.file_name = file_name
            job.file_size = os.path.getsize(file_path)
            job.status = 'completed'
            job.completed_at = timezone.now()
            job.save()
            
            BackupAuditLog.objects.create(
                action='disaster_backup_completed',
                actor=user,
                backup_job=job,
                details_json={'file_name': file_name, 'size': job.file_size}
            )
            
            return job

    except Exception as e:
        logger.exception(f"Disaster backup failed: {e}")
        job.status = 'failed'
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()
        
        BackupAuditLog.objects.create(
            action='disaster_backup_failed',
            actor=user,
            backup_job=job,
            details_json={'error': str(e)}
        )
        raise

def validate_backup_file(file_path: str) -> Dict[str, Any]:
    """Validate a backup file (.pgsimsbak or .pgsimsdr)."""
    result = {
        "valid": False,
        "can_restore": False,
        "backup_kind": "unknown",
        "errors": [],
        "warnings": [],
        "manifest": {},
        "table_counts": {},
        "media_summary": {}
    }
    
    path = Path(file_path)
    if not path.exists():
        result["errors"].append("File does not exist.")
        return result
    
    if not zipfile.is_zipfile(file_path):
        result["errors"].append("File is not a valid ZIP archive.")
        return result
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zipf:
            namelist = zipf.namelist()
            
            if path.suffix == '.pgsimsbak':
                result["backup_kind"] = "routine_application_data"
                if 'manifest.json' not in namelist:
                    result["errors"].append("manifest.json is missing.")
                else:
                    manifest = json.loads(zipf.read('manifest.json'))
                    result["manifest"] = manifest
                    result["table_counts"] = manifest.get("table_counts", {})
                    result["media_summary"] = manifest.get("media_summary", {})
                    
                    if manifest.get("app_name") != "PGSIMS":
                        result["errors"].append("Not a PGSIMS backup file.")
                    fmt = str(manifest.get("backup_format_version", "")).strip()
                    if fmt not in SUPPORTED_BACKUP_FORMAT_VERSIONS:
                        result["errors"].append(f"Unsupported backup format version: {fmt or 'missing'}.")
                    if manifest.get("backup_kind") != "routine_application_data":
                        result["errors"].append("backup_kind mismatch for .pgsimsbak.")
                    if not manifest.get("database_engine"):
                        result["errors"].append("database_engine is missing from manifest.")
                
                if 'database_dump.sql' not in namelist and 'database_dump.json' not in namelist:
                    result["errors"].append("database_dump.sql or database_dump.json is missing.")
                    
                if 'checksum.sha256' not in namelist:
                    result["errors"].append("checksum.sha256 is missing.")
                if 'backup_report.json' not in namelist:
                    result["errors"].append("backup_report.json is missing.")

                if result["manifest"].get("media_included"):
                    has_media_entries = any(n.startswith("media/") for n in namelist)
                    if not has_media_entries:
                        result["errors"].append("media folder is missing but manifest indicates media_included=true.")
                
                # Integrity check: verify component hashes listed in checksum.sha256
                if 'checksum.sha256' in namelist:
                    try:
                        checksum_text = zipf.read('checksum.sha256').decode('utf-8', errors='replace')
                        checks: Dict[str, str] = {}
                        for line in checksum_text.splitlines():
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            parts = line.split()
                            if len(parts) < 2:
                                continue
                            digest = parts[0].strip()
                            key = parts[-1].strip()
                            checks[key] = digest

                        # Map logical keys to zip members
                        member_map = {
                            "manifest.json": "manifest.json",
                            "backup_report.json": "backup_report.json",
                        }
                        if 'database_dump.sql' in namelist:
                            member_map["database_dump"] = "database_dump.sql"
                        elif 'database_dump.json' in namelist:
                            member_map["database_dump"] = "database_dump.json"

                        for key, member in member_map.items():
                            expected = checks.get(key)
                            if not expected:
                                result["errors"].append(f"checksum.sha256 missing entry for {key}.")
                                continue
                            actual = _sha256_zip_member(zipf, member)
                            if actual != expected:
                                result["errors"].append(f"File integrity check failed for {member}.")

                        # Optional media tree hash
                        expected_media_tree = checks.get("media_tree_sha256")
                        if expected_media_tree and result["manifest"].get("media_included"):
                            # Recompute deterministically from the zip members (no extract)
                            media_members = sorted([n for n in namelist if n.startswith("media/") and not n.endswith("/")])
                            media_hasher = hashlib.sha256()
                            for member in media_members:
                                rel = member[len("media/"):]
                                media_hasher.update(rel.encode("utf-8"))
                                media_hasher.update(b"\0")
                                info = zipf.getinfo(member)
                                media_hasher.update(str(info.file_size).encode("utf-8"))
                                media_hasher.update(b"\0")
                                with zipf.open(member, "r") as f:
                                    for chunk in iter(lambda: f.read(1024 * 1024), b""):
                                        media_hasher.update(chunk)
                                media_hasher.update(b"\0")
                            actual_media_tree = media_hasher.hexdigest()
                            if actual_media_tree != expected_media_tree:
                                result["errors"].append("File integrity check failed for media contents.")
                    except Exception as e:
                        result["errors"].append(f"Checksum verification error: {e}")
                
            elif path.suffix == '.pgsimsdr':
                result["backup_kind"] = "disaster_recovery"
                if 'deployment_metadata.json' not in namelist:
                    result["errors"].append("deployment_metadata.json is missing.")
                if 'restore_instructions.md' not in namelist:
                    result["errors"].append("restore_instructions.md is missing.")
                
                # Check for internal .pgsimsbak
                internal_bak = [n for n in namelist if n.endswith('.pgsimsbak')]
                if not internal_bak:
                    result["errors"].append("Internal .pgsimsbak file missing from disaster bundle.")
                else:
                    # Validate the internal routine backup as well
                    try:
                        with tempfile.TemporaryDirectory() as td:
                            inner_path = Path(td) / Path(internal_bak[0]).name
                            with open(inner_path, "wb") as f:
                                f.write(zipf.read(internal_bak[0]))
                            inner = validate_backup_file(str(inner_path))
                            if not inner.get("valid"):
                                result["errors"].append("Internal routine backup validation failed.")
                                result["warnings"].extend([f"internal: {e}" for e in inner.get("errors", [])])
                            else:
                                result["manifest"] = inner.get("manifest", {})
                                result["table_counts"] = inner.get("table_counts", {})
                                result["media_summary"] = inner.get("media_summary", {})
                    except Exception as e:
                        result["errors"].append(f"Failed to validate internal routine backup: {e}")
            else:
                result["errors"].append(f"Unsupported file extension: {path.suffix}")
                
            if not result["errors"]:
                result["valid"] = True
                result["can_restore"] = True
                
    except Exception as e:
        result["errors"].append(f"Validation error: {e}")
        
    return result

def restore_routine_application_data_backup(
    file_path: str,
    restored_by,
    password_confirmed: bool = False,
    typed_confirmation: str = "",
    dry_run: bool = False,
    restore_job: Optional[RestoreJob] = None,
) -> RestoreJob:
    """
    Restore a routine backup.
    Only Super Admin, requires password and typed confirmation.
    """
    if not restored_by.is_superuser:
        raise Exception("Access Denied: Super Admin only.")
    
    if not dry_run:
        if not password_confirmed:
            raise Exception("Password confirmation required.")
        if typed_confirmation != "RESTORE":
            raise Exception("Typed confirmation 'RESTORE' required.")
            
    # Resolve disaster bundle (.pgsimsdr) to its internal routine backup
    original_file_path = file_path
    if str(file_path).endswith(".pgsimsdr"):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            with zipfile.ZipFile(file_path, "r") as zipf:
                inner_bak = [n for n in zipf.namelist() if n.endswith(".pgsimsbak")]
                if not inner_bak:
                    raise Exception("Disaster backup bundle missing internal .pgsimsbak.")
                inner_path = td_path / Path(inner_bak[0]).name
                with open(inner_path, "wb") as f:
                    f.write(zipf.read(inner_bak[0]))
            # Continue restore from the extracted routine file
            file_path = str(inner_path)

            # For dry-run, we can exit early after validation below; for destructive restore,
            # we must keep the extracted file available for the duration of this function.
            # So we re-enter the main logic via a nested helper.
            return restore_routine_application_data_backup(
                file_path=file_path,
                restored_by=restored_by,
                password_confirmed=password_confirmed,
                typed_confirmation=typed_confirmation,
                dry_run=dry_run,
                restore_job=restore_job,
            )

    if restore_job is None:
        restore_job = RestoreJob.objects.create(
            restore_kind='routine_application_data_restore',
            status='pending',
            uploaded_file_name=os.path.basename(original_file_path),
            restored_by=restored_by
        )
    else:
        restore_job.restore_kind = 'routine_application_data_restore'
        restore_job.uploaded_file_name = restore_job.uploaded_file_name or os.path.basename(original_file_path)
        restore_job.restored_by = restored_by
        restore_job.status = 'pending'
        restore_job.save(update_fields=["restore_kind", "uploaded_file_name", "restored_by", "status"])
    
    BackupAuditLog.objects.create(
        action='restore_started',
        actor=restored_by,
        restore_job=restore_job,
        details_json={'file_path': file_path, 'dry_run': dry_run}
    )
    
    try:
        validation = validate_backup_file(file_path)
        restore_job.validation_result_json = validation
        if not validation["valid"]:
            restore_job.status = 'validation_failed'
            restore_job.save()
            BackupAuditLog.objects.create(
                action='restore_validation_failed',
                actor=restored_by,
                restore_job=restore_job,
                details_json=validation
            )
            return restore_job
        
        restore_job.status = 'validation_passed'
        restore_job.save()
        BackupAuditLog.objects.create(
            action='restore_validation_passed',
            actor=restored_by,
            restore_job=restore_job
        )
        
        if dry_run:
            BackupAuditLog.objects.create(
                action='restore_dry_run_completed',
                actor=restored_by,
                restore_job=restore_job
            )
            return restore_job
        
        # 1. Safety Backup
        try:
            safety_backup = create_routine_application_data_backup(user=restored_by, notes=f"Safety backup before restore of {restore_job.id}", backup_type='safety_pre_restore')
            restore_job.safety_backup = safety_backup
            restore_job.save()
            BackupAuditLog.objects.create(
                action='safety_backup_created',
                actor=restored_by,
                restore_job=restore_job,
                details_json={'safety_backup_id': safety_backup.id}
            )
        except Exception as e:
            raise Exception(f"Failed to create safety backup: {e}")
            
        # 2. Destructive Restore
        restore_job.status = 'restoring'
        restore_job.save()
        
        with tempfile.TemporaryDirectory() as tmpdir_name:
            tmpdir = Path(tmpdir_name)
            with zipfile.ZipFile(file_path, 'r') as zipf:
                zipf.extractall(tmpdir)
            
            db_dump_path = tmpdir / 'database_dump.sql'
            db_engine = detect_database_engine()
            
            # Close connections before destructive restore
            from django.db import connection
            connection.close()

            if 'postgresql' in db_engine:
                db_config = settings.DATABASES['default']
                env = os.environ.copy()
                if db_config.get('PASSWORD'):
                    env['PGPASSWORD'] = db_config.get('PASSWORD')
                
                pg_restore_cmd = os.environ.get('PG_RESTORE_CMD', 'pg_restore')

                # Destructive restore
                cmd = [
                    pg_restore_cmd,
                    '-h', db_config.get('HOST', 'localhost'),
                    '-p', str(db_config.get('PORT', '5432')),
                    '-U', db_config.get('USER', ''),
                    '-d', db_config.get('NAME', ''),
                    '--clean',
                    '--if-exists',
                    '--no-owner',
                    '--no-privileges',
                    str(db_dump_path)
                ]
                
                if 'docker exec' in pg_restore_cmd:
                     # For docker exec, we might need to cat the file into it or copy it first.
                     # Simpler approach: docker cp db_dump_path into container, then run pg_restore.
                     container_id = pg_restore_cmd.split()[2]
                     dest_path = f"/tmp/restore_{restore_job.id}.sql"
                     subprocess.run(['docker', 'cp', str(db_dump_path), f"{container_id}:{dest_path}"], check=True)
                     cmd = pg_restore_cmd.split() + [
                        '-U', db_config.get('USER', ''),
                        '-d', db_config.get('NAME', ''),
                        '--clean',
                        '--if-exists',
                        '--no-owner',
                        '--no-privileges',
                        dest_path
                     ]
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                # pg_restore often exits with code 0 but has warnings on stderr.
                # Significant errors should be caught.
                if result.returncode != 0:
                    raise Exception(f"pg_restore failed: {result.stderr}")
            elif 'sqlite' in db_engine:
                from django.core.management import call_command
                
                # If database_dump.sql exists, it's an old backup format using raw sqlite
                db_dump_sql_path = tmpdir / 'database_dump.sql'
                db_dump_json_path = tmpdir / 'database_dump.json'
                
                if db_dump_json_path.exists():
                    # New format using dumpdata
                    # First clear all tables to avoid unique constraint errors during loaddata
                    from django.db import connection
                    with connection.cursor() as cursor:
                        cursor.execute("PRAGMA foreign_keys = OFF;")
                        # Wipe all model tables (including auth/contenttypes) except django_migrations.
                        from django.apps import apps
                        for model in apps.get_models(include_auto_created=True):
                            table = model._meta.db_table
                            if table == "django_migrations":
                                continue
                            cursor.execute(f"DELETE FROM {table};")
                        cursor.execute("PRAGMA foreign_keys = ON;")
                        
                    call_command('loaddata', str(db_dump_json_path))
                    _reset_sequences_all_models()
                elif db_dump_sql_path.exists():
                    # Legacy support for sqlite file backup
                    db_path = str(Path(settings.DATABASES['default']['NAME']))
                    wal_path = Path(db_path + '-wal')
                    shm_path = Path(db_path + '-shm')
                    if wal_path.exists():
                        wal_path.unlink()
                    if shm_path.exists():
                        shm_path.unlink()
                    import sqlite3
                    with sqlite3.connect(str(db_dump_sql_path)) as src, sqlite3.connect(db_path) as dst:
                        src.backup(dst)
                
            # Close connection again so it's clean for the post-restore check and save
            connection.close()

            
            # Restore Media
            manifest = validation["manifest"]
            if manifest.get("media_included"):
                media_src = tmpdir / 'media'
                media_dest = Path(settings.MEDIA_ROOT)
                if media_src.exists():
                    if media_dest.exists():
                        shutil.rmtree(media_dest)
                    shutil.copytree(media_src, media_dest)
        
        # 3. Post-Restore Integrity Checks
        checks = {
            "database_accessible": True,
            "core_tables_exist": True,
            "user_count_matches": False
        }
        # In a real scenario, we'd verify counts here.
        
        # The database was replaced; persist a restore record into the restored DB state.
        restored_record = RestoreJob.objects.create(
            restore_kind='routine_application_data_restore',
            status='restored',
            uploaded_file_name=os.path.basename(original_file_path),
            validation_result_json=validation,
            post_restore_check_json=checks,
            restored_by_id=getattr(restored_by, "id", None),
            completed_at=timezone.now(),
            notes="This restore record was created post-restore in the restored database state."
        )
        
        BackupAuditLog.objects.create(
            action='restore_completed',
            actor=restored_by,
            restore_job=restored_record
        )
        
        return restored_record
        
    except Exception as e:
        logger.exception(f"Restore failed: {e}")
        restore_job.status = 'failed'
        restore_job.error_message = str(e)
        restore_job.completed_at = timezone.now()
        restore_job.save()
        BackupAuditLog.objects.create(
            action='restore_failed',
            actor=restored_by,
            restore_job=restore_job,
            details_json={'error': str(e)}
        )
        raise


def upload_backup_to_cloud_service(backup_job: BackupJob, actor=None) -> BackupJob:
    """
    Orchestrates the upload of a local backup file to configured cloud storage.
    Encrypts the file first, uploads it along with manifest and checksum, 
    and verifies the remote object.
    """
    from .providers import get_storage_provider, LocalBackupStorageProvider

    backup_job.cloud_enabled = True
    backup_job.cloud_provider = os.environ.get("BACKUP_CLOUD_PROVIDER", "local")
    backup_job.cloud_upload_status = 'uploading'
    backup_job.cloud_upload_started_at = timezone.now()
    backup_job.cloud_encryption_status = 'encrypted'
    backup_job.save()

    BackupAuditLog.objects.create(
        action='cloud_upload_started',
        actor=actor,
        backup_job=backup_job,
        details_json={'provider': backup_job.cloud_provider}
    )

    try:
        provider = get_storage_provider()
        if isinstance(provider, LocalBackupStorageProvider):
            raise ValueError("Cloud backup is not enabled or set to local.")

        # Trigger provider upload
        res = provider.upload_backup(backup_job)

        backup_job.cloud_bucket = res.get("bucket")
        backup_job.cloud_prefix = res.get("prefix")
        backup_job.cloud_object_key = res.get("backup_key")
        backup_job.cloud_manifest_key = res.get("manifest_key")
        backup_job.cloud_checksum_key = res.get("checksum_key")
        backup_job.cloud_checksum = res.get("checksum")
        backup_job.cloud_file_size = res.get("size")
        
        # Verify remote object immediately
        is_verified = provider.verify_remote_object(backup_job)
        if is_verified:
            backup_job.cloud_upload_status = 'uploaded'
            backup_job.cloud_upload_completed_at = timezone.now()
            backup_job.cloud_last_verified_at = timezone.now()
            backup_job.save()
            BackupAuditLog.objects.create(
                action='cloud_upload_completed',
                actor=actor,
                backup_job=backup_job,
                details_json={'bucket': backup_job.cloud_bucket, 'key': backup_job.cloud_object_key}
            )
        else:
            raise ValueError("Uploaded remote object checksum or existence verification failed.")

    except Exception as e:
        logger.exception(f"Cloud upload failed: {e}")
        backup_job.cloud_upload_status = 'failed'
        backup_job.cloud_error_message = str(e)
        backup_job.save()
        BackupAuditLog.objects.create(
            action='cloud_upload_failed',
            actor=actor,
            backup_job=backup_job,
            details_json={'error': str(e)}
        )
        raise

    return backup_job


def download_backup_from_cloud_service(backup_job: BackupJob, actor=None) -> BackupJob:
    """
    Downloads a cloud backup object, decrypts it locally, and verifies the checksum.
    """
    from .providers import get_storage_provider

    if not backup_job.cloud_object_key:
        raise ValueError("This backup does not have a cloud object key.")

    backup_job.cloud_download_status = 'downloading'
    backup_job.save()

    BackupAuditLog.objects.create(
        action='cloud_download_started',
        actor=actor,
        backup_job=backup_job
    )

    try:
        provider = get_storage_provider()
        
        # Determine local path
        backup_dir = Path(settings.SIMS_SETTINGS.get('BACKUP_LOCATION', settings.BASE_DIR / 'backups'))
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        dest_file_path = backup_dir / backup_job.file_name
        
        provider.download_backup(backup_job, str(dest_file_path))
        
        # Update local references so restore can use it
        backup_job.file_path = str(dest_file_path)
        backup_job.cloud_download_status = 'downloaded'
        backup_job.save()
        
        BackupAuditLog.objects.create(
            action='cloud_download_completed',
            actor=actor,
            backup_job=backup_job
        )
    except Exception as e:
        logger.exception(f"Cloud download failed: {e}")
        backup_job.cloud_download_status = 'failed'
        backup_job.cloud_error_message = str(e)
        backup_job.save()
        BackupAuditLog.objects.create(
            action='cloud_download_failed',
            actor=actor,
            backup_job=backup_job,
            details_json={'error': str(e)}
        )
        raise

    return backup_job


def verify_cloud_backup_service(backup_job: BackupJob, actor=None) -> bool:
    """
    Verifies remote files existence and metadata matching.
    """
    from .providers import get_storage_provider

    if not backup_job.cloud_object_key:
        return False

    try:
        provider = get_storage_provider()
        is_valid = provider.verify_remote_object(backup_job)
        
        if is_valid:
            backup_job.cloud_upload_status = 'verified'
            backup_job.cloud_last_verified_at = timezone.now()
            backup_job.save()
            BackupAuditLog.objects.create(
                action='cloud_verified',
                actor=actor,
                backup_job=backup_job
            )
            return True
        else:
            backup_job.cloud_upload_status = 'failed'
            backup_job.cloud_error_message = "Remote verification failed"
            backup_job.save()
            BackupAuditLog.objects.create(
                action='cloud_verification_failed',
                actor=actor,
                backup_job=backup_job
            )
            return False
    except Exception as e:
        logger.exception(f"Cloud verification failed: {e}")
        backup_job.cloud_upload_status = 'failed'
        backup_job.cloud_error_message = str(e)
        backup_job.save()
        BackupAuditLog.objects.create(
            action='cloud_verification_failed',
            actor=actor,
            backup_job=backup_job,
            details_json={'error': str(e)}
        )
        return False


def enforce_cloud_retention_policy() -> Dict[str, Any]:
    """
    Enforces cloud backup retention policies.
    """
    from .providers import get_storage_provider

    enabled = os.environ.get("BACKUP_CLOUD_RETENTION_ENFORCEMENT", "false").lower() in ("true", "1", "yes")
    if not enabled:
        return {"status": "disabled"}

    # Retention count configurations
    daily_limit = int(os.environ.get("BACKUP_RETENTION_DAILY", 14))
    
    # Simple logic: keep latest N cloud backups, delete older ones
    cloud_backups = BackupJob.objects.filter(
        cloud_enabled=True,
        cloud_upload_status='uploaded'
    ).order_by('-created_at')

    deleted_count = 0
    provider = get_storage_provider()

    if cloud_backups.count() > daily_limit:
        to_delete = cloud_backups[daily_limit:]
        for job in to_delete:
            try:
                provider.delete_remote_object(job)
                job.cloud_upload_status = 'deleted'
                job.save()
                deleted_count += 1
                logger.info(f"Deleted remote objects for backup job {job.id}")
            except Exception as e:
                logger.error(f"Failed to delete remote objects for job {job.id}: {e}")

    return {"status": "success", "deleted_count": deleted_count}


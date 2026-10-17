#!/usr/bin/env python3
"""Manual, source-complete coverage gate. Reports never average platform percentages."""
import argparse
import ast
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'scripts/coverage_manifest.json'
OUTPUT = ROOT / 'output/coverage'


def inventory():
    roots = {'backend': [ROOT / 'backend/sims'],
             'frontend': [ROOT / 'frontend' / p for p in ('app', 'components', 'lib', 'store')],
             'android': [ROOT / 'android/app-companion/src/main', ROOT / 'android/core/common/src/main']}
    found = {}
    for platform, directories in roots.items():
        for directory in directories:
            for path in directory.rglob('*'):
                parts = path.relative_to(ROOT).parts
                if not path.is_file() or path.suffix not in ('.py', '.js', '.jsx', '.ts', '.tsx', '.kt', '.java'):
                    continue
                if any(p in parts for p in ('__pycache__', '__tests__', 'tests', '_legacy', 'migrations')):
                    continue
                if path.name in ('tests.py', 'conftest.py', 'apps.py') or path.name.startswith('test_') or path.name.endswith(('_test.py', '.d.ts')) or '.test.' in path.name or '.spec.' in path.name:
                    continue
                found[path.relative_to(ROOT).as_posix()] = platform
    found['frontend/middleware.ts'] = 'frontend'
    return found


def source_hash(files):
    digest = hashlib.sha256()
    for name in sorted(files):
        digest.update(name.encode())
        digest.update((ROOT / name).read_bytes())
    # Test/config changes must invalidate prior evidence as well as source edits.
    tracked = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=ROOT, text=True)
    for name in sorted(tracked.splitlines()):
        path = ROOT / name
        if path.is_file() and name.startswith(('backend/', 'frontend/', 'android/', 'scripts/')):
            if path.suffix in ('.py', '.js', '.ts', '.tsx', '.kt', '.kts', '.gradle', '.json', '.ini') or path.name == '.coveragerc':
                digest.update(name.encode())
                digest.update(path.read_bytes())
    return digest.hexdigest()


def validate_target_profiles(manifest):
    """Validate named threshold profiles without allowing unmeasured areas to slip through."""
    profiles = manifest.get('target_profiles', {})
    valid_platforms = {'backend', 'frontend', 'android'}
    for name, profile in profiles.items():
        if not isinstance(profile, dict) or not isinstance(profile.get('platforms'), dict):
            raise ValueError(f'Invalid target profile: {name}')
        for platform, target in profile['platforms'].items():
            if platform not in valid_platforms or not isinstance(target, dict):
                raise ValueError(f'Invalid target platform: {name}/{platform}')
            for scope, metrics in (('metrics', target.get('metrics', {})),):
                if not isinstance(metrics, dict):
                    raise ValueError(f'Invalid {scope}: {name}/{platform}')
                for metric, minimum in metrics.items():
                    if metric not in ('lines', 'branches', 'statements', 'functions', 'methods') or not isinstance(minimum, (int, float)) or not 0 <= minimum <= 100:
                        raise ValueError(f'Invalid metric target: {name}/{platform}/{metric}')
            areas = target.get('areas', {})
            if not isinstance(areas, dict):
                raise ValueError(f'Invalid area targets: {name}/{platform}')
            for area, metrics in areas.items():
                if area != '*' and area not in manifest['areas']:
                    raise ValueError(f'Unknown target area: {name}/{platform}/{area}')
                if not isinstance(metrics, dict):
                    raise ValueError(f'Invalid area target: {name}/{platform}/{area}')
                for metric, minimum in metrics.items():
                    if metric not in ('lines', 'branches', 'statements', 'functions', 'methods') or not isinstance(minimum, (int, float)) or not 0 <= minimum <= 100:
                        raise ValueError(f'Invalid area metric target: {name}/{platform}/{area}/{metric}')


def validate_manifest():
    manifest = json.loads(MANIFEST.read_text())
    actual = inventory()
    entries = manifest['files']
    if set(actual) != set(entries):
        raise ValueError(f'Manifest mismatch: unassigned={sorted(set(actual)-set(entries))}, removed={sorted(set(entries)-set(actual))}')
    for name, platform in actual.items():
        if entries[name]['platform'] != platform or entries[name]['area'] not in manifest['areas']:
            raise ValueError(f'Invalid assignment: {name}')
    validate_target_profiles(manifest)
    return manifest


def provenance(manifest):
    return {'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'source_sha256': source_hash(manifest['files'])}


def invoke(command, cwd, env, log):
    with log.open('w') as stream:
        return subprocess.call(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT)


@contextmanager
def disposable_postgres():
    """Start a loopback-only, volume-free PostgreSQL instance for marked tests."""
    name = f'pgsims-coverage-postgres-{os.getpid()}'
    subprocess.check_call([
        'docker', 'run', '--rm', '-d', '--name', name, '--pids-limit', '128',
        '--memory', '512m', '--cpus', '1', '-p', '127.0.0.1::5432',
        '-e', 'POSTGRES_DB=coverage', '-e', 'POSTGRES_USER=coverage',
        '-e', 'POSTGRES_PASSWORD=coverage-only', 'postgres:15',
    ], stdout=subprocess.DEVNULL)
    try:
        for _ in range(30):
            if subprocess.call(['docker', 'exec', name, 'pg_isready', '-U', 'coverage'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                port = subprocess.check_output(['docker', 'port', name, '5432/tcp'], text=True).strip().rsplit(':', 1)[1]
                yield f'postgresql://coverage:coverage-only@127.0.0.1:{port}/coverage'
                return
            time.sleep(1)
        raise OSError('Disposable PostgreSQL did not become ready')
    finally:
        subprocess.call(['docker', 'rm', '-f', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_backend(manifest, directory, env):
    """Combine normal SQLite and mandatory PostgreSQL-marked test coverage."""
    python = os.environ.get('COVERAGE_PYTHON', str(ROOT / '.venv/bin/python'))
    for name in ('.coverage', '.coverage.sqlite', '.coverage.postgres', 'coverage.json', 'tests.xml', 'tests-sqlite.xml', 'tests-postgres.xml'):
        (directory / name).unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix='pgsims-coverage-db-') as temporary:
        base = [python, '-m', 'pytest', '-o', 'addopts=--tb=short --disable-warnings --ignore=sims/_legacy',
                '--cov=sims', '--cov-branch', '--cov-config=.coveragerc', '--cov-fail-under=0']
        sqlite_env = env | {
            'DATABASE_URL': f'sqlite:///{temporary}/coverage.sqlite3',
            'SECRET_KEY': 'isolated-coverage-tests-only', 'DEBUG': 'False',
            'DJANGO_SETTINGS_MODULE': 'sims_project.settings_test',
            'COVERAGE_FILE': str(directory / '.coverage.sqlite'),
        }
        sqlite = invoke(base + ['-m', 'not postgres', f'--junitxml={directory / "tests-sqlite.xml"}'],
                        ROOT / 'backend', sqlite_env, directory / 'run-sqlite.log')
        if sqlite:
            return sqlite
        with disposable_postgres() as database_url:
            postgres_env = env | {
                'DATABASE_URL': database_url, 'SECRET_KEY': 'isolated-coverage-tests-only',
                'DEBUG': 'False', 'DJANGO_SETTINGS_MODULE': 'sims_project.settings_test',
                'COVERAGE_FILE': str(directory / '.coverage.postgres'),
            }
            # The disposable database has no migration history.  pytest-django's
            # direct model-table setup is equivalent for this marked runtime
            # check and avoids spending minutes applying historical migrations.
            postgres = invoke(base + ['--no-migrations', '-m', 'postgres', f'--junitxml={directory / "tests-postgres.xml"}'],
                              ROOT / 'backend', postgres_env, directory / 'run-postgres.log')
        if postgres:
            return postgres
    coverage_env = env | {'COVERAGE_FILE': str(directory / '.coverage')}
    combine = subprocess.call([python, '-m', 'coverage', 'combine', str(directory / '.coverage.sqlite'), str(directory / '.coverage.postgres')], cwd=ROOT / 'backend', env=coverage_env)
    if combine:
        return combine
    reports = subprocess.call([python, '-m', 'coverage', 'json', '-o', str(directory / 'coverage.json')], cwd=ROOT / 'backend', env=coverage_env)
    reports |= subprocess.call([python, '-m', 'coverage', 'html', '-d', str(directory / 'html')], cwd=ROOT / 'backend', env=coverage_env)
    (directory / 'run.log').write_text(
        'Backend coverage uses separate isolated database runs.\n\n'
        + (directory / 'run-sqlite.log').read_text()
        + '\n\n===== PostgreSQL marked tests =====\n\n'
        + (directory / 'run-postgres.log').read_text()
    )
    return reports


def run(platform, manifest, unit_only=False):
    directory = OUTPUT / platform
    directory.mkdir(parents=True, exist_ok=True)
    # Remove the completion marker first; interruption must not preserve old success.
    marker = directory / 'run.json'
    marker.unlink(missing_ok=True)
    stamp = provenance(manifest)
    env = os.environ.copy()
    if platform == 'frontend':
        command = ['npm', 'run', 'test:coverage', '--', '--runInBand', '--silent', '--json',
                   f'--outputFile={directory / "tests.json"}', f'--coverageDirectory={directory}',
                   '--coverageReporters=json-summary', '--coverageReporters=html', '--coverageReporters=text-summary']
        result = invoke(command, ROOT / 'frontend', env, directory / 'run.log')
    elif platform == 'backend':
        result = run_backend(manifest, directory, env)
    else:
        command = ['./gradlew', 'coverageUnitReport' if unit_only else 'coverageReport', '--no-parallel', '--max-workers=2']
        if not unit_only:
            serial = env.get('ANDROID_SERIAL')
            if not serial:
                raise ValueError('ANDROID_SERIAL must identify the dedicated pgsims emulator')
            avd = subprocess.check_output(['adb', '-s', serial, 'emu', 'avd', 'name'], text=True).splitlines()
            if not avd or avd[0].strip() != 'pgsims':
                raise ValueError('Connected coverage requires the dedicated pgsims AVD')
            base_url = env.get('COVERAGE_ANDROID_BASE_URL', '')
            from urllib.parse import urlparse
            if urlparse(base_url).hostname not in ('localhost', '127.0.0.1', '10.0.2.2'):
                raise ValueError('COVERAGE_ANDROID_BASE_URL must point to an isolated loopback test backend')
            command.append('-PpgrCompanionTestBaseUrl=' + base_url)
        result = invoke(command, ROOT / 'android', env, directory / 'run.log')
        cases = []
        for module in ('app-companion', 'core/common'):
            build = ROOT / 'android' / module / 'build'
            paths = list((build / 'test-results/testDebugUnitTest').glob('TEST-*.xml'))
            if not unit_only:
                paths += list((build / 'outputs/androidTest-results/connected/debug').rglob('TEST-*.xml'))
            for path in paths:
                cases.extend(ET.parse(path).getroot().iter('testcase'))
        failed = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
        skipped = sum(c.find('skipped') is not None for c in cases)
        (directory / 'tests.json').write_text(json.dumps({'total': len(cases), 'passed': len(cases)-failed-skipped, 'failed': failed, 'skipped': skipped}))
        stamp['unit_only'] = unit_only

    stamp.update(exit_code=result, platform=platform)
    marker.write_text(json.dumps(stamp, indent=2) + '\n')
    print(f'{platform}: exit {result}; {directory / "run.log"}')
    return result


def parse_report(platform):
    directory = OUTPUT / platform
    if platform == 'frontend':
        data = json.loads((directory / 'coverage-summary.json').read_text())
        result = {}
        for name, values in data.items():
            if name == 'total':
                continue
            path = Path(name)
            relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else name
            result[relative] = {key: (values[key]['covered'], values[key]['total'])
                                for key in ('lines', 'branches', 'statements', 'functions')}
        tests = json.loads((directory / 'tests.json').read_text())
        counts = {'passed': tests['numPassedTests'], 'failed': tests['numFailedTests'],
                  'skipped': tests['numPendingTests'] + tests.get('numTodoTests', 0), 'total': tests['numTotalTests']}
        if tests.get('numRuntimeErrorTestSuites', 0) or not tests.get('success', False):
            counts['failed'] += 1
        return result, counts
    if platform == 'backend':
        data = json.loads((directory / 'coverage.json').read_text())
        result = {}
        for name, values in data['files'].items():
            s = values['summary']
            path = Path(name)
            relative = path.relative_to(ROOT).as_posix() if path.is_absolute() else 'backend/' + name
            result[relative] = {'lines': (s['covered_lines'], s['num_statements']),
                                'branches': (s['covered_branches'], s['num_branches'])}
        paths = [directory / 'tests-sqlite.xml', directory / 'tests-postgres.xml']
        if not all(path.exists() for path in paths):
            raise ValueError('Missing SQLite or PostgreSQL backend test evidence')
        cases = [case for path in paths for case in ET.parse(path).findall('.//testcase')]
        failed = sum(c.find('failure') is not None or c.find('error') is not None for c in cases)
        skipped = sum(c.find('skipped') is not None for c in cases)
        return result, {'passed': len(cases)-failed-skipped, 'failed': failed, 'skipped': skipped, 'total': len(cases)}
    # Android XML is aggregated by Gradle from matching unit and device bytecode.
    root = ET.parse(directory / 'coverage.xml').getroot()
    result = {}
    for package in root.findall('package'):
        for source in package.findall('sourcefile'):
            suffix = '/java/' + package.attrib['name'] + '/' + source.attrib['name']
            matches = [p for p in inventory() if p.startswith('android/') and p.endswith(suffix)]
            if not matches and (package.attrib['name'].startswith(('kotlin/', 'okhttp3/'))):
                # Inline library source tables emitted into the app's bytecode.
                continue
            if len(matches) != 1:
                raise ValueError(f'Unmapped Android source: {suffix}')
            counters = {c.attrib['type']: (int(c.attrib['covered']), int(c.attrib['covered']) + int(c.attrib['missed'])) for c in source.findall('counter')}
            result[matches[0]] = {metric: counters.get(kind, (0, 0)) for metric, kind in [('lines','LINE'),('branches','BRANCH'),('methods','METHOD')]}
    return result, json.loads((directory / 'tests.json').read_text())


def has_executable_source(path):
    """Comments and docstrings do not create executable coverage opportunities."""
    text = path.read_text()
    if path.suffix != '.py':
        return bool(text.strip())
    return bool(ast.parse(text).body)


def threshold_for(profile, platform, area, metric, legacy_minimum):
    """Return the most-specific target: area, wildcard area, platform, then legacy minimum."""
    if profile is None:
        return legacy_minimum
    target = profile['platforms'].get(platform, {})
    scopes = [target.get('metrics', {})] if area is None else [
        target.get('areas', {}).get(area, {}),
        target.get('areas', {}).get('*', {}),
        target.get('metrics', {}),
    ]
    for metrics in scopes:
        if metric in metrics:
            return metrics[metric]
    return None


def report(manifest, platforms, target_profile=None):
    failures, rows, test_counts = [], {}, {}
    profiles = manifest.get('target_profiles', {})
    profile = profiles.get(target_profile) if target_profile else None
    if target_profile and profile is None:
        raise ValueError(f'Unknown target profile: {target_profile}')
    stamp = provenance(manifest)
    for platform in platforms:
        try:
            marker = json.loads((OUTPUT / platform / 'run.json').read_text())
            if any(marker.get(k) != v for k, v in stamp.items()) or marker.get('exit_code') != 0 or marker.get('unit_only'):
                raise ValueError('Failed or stale run; rerun at this commit/source hash')
            files, counts = parse_report(platform)
            test_counts[platform] = counts
            if not counts['total'] or counts['failed'] or counts['skipped']:
                failures.append(f'{platform}: failed/skipped/empty test suite: {counts}')
            for name, assignment in manifest['files'].items():
                if assignment['platform'] != platform:
                    continue
                if name not in files:
                    # Empty Python package markers have no executable statements.
                    if not has_executable_source(ROOT / name):
                        continue
                    failures.append(f'{platform}: missing source coverage: {name}')
                    continue
                for group in (platform, platform + '/' + assignment['area']):
                    for metric, (covered, total) in files[name].items():
                        value = rows.setdefault(group, {}).setdefault(metric, [0, 0])
                        value[0] += covered
                        value[1] += total
        except (ValueError, KeyError, OSError, ET.ParseError) as error:
            failures.append(f'{platform}: {error}')
    percentages = {}
    for group, metrics in sorted(rows.items()):
        percentages[group] = {}
        for metric, (covered, total) in metrics.items():
            percent = 100 * covered / total if total else None
            percentages[group][metric] = {'covered': covered, 'total': total, 'percent': percent}
            platform, _, area = group.partition('/')
            minimum = threshold_for(profile, platform, area or None, metric, manifest['minimum'])
            if minimum is not None and percent is not None and percent < minimum:
                failures.append(f'{group} {metric}: {percent:.2f}% < {minimum}%')
    output = {'provenance': stamp, 'metrics': percentages, 'tests': test_counts,
              'failures': failures, 'platforms': platforms, 'target_profile': target_profile,
              'verdict': 'GO' if not failures else 'BLOCKED'}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / 'summary.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
    return bool(failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['inventory', 'backend', 'frontend', 'android', 'report'])
    parser.add_argument('--platform', action='append', choices=['backend','frontend','android'])
    parser.add_argument('--unit-only', action='store_true', help='Android baseline only; never satisfies the complete gate')
    parser.add_argument('--target-profile', help='Named target profile from coverage_manifest.json')
    args = parser.parse_args()
    manifest = validate_manifest()
    if args.mode == 'inventory':
        print(f'{len(manifest["files"])} assigned source files; manifest valid')
        return 0
    if args.mode == 'report':
        profile = manifest.get('target_profiles', {}).get(args.target_profile, {})
        platforms = args.platform or list(profile.get('platforms', {})) or ['backend', 'frontend', 'android']
        return report(manifest, platforms, args.target_profile)
    return run(args.mode, manifest, args.unit_only)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        sys.exit(2)

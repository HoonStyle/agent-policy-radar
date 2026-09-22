"""Local execution evidence, not an authenticated or tamper-proof audit ledger."""
import datetime as dt
import hashlib
import json
import platform
from pathlib import Path
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def save(path, data):
    with path.open('xb') as stream:
        stream.write(data)
    path.chmod(0o600)


def inventory():
    result = {}
    for directory, pattern in [('reports', '*.json'), ('reports', '*.md'),
                               ('recommendations', '*.md'), ('data', 'source_state.json'),
                               ('data/snapshots', '*.txt'), ('sources', '*-source-changes.md')]:
        for path in (ROOT / directory).glob(pattern):
            result[str(path.relative_to(ROOT))] = path.read_bytes()
    return result


def execute(argv, operation, base=None):
    base = Path(base) if base else Path.home() / '.agent-policy-radar' / 'audit'
    folder = base / (dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex)
    folder.mkdir(parents=True, mode=0o700, exist_ok=False)
    started, clock = utc(), time.monotonic()
    before = inventory()
    code = None
    failure = None
    inputs = {}
    for pattern in ('scripts/*.py', 'data/*registry.json', 'data/instruction_targets.json', 'package.json'):
        for p in ROOT.glob(pattern):
            inputs[str(p.relative_to(ROOT))] = sha(p.read_bytes())
    metadata = {'schema_version': 1, 'run_id': folder.name, 'started_at': started,
                'argv': argv, 'cwd': str(Path.cwd()), 'package_root': str(ROOT),
                'python': platform.python_version(), 'platform': platform.platform(),
                'tool_version': json.loads((ROOT / 'package.json').read_text())['version'],
                'implementation_and_config_sha256': inputs,
                'approval': None, 'policy_applied': False,
                'limitations': ['Local files editable by owner; not tamper-proof',
                                'argv and artifacts may contain private paths or excerpts',
                                'Only unified CLI executions are captured',
                                'Unchanged output does not prove a stage executed']}
    save(folder / 'started.json', json.dumps(metadata, ensure_ascii=False, indent=2).encode())
    try:
        code = operation()
        return code
    except BaseException as error:
        failure = type(error).__name__
        raise
    finally:
        after = inventory()
        artifacts = []
        for name in sorted(before.keys() | after.keys()):
            old, new = before.get(name), after.get(name)
            item = {'path': name, 'before_sha256': sha(old) if old is not None else None,
                    'after_sha256': sha(new) if new is not None else None,
                    'changed': old != new}
            # Preserve both sides locally without trusting basename uniqueness.
            for side, data in [('before', old), ('after', new)]:
                if data is not None:
                    content = folder / (sha(data) + '.blob')
                    if not content.exists():
                        save(content, data)
                    item[side + '_artifact'] = content.name
            artifacts.append(item)
        metadata.update({'finished_at': utc(), 'duration_seconds': round(time.monotonic() - clock, 3),
                         'exit_code': code, 'exception_type': failure,
                         'status': 'success' if code == 0 and failure is None else 'failed',
                         'artifacts': artifacts})
        save(folder / 'finished.json', json.dumps(metadata, ensure_ascii=False, indent=2).encode())
        print(f'Audit record: {folder}', file=sys.stderr)

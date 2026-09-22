#!/usr/bin/env python3
"""Local review ledger helper. Does not run profile commands or modify reviewed code."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import uuid

LEVELS = {'unverified', 'source', 'execution', 'simulator', 'device'}
STATUSES = {'open', 'investigating', 'fixed-unverified', 'verified', 'deferred', 'rejected', 'reopened'}
INPUTS = {'source', 'requirements', 'initial-judgment', 'briefing', 'other'}


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, timeout=30).stdout


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def profile(root):
    path = root / '.review-workflow.json'
    raw = path.read_bytes() if path.exists() else None
    config = json.loads(raw) if raw else {'schema_version': 1, 'language': 'ko', 'ledger_dir': '.review-notes'}
    if config.get('schema_version') != 1:
        raise ValueError('Unsupported profile schema')
    destination = Path(config.get('ledger_dir', '.review-notes'))
    if destination.is_absolute() or '..' in destination.parts:
        raise ValueError('ledger_dir must be project-relative, without ..')
    config['ledger_dir'] = str(destination)
    return config, sha(raw) if raw is not None else None


def file_hash(root, name):
    path = root / name
    if path.is_symlink():
        return sha(os.fsencode(os.readlink(path))), 'symlink'
    if not path.exists():
        return None, 'deleted'
    if not path.is_file():
        raise ValueError(f'Unsupported path (e.g. submodule): {name}')
    return sha(path.read_bytes()), 'file'


def snapshot(root):
    """Hash all index entries plus nonignored untracked files; never store contents."""
    root = Path(root).resolve()
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    before = git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all')
    tracked = git(root, 'ls-files', '--stage', '-z')
    staged = set(git(root, 'diff', '--cached', '--name-only', '-z', '--no-renames').split(b'\0'))
    unstaged = set(git(root, 'diff', '--name-only', '-z', '--no-renames').split(b'\0'))
    untracked = git(root, 'ls-files', '--others', '--exclude-standard', '-z')
    records = []
    indexed = set()
    for entry in tracked.split(b'\0'):
        if not entry:
            continue
        meta, rawname = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        if stage != b'0' or mode == b'160000':
            raise ValueError('Unmerged index/submodule requires manual baseline; not claiming full coverage')
        name = os.fsdecode(rawname)
        indexed.add(rawname)
        content = git(root, 'cat-file', 'blob', oid.decode())
        records.append({'path': name, 'state': 'staged' if rawname in staged else 'index',
                        'sha256': sha(content), 'mode': mode.decode()})
        digest, kind = file_hash(root, name)
        records.append({'path': name, 'state': 'unstaged' if rawname in unstaged else 'worktree',
                        'sha256': digest, 'kind': kind})
    for name in staged - indexed - {b''}:
        records.append({'path': os.fsdecode(name), 'state': 'staged-deleted', 'sha256': None})
    for rawname in untracked.split(b'\0'):
        if rawname:
            name = os.fsdecode(rawname)
            digest, kind = file_hash(root, name)
            records.append({'path': name, 'state': 'untracked', 'sha256': digest, 'kind': kind})
    if before != git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all') or head != git(root, 'rev-parse', 'HEAD').decode().strip() or tracked != git(root, 'ls-files', '--stage', '-z'):
        raise ValueError('Repository changed during capture; retry with writers paused')
    records.sort(key=lambda x: (x['path'], x['state']))
    return {'head': head, 'files': records, 'content_sha256': sha(json.dumps(records, sort_keys=True).encode()),
            'scope': 'all index and worktree files plus nonignored untracked files',
            'limitations': ['Ignored files excluded', 'Renames represented as deletion/addition when applicable',
                            'Not an atomic filesystem snapshot; pause concurrent writers',
                            'Matching hashes do not prove reviewer read the files', 'Paths may be private']}


def classify(review):
    actor, first = review.get('reviewer'), review.get('initial_reviewer')
    inputs = review.get('inputs')
    if not actor or not first:
        return 'unknown'
    if actor == first:
        return 'self'
    if not isinstance(inputs, list) or not inputs or not review.get('input_inventory_complete'):
        return 'unknown'
    if any(not isinstance(x, dict) or x.get('kind') not in INPUTS or not x.get('reference') for x in inputs):
        return 'unknown'
    kinds = {x['kind'] for x in inputs}
    if kinds & {'initial-judgment', 'briefing'}:
        return 'comparative'
    if kinds <= {'source', 'requirements'} and review.get('execution_reference'):
        return 'independent'
    return 'unknown'


def validate(data):
    errors = []
    if data.get('schema_version') != 1:
        errors.append('Unsupported ledger schema')
    seen = set()
    for finding in data.get('findings', []):
        fid = finding.get('id')
        if not fid or fid in seen:
            errors.append('Missing or duplicate finding ID')
        seen.add(fid)
        if finding.get('status') not in STATUSES:
            errors.append(f'{fid}: invalid status')
        v = finding.get('verification', {})
        if v.get('level', 'unverified') not in LEVELS:
            errors.append(f'{fid}: invalid verification level')
        if finding.get('status') == 'verified':
            level = v.get('level')
            required = ['code_location', 'reasoning'] if level == 'source' else ['command', 'result', 'environment']
            if level in {'simulator', 'device'}:
                required += ['device_id', 'configuration_id']
            if level not in LEVELS - {'unverified'}:
                errors.append(f'{fid}: unverified cannot become verified')
            if any(not v.get(key) for key in required) or v.get('outcome') != 'pass':
                errors.append(f'{fid}: missing verification evidence or pass outcome')
            if any(not finding.get(key) for key in ['requirement_reference', 'observed_boundary', 'unconfirmed_scope']):
                errors.append(f'{fid}: requirement/boundary/unconfirmed scope required (use explicit none if appropriate)')
    for event in data.get('passes', []):
        if event.get('classification') != classify(event):
            errors.append('Pass classification inconsistent with recorded inputs')
    return errors


def persist(path, data):
    """Cooperating writers use an exclusive lock; journal complete state before replacement."""
    path = Path(path)
    history = path.parent / (path.name + '.history')
    history.mkdir(mode=0o700, exist_ok=True)
    payload = (json.dumps(data, ensure_ascii=True, indent=2) + '\n').encode()
    event = history / (uuid.uuid4().hex + '.json')
    with event.open('xb') as stream:
        stream.write(payload)
    event.chmod(0o600)
    fd, name = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--repo', default='.')
    init.add_argument('--output', help='Explicit ledger path; overrides project ledger_dir')
    for cmd in ('finding', 'update', 'pass', 'validate', 'compare'):
        parser = sub.add_parser(cmd)
        parser.add_argument('ledger')
        if cmd in ('finding', 'update', 'pass'):
            parser.add_argument('--input', required=True, help='JSON input; no executable commands')
        if cmd == 'update':
            parser.add_argument('--id', required=True)
    args = p.parse_args()
    lock = None
    try:
        if args.command == 'init':
            root = Path(git(args.repo, 'rev-parse', '--show-toplevel').decode().strip()).resolve()
            settings, digest = profile(root)
            baseline = snapshot(root)
            destination = (root / settings['ledger_dir']).resolve()
            if not destination.is_relative_to(root):
                raise ValueError('Profile ledger_dir escapes project through a symlink')
            path = Path(args.output).expanduser().resolve() if args.output else destination / (uuid.uuid4().hex + '.json')
            path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
            lock = path.with_name(path.name + '.lock')
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            if path.exists():
                raise ValueError('Ledger already exists')
            data = {'schema_version': 1, 'created_at': utc(), 'repository': str(root), 'baseline': baseline,
                    'profile': settings, 'profile_sha256': digest, 'findings': [], 'passes': [],
                    'checks': settings.get('checks', []), 'events': [{'at': utc(), 'action': 'init'}]}
        else:
            path = Path(args.ledger).expanduser().resolve(strict=True)
            if args.command in ('finding', 'update', 'pass'):
                lock = path.with_name(path.name + '.lock')
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.close(fd)
            data = load(path)
            if args.command == 'validate':
                errors = validate(data)
                print('\n'.join(errors) if errors else 'Structure valid; evidence truth and approval are not certified.')
                return int(bool(errors))
            if args.command == 'compare':
                current = snapshot(data['repository'])
                match = current['head'] == data['baseline']['head'] and current['files'] == data['baseline']['files']
                print('Recorded scope matches' if match else 'Baseline differs (including any untracked ledger files)')
                return 0 if match else 1
            incoming = load(args.input)
            if args.command == 'finding':
                numbers = [int(f['id'][2:]) for f in data['findings']]
                incoming['id'] = f'R-{max(numbers, default=0) + 1:03d}'
                incoming.setdefault('status', 'open')
                incoming.setdefault('verification', {'level': 'unverified'})
                data['findings'].append(incoming)
                print(incoming['id'])
            elif args.command == 'update':
                matches = [i for i, f in enumerate(data['findings']) if f['id'] == args.id]
                if not matches:
                    raise ValueError('Unknown finding ID')
                incoming['id'] = args.id
                data['findings'][matches[0]] = incoming
            else:
                incoming['classification'] = classify(incoming)
                incoming['recorded_at'] = utc()
                incoming['id'] = f'P-{len(data["passes"]) + 1:03d}'
                data['passes'].append(incoming)
                print(incoming['classification'])
            data['events'].append({'at': utc(), 'action': args.command, 'id': incoming['id']})
        errors = validate(data)
        if errors:
            raise ValueError('; '.join(errors))
        persist(path, data)
        print(path)
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f'Error: {error}', file=__import__('sys').stderr)
        return 1
    finally:
        if lock is not None and 'fd' in locals():
            lock.unlink(missing_ok=True)


if __name__ == '__main__':
    raise SystemExit(main())

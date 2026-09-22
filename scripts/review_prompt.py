#!/usr/bin/env python3
"""Create a unique local prompt-review bundle; never apply a patch."""
import argparse
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import re
import uuid

SAFETY = re.compile(r'승인|금지|비공개|개인정보|자격|비밀|외부|결제|삭제|보안|안전|권한|approval|privacy|secret|credential|permission|delete|never|must not|do not|security|safety', re.I)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def draft(text):
    """Only adjacent identical plain bullets; section/code context stays intact."""
    output, decisions = [], []
    fence = None
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            output.append(line)
            continue
        repeat = output and line == output[-1] and re.match(r'^[-*] \S', line)
        if not fence and repeat:
            protected = bool(SAFETY.search(line))
            decisions.append({'line': number, 'action': 'keep' if protected else 'delete',
                              'original_text': line, 'duplicate_of_line': number - 1,
                              'reason': 'safety-related repetition retained' if protected else 'adjacent identical bullet; review before applying'})
            if not protected:
                continue
        output.append(line)
    return ''.join(output), decisions


def review(target, output, proposal=None):
    target = Path(target).expanduser().resolve(strict=True)
    raw = target.read_bytes()
    if len(raw) > 1_000_000:
        raise ValueError('Input exceeds 1 MB; no partial review is generated')
    text = raw.decode('utf-8')
    suggested, decisions = draft(text)
    mode = 'conservative-local-draft'
    if proposal:
        proposed = Path(proposal).expanduser().resolve(strict=True).read_bytes()
        if len(proposed) > 1_000_000:
            raise ValueError('Proposal exceeds 1 MB')
        suggested = proposed.decode('utf-8')
        mode = 'provided-proposal-unverified'
        decisions = [{'action': 'review', 'reason': 'Provided proposal requires semantic and safety review; no automatic approval.'}]
    changes = list(difflib.unified_diff(text.splitlines(True), suggested.splitlines(True),
                                      fromfile='original/' + target.name, tofile='proposed/' + target.name))
    removed_sensitive = [x[1:].rstrip() for x in changes if x.startswith('-') and not x.startswith('---') and SAFETY.search(x)]
    run = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex
    folder = Path(output).expanduser().resolve() / run
    # Artifacts may contain private text. Never publish them automatically.
    folder.mkdir(parents=True, mode=0o700, exist_ok=False)
    artifacts = {'proposed.md': suggested.encode('utf-8'), 'changes.diff': ''.join(changes).encode('utf-8')}
    manifest = {'schema_version': 1, 'review_id': run, 'mode': mode, 'target': str(target),
                'created_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'proposal_source': str(Path(proposal).expanduser().resolve()) if proposal else None,
                'original_bytes': len(raw), 'proposed_bytes': len(artifacts['proposed.md']),
                'changed': raw != artifacts['proposed.md'],
                'original_sha256': digest(raw), 'proposed_sha256': digest(artifacts['proposed.md']),
                'patch_sha256': digest(artifacts['changes.diff']), 'status': 'pending-review',
                'approval': None, 'applied': False, 'decisions': decisions,
                'safety_removals_require_review': removed_sensitive,
                'limitations': ['No cross-file authority inference', 'No automatic semantic conflict resolution',
                                'Keyword safety checks are incomplete', 'Original bytes must be rechecked before any approved application']}
    artifacts['manifest.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    for name, data in artifacts.items():
        p = folder / name
        with p.open('xb') as stream:
            stream.write(data)
        p.chmod(0o600)
    return folder


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', help='Explicit instruction file to review')
    parser.add_argument('--proposal', help='Optional agent/human-authored replacement file')
    parser.add_argument('--output-dir', default=str(Path.home() / '.agent-policy-radar' / 'reviews'))
    args = parser.parse_args(argv)
    try:
        folder = review(args.target, args.output_dir, args.proposal)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f'Review failed: {error}\n')
    print(f'Review bundle: {folder}\nOriginal unchanged; explicit approval required before application.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

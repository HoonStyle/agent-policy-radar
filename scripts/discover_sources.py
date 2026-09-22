#!/usr/bin/env python3
"""Bounded official-index discovery. Candidates are not verified guidance."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import uuid

INDEXES = [
    'https://code.claude.com/docs/llms.txt',
    'https://platform.claude.com/llms.txt',
    'https://developers.openai.com/llms.txt',
    'https://learn.chatgpt.com/llms.txt',
]
HOSTS = {'code.claude.com', 'platform.claude.com', 'developers.openai.com', 'learn.chatgpt.com'}
TERMS = re.compile(r'prompt|migrat|release|changelog|model|instruction|agents\.md|claude\.md', re.I)
LIMIT = 5_000_000


def allowed(url):
    u = urllib.parse.urlsplit(url)
    return u.scheme == 'https' and u.hostname in HOSTS and not u.username and not u.password and u.port in (None, 443)


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError('Redirect outside official allowlist')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, timeout):
    if not allowed(url):
        raise ValueError('URL outside official allowlist')
    request = urllib.request.Request(url, headers={'User-Agent': 'agent-policy-radar-discovery/1'})
    with urllib.request.build_opener(Redirects()).open(request, timeout=timeout) as response:
        data = response.read(LIMIT + 1)
        if len(data) > LIMIT:
            raise ValueError('Index exceeds size limit; not parsed partially')
        return data.decode('utf-8'), response.url


def candidates(text, base):
    found = {}
    for number, line in enumerate(text.splitlines(), 1):
        for match in re.finditer(r'\[([^\]]+)\]\(([^\s)]+)\)', line):
            title, href = match.groups()
            url = urllib.parse.urljoin(base, href)
            url = urllib.parse.urldefrag(url)[0]
            try:
                valid = allowed(url)
            except ValueError:
                valid = False
            if valid and TERMS.search(title + ' ' + url):
                found.setdefault(url, {'url': url, 'title': title, 'index_url': base, 'line': number,
                                       'evidence': line, 'verified': False})
    return list(found.values())


def discover(output, timeout=15):
    output = Path(output).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    previous = set()
    for path in output.glob('*/report.json'):
        record = json.loads(path.read_text(encoding='utf-8'))
        previous.update(c['url'] for c in record['candidates'])
    stamp = dt.datetime.now(dt.timezone.utc).isoformat()
    results, combined = [], {}
    for url in INDEXES:
        try:
            text, final = fetch(url, timeout)
            entries = candidates(text, final)
            for c in entries:
                if c['url'] not in combined:
                    c['status'] = 'previously-seen' if c['url'] in previous else 'first-seen'
                    combined[c['url']] = c
            results.append({'url': url, 'final_url': final, 'ok': True,
                            'sha256': hashlib.sha256(text.encode()).hexdigest(), 'candidate_count': len(entries)})
        except Exception as error:
            results.append({'url': url, 'ok': False, 'error': str(error)})
    folder = output / uuid.uuid4().hex
    folder.mkdir(exist_ok=False)
    report = {'checked_at': stamp, 'indexes': results, 'candidates': list(combined.values()),
              'limitations': ['First-seen is not publication date', 'Keyword matching is not semantic verification',
                              'Only index links parsed; candidate bodies and release announcements not fetched',
                              'No automatic registry or instruction changes']}
    (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Discovered {len(combined)} candidates; index failures: {sum(not r["ok"] for r in results)}')
    print(f'Report: {folder / "report.json"}')
    return 1 if any(not r['ok'] for r in results) else 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir', default=str(Path.home() / '.agent-policy-radar' / 'discovery'))
    p.add_argument('--timeout', type=int, default=15)
    args = p.parse_args()
    return discover(args.output_dir, args.timeout)


if __name__ == '__main__':
    raise SystemExit(main())

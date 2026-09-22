import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'plugins/review-workflow/skills/review-workflow/scripts/review.py'
spec = importlib.util.spec_from_file_location('review_cli', SCRIPT)
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class WorkflowTests(unittest.TestCase):
    def test_classification(self):
        data = {'reviewer': 'B', 'initial_reviewer': 'A', 'input_inventory_complete': True,
                'execution_reference': 'run', 'inputs': [{'kind': 'source', 'reference': 'file'}]}
        self.assertEqual(r.classify(data), 'independent')
        data['inputs'].append({'kind': 'briefing', 'reference': 'brief'})
        self.assertEqual(r.classify(data), 'comparative')
        data['input_inventory_complete'] = False
        self.assertEqual(r.classify(data), 'unknown')
        data['reviewer'] = 'A'
        self.assertEqual(r.classify(data), 'self')

    def test_pass_references(self):
        data = {'schema_version': 1, 'findings': [{'id': 'R-001', 'status': 'open'}],
                'passes': [{'classification': 'unknown', 'finding_ids': ['R-001']}]}
        self.assertFalse(r.validate(data))
        for refs in (['R-999'], 'R-001', [None], None):
            data['passes'][0]['finding_ids'] = refs
            self.assertTrue(r.validate(data))
        data['passes'][0]['finding_ids'] = []
        self.assertFalse(r.validate(data))

    def test_verification(self):
        finding = {'id': 'R-001', 'status': 'verified', 'requirement_reference': 'spec',
                   'observed_boundary': 'return', 'unconfirmed_scope': 'external output',
                   'verification': {'level': 'source', 'code_location': 'a:1', 'reasoning': 'evidence', 'outcome': 'pass'}}
        data = {'schema_version': 1, 'findings': [finding]}
        self.assertFalse(r.validate(data))
        for level in ('unverified', 'execution', 'simulator', 'device'):
            finding['verification']['level'] = level
            self.assertTrue(r.validate(data))
        finding['verification'].update(level='device', command='test', result='ok', environment='lab', device_id='d', configuration_id='c')
        self.assertFalse(r.validate(data))

    def test_real_cli_and_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / '한글 repo'
            root.mkdir()
            def git(*args):
                return r.git(root, *args)
            git('init'); git('config', 'user.email', 'test@example.invalid'); git('config', 'user.name', 'Fixture')
            f = root / 'a.txt'; f.write_text('base')
            git('add', '.'); git('commit', '-m', 'fixture')
            f.write_text('staged'); git('add', 'a.txt'); f.write_text('unstaged')
            (root / 'new.txt').write_text('new')
            snap = r.snapshot(root)
            self.assertEqual({x['state'] for x in snap['files']}, {'staged', 'unstaged', 'untracked'})
            self.assertEqual(r.snapshot(root), snap)
            ledger = Path(tmp) / 'ledger.json'
            def cli(*args, expected=0):
                result = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
            cli('init', '--repo', root, '--output', ledger)
            cli('compare', ledger)
            entry = Path(tmp) / 'finding.json'
            entry.write_text(json.dumps({'title': 'test', 'status': 'open'}))
            cli('finding', ledger, '--input', entry)
            cli('finding', ledger, '--input', entry)
            data = r.load(ledger)
            self.assertEqual([x['id'] for x in data['findings']], ['R-001', 'R-002'])
            entry.write_text('{"status":"verified"}')
            cli('update', ledger, '--id', 'R-001', '--input', entry, expected=1)
            self.assertEqual(r.load(ledger), data)
            self.assertEqual(len(list(Path(str(ledger) + '.history').glob('*.json'))), 3)
            cli('validate', ledger)
            entry.write_text('{"finding_ids":["R-999"]}')
            cli('pass', ledger, '--input', entry, expected=1)
            self.assertEqual(r.load(ledger), data)
            self.assertEqual(len(list(Path(str(ledger) + '.history').glob('*.json'))), 3)
            entry.write_text('{"finding_ids":["R-001"]}')
            cli('pass', ledger, '--input', entry)
            cli('validate', ledger)
            # Standalone validation must catch a manually corrupted reference too.
            good = ledger.read_bytes()
            broken = r.load(ledger)
            broken['passes'][0]['finding_ids'] = ['R-999']
            ledger.write_text(json.dumps(broken))
            cli('validate', ledger, expected=1)
            ledger.write_bytes(good)
            f.write_text('changed again'); cli('compare', ledger, expected=1)
            # Lock held by someone else must never be removed by a failed command.
            lock = Path(str(ledger) + '.lock'); lock.write_text('held')
            cli('finding', ledger, '--input', entry, expected=1)
            self.assertTrue(lock.exists())

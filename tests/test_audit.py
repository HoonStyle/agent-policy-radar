import sys
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import audit


class AuditTests(unittest.TestCase):
    def test_before_after_and_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'package'
            root.mkdir()
            (root / 'package.json').write_text('{"version":"test"}', encoding='utf-8')
            (root / 'reports').mkdir()
            report = root / 'reports/test.json'
            report.write_text('{"old":true}', encoding='utf-8')
            output = Path(tmp) / 'audit'
            def operation():
                report.write_text('{"new":true}', encoding='utf-8')
                return 0
            with patch.object(audit, 'ROOT', root):
                self.assertEqual(audit.execute(['scan'], operation, output), 0)
                with self.assertRaises(RuntimeError):
                    audit.execute(['scan'], lambda: (_ for _ in ()).throw(RuntimeError('test')), output)
            records = [json.loads(p.read_text(encoding='utf-8')) for p in output.glob('*/finished.json')]
            self.assertEqual({x['status'] for x in records}, {'success', 'failed'})
            success = next(x for x in records if x['status'] == 'success')
            self.assertTrue(success['artifacts'][0]['changed'])
            folder = output / success['run_id']
            artifact = success['artifacts'][0]
            self.assertEqual((folder / artifact['before_artifact']).read_text(encoding='utf-8'), '{"old":true}')
            self.assertEqual((folder / artifact['after_artifact']).read_text(encoding='utf-8'), '{"new":true}')
            self.assertIsNone(success['approval'])
            self.assertFalse(success['policy_applied'])

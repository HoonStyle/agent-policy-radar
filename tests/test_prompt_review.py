import sys
from pathlib import Path
import tempfile
import unittest
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_prompt import draft, review


class ReviewTests(unittest.TestCase):
    def test_duplicate(self):
        self.assertEqual(draft('- Be concise.\n- Be concise.\n')[0], '- Be concise.\n')

    def test_safety(self):
        text = '- 승인 없이 삭제 금지\n- 승인 없이 삭제 금지\n'
        self.assertEqual(draft(text)[0], text)

    def test_context(self):
        for text in ['```\n- a\n- a\n```\n', '- a\n\n## Other\n- a\n']:
            self.assertEqual(draft(text)[0], text)

    def test_bundles_and_proposal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / '한글 instructions.md'
            raw = b'- Never delete files.\r\n'
            p.write_bytes(raw)
            proposal = root / 'draft.md'
            proposal.write_text('Replacement\n')
            a = review(p, root / 'output', proposal)
            b = review(p, root / 'output', proposal)
            self.assertNotEqual(a, b)
            self.assertEqual(p.read_bytes(), raw)
            record = json.loads((a / 'manifest.json').read_text())
            self.assertFalse(record['applied'])
            self.assertIsNone(record['approval'])
            self.assertTrue(record['safety_removals_require_review'])
            self.assertIn('- Never delete files.', (a / 'changes.diff').read_text())


if __name__ == '__main__':
    unittest.main()

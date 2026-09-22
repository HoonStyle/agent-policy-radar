import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import policy_radar as runner


class RunnerTests(unittest.TestCase):
    def test_external_failure_continues_local(self):
        with patch.object(sys, 'argv', ['radar', 'all']), patch.object(runner, 'run_step', side_effect=[1, 1, 0, 0, 0]) as step:
            self.assertEqual(runner.main(), 1)
            self.assertEqual([c.args[0] for c in step.call_args_list], ['discover', 'sources', 'scan', 'overlap', 'recommend'])

    def test_local_failure_stops_dependents(self):
        with patch.object(sys, 'argv', ['radar', 'all']), patch.object(runner, 'run_step', side_effect=[1, 0, 2]) as step:
            self.assertEqual(runner.main(), 2)
            self.assertEqual([c.args[0] for c in step.call_args_list], ['discover', 'sources', 'scan'])

    def test_standalone_failure(self):
        with patch.object(sys, 'argv', ['radar', 'discover']), patch.object(runner, 'run_step', return_value=1) as step:
            self.assertEqual(runner.main(), 1)
            step.assert_called_once_with('discover')

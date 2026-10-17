"""Ensure coverage accounting fails closed instead of hiding missing evidence."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import coverage_gate as gate


class CoverageGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {'minimum': 95, 'files': {'frontend/app/page.tsx': {'platform': 'frontend', 'area': 'identity'}}}
        (self.root / 'frontend').mkdir()
        self.stamp = {'commit': 'test', 'source_sha256': 'hash'}
        (self.root / 'frontend/run.json').write_text(json.dumps({**self.stamp, 'exit_code': 0}))

    def report(self, coverage, counts=None):
        with patch.object(gate, 'OUTPUT', self.root), patch.object(gate, 'provenance', return_value=self.stamp), patch.object(gate, 'parse_report', return_value=(coverage, counts or {'passed':1,'total':1,'failed':0,'skipped':0})), contextlib.redirect_stdout(io.StringIO()):
            return gate.report(self.manifest, ['frontend'])

    def test_branches_fail_even_when_lines_pass(self):
        self.assertTrue(self.report({'frontend/app/page.tsx': {'lines': (100,100), 'branches': (94,100)}}))

    def test_exact_threshold_passes(self):
        self.assertFalse(self.report({'frontend/app/page.tsx': {'lines': (95,100), 'branches': (95,100)}}))

    def test_unrounded_threshold(self):
        self.assertTrue(self.report({'frontend/app/page.tsx': {'lines': (94999,100000)}}))

    def test_empty_metric_is_not_fabricated_100_percent(self):
        self.report({'frontend/app/page.tsx': {'lines': (1,1), 'branches': (0,0)}})
        data=json.loads((self.root/'summary.json').read_text())
        self.assertIsNone(data['metrics']['frontend']['branches']['percent'])

    def test_skipped_tests_fail(self):
        self.assertTrue(self.report({'frontend/app/page.tsx': {'lines':(1,1)}}, {'passed':1,'total':2,'failed':0,'skipped':1}))

    def test_stale_commit_fails(self):
        (self.root/'frontend/run.json').write_text(json.dumps({'commit':'old','source_sha256':'hash','exit_code':0}))
        self.assertTrue(self.report({}))

    def test_missing_run_fails(self):
        (self.root/'frontend/run.json').unlink()
        self.assertTrue(self.report({}))

    def test_low_area_cannot_be_hidden_in_platform_average(self):
        self.manifest['files']['frontend/app/other.tsx']={'platform':'frontend','area':'other'}
        self.assertTrue(self.report({'frontend/app/page.tsx': {'lines': (1,2)}, 'frontend/app/other.tsx': {'lines': (1000,1000)}}))

    def test_profile_uses_area_floor_over_platform_floor(self):
        self.manifest['target_profiles'] = {
            'sprint': {'platforms': {'frontend': {
                'metrics': {'lines': 60},
                'areas': {'identity': {'lines': 80}},
            }}}
        }
        with patch.object(gate, 'OUTPUT', self.root), patch.object(gate, 'provenance', return_value=self.stamp), patch.object(gate, 'parse_report', return_value=({'frontend/app/page.tsx': {'lines': (70,100)}}, {'passed':1,'total':1,'failed':0,'skipped':0})), contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(gate.report(self.manifest, ['frontend'], 'sprint'))

    def test_profile_uses_platform_floor_for_platform_total(self):
        self.manifest['target_profiles'] = {
            'sprint': {'platforms': {'frontend': {
                'metrics': {'lines': 80},
                'areas': {'*': {'lines': 60}},
            }}}
        }
        with patch.object(gate, 'OUTPUT', self.root), patch.object(gate, 'provenance', return_value=self.stamp), patch.object(gate, 'parse_report', return_value=({'frontend/app/page.tsx': {'lines': (70,100)}}, {'passed':1,'total':1,'failed':0,'skipped':0})), contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(gate.report(self.manifest, ['frontend'], 'sprint'))

    def test_profile_can_omit_non_applicable_metric(self):
        self.manifest['target_profiles'] = {
            'sprint': {'platforms': {'frontend': {
                'metrics': {'lines': 60},
                'areas': {'identity': {'lines': 70}},
            }}}
        }
        with patch.object(gate, 'OUTPUT', self.root), patch.object(gate, 'provenance', return_value=self.stamp), patch.object(gate, 'parse_report', return_value=({'frontend/app/page.tsx': {'lines': (70,100), 'branches': (0,100)}}, {'passed':1,'total':1,'failed':0,'skipped':0})), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(gate.report(self.manifest, ['frontend'], 'sprint'))


if __name__ == '__main__':
    unittest.main()

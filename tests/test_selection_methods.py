"""Regression tests for evidence-filtered supervisor-choice rules."""
import unittest, importlib.util, json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('selection_check',R/'scripts/check_selection_evidence.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SelectionMethods(unittest.TestCase):
    def test_valid_fixture(self):
        claims=json.loads((R/'tests/fixtures/selection_evidence_valid.json').read_text())
        self.assertEqual(m.review(claims),[])
    def test_wrong_fixtures_rejected(self):
        claims=json.loads((R/'tests/fixtures/selection_evidence_invalid.json').read_text())
        errors=m.review(claims)
        self.assertGreaterEqual(len(errors),5)
        self.assertTrue(any('completion rate' in e for e in errors))
        self.assertTrue(any('national rule' in e for e in errors))
        self.assertTrue(any('serious finding' in e for e in errors))
        self.assertTrue(any('forbidden evidence basis' in e for e in errors))
    def test_country_specific_rules(self):
        for country,checks in {
            'mainland-china':['2020','NSFC','cannot yield dropout/delay rates'],
            'united-states':['rotations','not** evidence that all US STEM'],
            'united-kingdom':['archived','not UK-wide'],
            'australia':['RTP','not automatic'],
            'new-zealand':['at least monthly','not a nationwide'],
        }.items():
            s=(R/f'references/{country}.md').read_text()
            for check in checks: self.assertIn(check,s)
    def test_selection_and_safe_interviews(self):
        a=(R/'references/supervisor-selection-methods.md').read_text()
        b=(R/'references/interviews-and-risk-signals.md').read_text()
        for term in ('Mainland China','United States','United Kingdom','Australia','New Zealand','Canada','non-negotiable'):
            self.assertIn(term,a)
        for term in ('Current students','Graduate office','Never use','Rates require denominators'):
            self.assertIn(term,b)
    def test_main_skill_keep_8_and_no_portraits(self):
        s=(R/'SKILL.md').read_text()
        self.assertIn('eight dimensions internally',s)
        self.assertIn('without numbering or calling them “eight dimensions”',s)
        self.assertIn('no portraits, avatars',s)
        self.assertIn('supervisor-selection-methods.md',s)
    def test_audit_contains_rejections(self):
        s=(R/'docs/EVIDENCE_REVIEW.md').read_text()
        for t in ('Rejected','CNKI thesis pages','Demographic risk','SGSAH'):
            self.assertIn(t,s)
if __name__=='__main__':unittest.main()

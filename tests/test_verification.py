"""Known-error regression tests. Run with python -m unittest discover -s tests -v."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('vp',ROOT/'scripts'/'verify_publications.py')
vp=importlib.util.module_from_spec(spec);spec.loader.exec_module(vp)
CASES=json.loads((ROOT/'tests/fixtures/goldstone_cases.json').read_text())['items']
class PublicationGateTests(unittest.TestCase):
    def test_2011_false_solo_first_and_corresponding_is_rejected(self):
        r=vp.evaluate(CASES[0]);self.assertEqual(r['status'],'FAIL')
        self.assertTrue(any('Sole-first false' in x for x in r['errors']))
        self.assertTrue(any('Corresponding-author' in x for x in r['errors']))
        self.assertTrue(any('Independent PI' in x for x in r['review_required']))
    def test_2011_valid_cofirst_not_solo_first(self):
        r=vp.evaluate(CASES[1]);self.assertIn(r['status'],{'PASS_METADATA','REVIEW_REQUIRED'})
        self.assertIn('Co-first supported by supplied notes',r['checks'])
        self.assertEqual(r['errors'],[])
    def test_2024_wrong_doi_is_rejected(self):
        r=vp.evaluate(CASES[2]);self.assertEqual(r['status'],'FAIL')
        self.assertTrue(any('DOI mismatch' in x for x in r['errors']))
    def test_namesake_orcid_conflict_is_rejected(self):
        row={'claimed':{'researcher':'David C. Goldstone','doi':'10.1000/abc','title':'A title','year':2025,'orcid':'0000-0000-0000-0001'},
             'record':{'source':'https://example.org/article','doi':'10.1000/abc','title':'A title','year':2025,
                       'authors':[{'name':'David C. Goldstone','orcid':'0000-0000-0000-9999'}]}}
        r=vp.evaluate(row)
        self.assertIn('ORCID conflict for matched author',r['errors'])
    def test_independent_pi_always_requires_external_evidence(self):
        row=dict(CASES[1]);row['claimed']=dict(row['claimed']);row['claimed']['roles']=['independent_pi']
        r=vp.evaluate(row)
        self.assertEqual(r['status'],'REVIEW_REQUIRED')
    def test_doi_normalization(self):
        self.assertEqual(vp.doi('https://doi.org/10.1038/NATURE10623'),'10.1038/nature10623')
if __name__=='__main__':unittest.main()

"""Regression checks: eight peer-level topics are visible exactly once; no recap."""
import json,importlib.util,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qa',ROOT/'scripts'/'validate_report.py')
qa=importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
class IntegratedReportTests(unittest.TestCase):
    def test_all_eight_in_internal_map(self):
        path=ROOT/'examples'/'coverage-map.example.json'
        r=qa.coverage_check(path,None)
        self.assertEqual(r['errors'],[],str(r))
        self.assertEqual(r['stats']['dimensions_reported'],8)
    def test_missing_one_internal_dimension_fails(self):
        data=json.loads((ROOT/'examples'/'coverage-map.example.json').read_text())
        del data['dimensions']['communication']
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'map.json';p.write_text(json.dumps(data))
            r=qa.coverage_check(p,None)
        self.assertTrue(any('Missing coverage entry: communication' in x for x in r['errors']))
    def test_skills_prohibit_eight_dimension_recap(self):
        s=(ROOT/'SKILL.md').read_text()
        style=(ROOT/'references'/'academic-cv-style.md').read_text()
        self.assertIn('without numbering or calling them “eight dimensions”',s)
        self.assertIn('must be visible as peer-level headings',style)
    def test_template_has_no_portrait_and_no_redundant_recap(self):
        import zipfile
        p=ROOT/'assets'/'academic-cv-template.docx'
        with zipfile.ZipFile(p) as z:
            body=z.read('word/document.xml').decode('utf-8')
            self.assertNotIn('Eight Dimensions', body)
            self.assertNotIn('<wp:inline', body)

    def test_template_has_eight_peer_level_headings(self):
        from docx import Document
        names=['Identity and Background','Research Direction and Applicant Fit',
               'Research Output and Scientific Capability','Funding and Research Projects',
               'Student Supervision and Outcomes','Laboratory Culture and Team Practices',
               'Academic Reputation and External Recognition','Communication and Accessibility']
        d=Document(ROOT/'assets/academic-cv-template.docx')
        for name in names:
            matches=[p for p in d.paragraphs if p.text.strip()==name]
            self.assertEqual(len(matches),1,name)
            self.assertEqual(matches[0].style.name,'CV Section')
    def test_portrait_not_required_in_docx_check(self):
        p=ROOT/'assets'/'academic-cv-template.docx'
        r=qa.docx_check(p,template=True)
        self.assertEqual(r['errors'],[],r)
        self.assertEqual(r['stats']['embedded_image_files'],0)

    def test_template_still_valid(self):
        p=ROOT/'assets'/'academic-cv-template.docx'
        r=qa.docx_check(p,template=True)
        self.assertEqual(r['errors'],[],r)
if __name__=='__main__':unittest.main()

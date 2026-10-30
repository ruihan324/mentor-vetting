import importlib.util, re, unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('qa',ROOT/'scripts'/'validate_report.py')
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
class ProjectTests(unittest.TestCase):
    def test_skill_metadata_and_references(self):
        s=(ROOT/'SKILL.md').read_text()
        self.assertTrue(s.startswith('---\nname: mentor-vetting'))
        self.assertIn('description:',s[:1500])
        self.assertLess(len(s.splitlines()),250)
        for rel in re.findall(r'(?:references|assets|scripts)/[\w-]+\.(?:md|docx|py)',s):
            self.assertTrue((ROOT/rel).exists(),f'Missing resource {rel}')
        for i in range(1,9):
            self.assertIn(f'   {i}.',s)
    def test_template_docx_has_correct_a4_and_rules(self):
        p=ROOT/'assets/academic-cv-template.docx'
        self.assertTrue(zipfile.is_zipfile(p))
        r=qa.docx_check(p,template=True)
        self.assertEqual(r['errors'],[],str(r))
    def test_all_country_rules_present(self):
        for name in ('mainland-china','united-states','united-kingdom','canada','australia','new-zealand'):
            self.assertGreater((ROOT/'references'/f'{name}.md').stat().st_size,500)
if __name__=='__main__':unittest.main()

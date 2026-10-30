"""V5.6 output contract and topic-visibility regression checks."""
import unittest, tempfile, json, importlib.util
from pathlib import Path
from docx import Document
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('check',ROOT/'scripts/validate_report.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class WordOnly(unittest.TestCase):
    def test_word_only_policy(self):
        s=(ROOT/'SKILL.md').read_text()
        self.assertIn('Never generate, attach or offer a PDF version',s)
        self.assertIn('Deliver exactly one editable',s)
        self.assertNotIn('requested PDFs',s)
        style=(ROOT/'references/academic-cv-style.md').read_text()
        self.assertIn('Deliver only DOCX, never PDF',style)
    def test_coverage_requires_visible_heading_and_equal_style(self):
        path=ROOT/'examples/coverage-map.example.json'
        r=m.coverage_check(path,ROOT/'assets/academic-cv-template.docx')
        self.assertEqual(r['errors'],[],r)
        data=json.loads(path.read_text())
        data['dimensions']['reputation']['section']='Invented Phantom Heading'
        with tempfile.TemporaryDirectory() as td:
            q=Path(td)/'m.json';q.write_text(json.dumps(data))
            bad=m.coverage_check(q,ROOT/'assets/academic-cv-template.docx')
        self.assertTrue(any('Required peer-level topic heading missing' in x for x in bad['errors']))
    def test_eight_heading_names_are_directly_visible(self):
        d=Document(ROOT/'assets/academic-cv-template.docx')
        data=json.loads((ROOT/'examples/coverage-map.example.json').read_text())
        for row in data['dimensions'].values():
            name=row['section']; matches=[p for p in d.paragraphs if p.text.strip()==name]
            self.assertEqual(len(matches),1,name)
            self.assertEqual(matches[0].style.name,'CV Section')
    def test_chinese_translated_topic_headings_map(self):
        names=['身份与背景','研究方向与适配性','科研成果与研究能力','基金与项目',
               '学生指导与培养结果','实验室与团队氛围','学术声誉与外部认可','沟通与指导可得性']
        keys=['background','research_fit','research_output','funding',
              'supervision','lab_culture','reputation','communication']
        data=json.loads((ROOT/'examples/coverage-map.example.json').read_text())
        d=Document(ROOT/'assets/academic-cv-template.docx')
        for key,name in zip(keys,names):
            old=data['dimensions'][key]['section']
            for pp in d.paragraphs:
                if pp.text.strip()==old:
                    pp.text=name
                    break
            data['dimensions'][key]['section']=name
        with tempfile.TemporaryDirectory() as td:
            doc=Path(td)/'translated.docx';cov=Path(td)/'coverage.json'
            d.save(doc);cov.write_text(json.dumps(data,ensure_ascii=False))
            r=m.coverage_check(cov,doc)
        self.assertEqual(r['errors'],[],r)
    def test_no_pdf_arg_in_validator(self):
        script=(ROOT/'scripts/validate_report.py').read_text()
        self.assertNotIn('def pdf_check(',script)
        self.assertNotIn('args.pdf',script)
if __name__=='__main__':unittest.main()

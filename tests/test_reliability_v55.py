"""Regression tests for previous false-positive structural validation."""
import unittest, tempfile, zipfile, io, json, importlib.util
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('report_qa',ROOT/'scripts/validate_report.py')
qa=importlib.util.module_from_spec(spec);spec.loader.exec_module(qa)
spec2=importlib.util.spec_from_file_location('claim_qa',ROOT/'scripts/check_selection_evidence.py')
cq=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(cq)

class NoFalsePass(unittest.TestCase):
    def test_orphan_link_relationship_does_not_count(self):
        template=ROOT/'assets/academic-cv-template.docx'
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'fake-link.docx'
            with zipfile.ZipFile(template,'r') as src, zipfile.ZipFile(target,'w') as dst:
                for member in src.infolist():
                    data=src.read(member.filename)
                    if member.filename=='word/_rels/document.xml.rels':
                        data=data.replace(b'</Relationships>',b'<Relationship Id="rId9999" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="https://example.org" TargetMode="External"/></Relationships>')
                    dst.writestr(member,data)
            result=qa.docx_check(target)
            self.assertTrue(any('No used external clickable hyperlink' in msg for msg in result['errors']),result)
    def test_portrait_file_rejected_for_normal_report(self):
        template=ROOT/'assets/academic-cv-template.docx'
        with tempfile.TemporaryDirectory() as tmp:
            target=Path(tmp)/'picture.docx'
            with zipfile.ZipFile(template,'r') as src, zipfile.ZipFile(target,'w') as dst:
                for member in src.infolist():dst.writestr(member,src.read(member.filename))
                dst.writestr('word/media/avatar.png',b'not-a-real-png')
            r=qa.docx_check(target)
            self.assertTrue(any('Embedded images' in x for x in r['errors']))
    def test_verified_record_needs_specific_link(self):
        data={'claims':[{'id':'x','kind':'funding','status':'Verified','sources':[{'type':'official'}]}]}
        self.assertTrue(any('specific source URL' in x for x in cq.review(data)))
    def test_dated_private_interview_does_not_require_public_url(self):
        account={'claims':[{'id':'int','kind':'student_experience','status':'Verified',
                             'sources':[{'type':'primary_interview','date':'2026-10-30','role':'former student'}]}]}
        self.assertEqual(cq.review(account),[])

    def test_main_skill_metadata_root_match(self):
        t=(ROOT/'SKILL.md').read_text(encoding='utf-8')
        self.assertEqual(ROOT.name,'mentor-vetting')
        self.assertIn('name: mentor-vetting',t[:200])
        self.assertIn('5.6.0-beta.1',t)

if __name__=='__main__':unittest.main()

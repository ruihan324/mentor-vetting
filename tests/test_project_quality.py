import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProjectQualityRules(unittest.TestCase):
    def test_project_rules_loaded(self):
        s=(ROOT/'SKILL.md').read_text()
        self.assertIn('project-quality-and-sources.md',s)
        self.assertIn('Current-project claims',s)
    def test_dimensions_all_internal(self):
        e=(ROOT/'references/evaluation.md').read_text()
        for n in range(1,9): self.assertIn(f'Dimension {n} ',e)
        self.assertIn('eight topic headings exactly once',e)
    def test_project_status_and_source_bias(self):
        p=(ROOT/'references/project-quality-and-sources.md').read_text()
        for term in ('Significance','Originality','Rigor','Feasibility','Student pathway','Source channel','Reddit','not proof of successful execution'):
            self.assertIn(term,p)
    def test_case_does_not_elevate_advertised_project_to_funded_place(self):
        import json
        case=json.loads((ROOT/'examples/tristan-de-rond-2026-public-case.json').read_text())
        self.assertEqual(case['verified_project_funding']['current_balance'],'Unknown')
        for row in case['advertised_2026_projects']:
            self.assertEqual(row['funded_student_place'],'Unknown')
            self.assertEqual(row['methods_rigor'],'Unknown')
    def test_no_portrait_requirement(self):
        s=(ROOT/'SKILL.md').read_text()
        self.assertIn('text-only',s.lower())
if __name__=='__main__': unittest.main()

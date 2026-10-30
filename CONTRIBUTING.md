# Contributing to Mentor Vetting

All code, skill instructions, documentation, and test cases are in English so international contributors can review them. Dossier language must still follow the end user's language.

## How to propose changes

1. Open an issue describing a **reproducible problem**, ideally with public institutional/publisher URLs and access dates.
2. Classify the issue as: **skill instruction defect**, **agent/tool execution defect**, **source/evidence coverage gap**, **template defect**, or **country-policy update**.
3. Suggest the smallest improvement that preserves the original eight dimensions, supported regions, accuracy requirements, and traditional Academic CV output.
4. For factual changes supply reliable primary records and indicate publication date, author-role notes, and affiliation evidence. Do not post third-party private communications or anonymous defamatory accusations.
5. For code changes, add tests; run `python -m unittest discover -s tests -v` and include console output.
6. For DOCX changes, provide safe/redacted page previews and the output of `scripts/validate_report.py`. No real person's sensitive information in fixtures.

## What good tests look like

- Wrong DOI versus correct original article title.
- An author is co-first but incorrectly called sole-first or corresponding.
- Name collision between people at different institutions.
- University title mistaken for graduate admission eligibility.
- An expired grant incorrectly called a current funded studentship.
- A DOCX missing full-width black section rules, A4 sizing, proper date/details alignment, functional links, or sensible pagination.

Regression tests should fail for false assertions, not simply pass if the report exists. Prefer source citations in fixture notes. Distinguish deterministic metadata checks from substantive scholarly judgment.

## Security, ethics and licensing

Do not publish applicant records, identifiable student interviews, nonpublic correspondence, or unsupported allegations. Do not contribute AI-generated photographs of real people. The project is licensed under the [MIT License](LICENSE); by contributing you agree to license your contributions under the same terms.

## Project boundaries

- Exactly eight named, peer-level content sections without a second eight-point summary.
- Mainland China, USA, UK, Canada, Australia, New Zealand only.
- Output only editable Word DOCX; report language follows the question.
- Traditional black-and-white academic CV style, not a colored dashboard.
- No fake faces, fabricated metrics, invented sources or pseudo-exact admission probabilities.


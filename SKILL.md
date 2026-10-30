---
name: mentor-vetting
description: >-
  Research and verify academic supervisors, principal investigators and their laboratories.
  Use for mentor due diligence, professor background checks, research-project assessment,
  PhD/master's supervisor choice and multi-supervisor comparisons. Supports Mainland China,
  the United States, United Kingdom, Canada, Australia and New Zealand. Creates evidence-linked,
  editable Word (.docx) reports only; never generates PDF deliverables.
metadata:
  version: "5.6.0-beta.1"
---

# Mentor Vetting

Investigate the named researcher at the named institution and give a **source-supported, decision-useful assessment**. Verify identity before attributing achievements. Public records are not proof of private conduct; never invent missing evidence, student outcomes, current vacancies, funding, interviews or admission odds.

## Load only relevant references

- **Always:** `references/verification.md` and `references/evaluation.md` (identity, standards and the eight mandatory internal dimensions).
- **Country-specific:** load only the matching `references/mainland-china.md`, `references/united-states.md`, `references/united-kingdom.md`, `references/canada.md`, `references/australia.md`, or `references/new-zealand.md`. Check actual programme policies, not assumed national rules.
- **Selection/comparison requests:** `references/supervisor-selection-methods.md` and `references/supervision-and-fit.md`. For team experiences or interview questions, also load `references/interviews-and-risk-signals.md`.
- **Current-project claims or disputed source reliability:** `references/project-quality-and-sources.md`.
- **When producing the Word report:** `references/academic-cv-style.md` and, when accessible, `assets/academic-cv-template.docx`.

## Research workflow

1. **Disambiguate** person, affiliation, name variants, ORCID, year and coauthors using an institutional source plus corroboration. Keep uncertain namesakes out of totals.
2. **Establish purpose and programme route:** master's, PhD, postdoc or collaboration; actual country, entry model, funding eligibility, applicant requirements and study duration. No unsolicited contact with the researcher or students.
3. **Investigate these eight dimensions internally**, recording one outcome or documented evidence gap for each:
   1. Research output and publication quality
   2. Grants, funding and research resources
   3. Student supervision and outcomes
   4. Laboratory and team culture
   5. Academic and professional reputation
   6. Education and professional background
   7. Research agenda and applicant fit
   8. Communication and accessibility
4. **Verify consequential claims at original sources:** DOI, title, journal, year, full author list, equal-first/corresponding notes, documented contributions, grant role/dates, supervision eligibility, actual research/project resources. A publication position alone does not establish independent PI leadership. No graduation/dropout/delay rate without a complete entering cohort and verified outcomes.
5. **Assess representative science:** select three to five research outputs (or all if fewer), giving the scientific question, methods, actual findings, the researcher's substantiated role, significance, and limits. Mark abstract-only assessments. Compare only reasonable field- and career-stage peers.
6. **Assess current projects independently:** significance, novelty, methods/controls, feasibility, staffing, equipment, verified available funding, student ownership, milestones, contingency and transferable skills. A project advertisement does not prove feasibility or an available funded place.
7. **Separate conclusions:** research achievement/current scientific capability; current project quality/readiness; supervision evidence/applicant fit. For multiple candidates compare non-negotiable eligibility first, then documented trade-offs. Do not assign pseudo-precise scores.
8. **Record evidence:** original page URL, issuer, event/publication date, checked date, researcher match, supporting and conflicting facts, and status: `Verified`, `Partially supported`, `Needs confirmation`, `Not found` or `Not applicable`. An absent record is not evidence that something does not exist. Community anecdotes prompt questions, not accusations.
9. **Stop efficiently:** once material claims have sufficient corroboration, avoid redundant searches; for inaccessible records stop and label the gap. `Preliminary public-information investigation` is the default. Claim `In-depth public-record verification` or `Key training/resource facts verified` only if the explicit gates in `references/verification.md` were met.

## Concise report output

Deliver exactly one editable **A4 Word (.docx) report**. Never generate, attach or offer a PDF version; internal rendering to images for inspection is permitted. Report language follows the user's query; retain official titles and article names verbatim. Use a **black-and-white traditional Academic CV**, not a dashboard. Center the text-only identity block; **no portraits, avatars or silhouettes**. Clearly label it an *independent public-source assessment*, never the researcher's official CV. Show date, country, and honest completion level on page 1.

**Keep all eight assessment topics visible as ordinary, equal-level CV section headings**, without numbering or calling them “eight dimensions”. Use exactly one main section for each topic, with report-language equivalents:

- **Identity and Background** — degrees, institutional appointment, position and eligibility (background).
- **Research Direction and Applicant Fit** — scientific agenda, methods and relevant skill fit (research_fit).
- **Research Output and Scientific Capability** — selected full citations and immediately adjacent, non-duplicative representative-work analysis (research_output).
- **Funding and Research Projects** — grant roles, equipment, current projects, scientific significance, feasibility and resource uncertainty in one place (funding).
- **Student Supervision and Outcomes** — verified students, training, completion evidence and career outcomes (supervision).
- **Laboratory Culture and Team Practices** — independently supported working practices, not personality conjecture (lab_culture).
- **Academic Reputation and External Recognition** — documented peer recognition and collaborations not already itemized (reputation).
- **Communication and Accessibility** — feedback practices and availability limits; show public email once in the centered header, not again here (communication).

These are **equal-level main sections**—the research and supervision topics use exactly the same heading style as the identity and funding topics—not a separate recap or checklist. Every subject appears once in its own section; missing evidence receives one concise, explicit line. Follow with **Brief Decision and Open Questions** (three separate judgments and 3–7 non-generic questions without re-listing facts) and **Sources and Verification** (working primary links). Do not repeat an item in a second section, add filler, force a fixed page count, or insert generic compliments. An internal coverage map records the status of each topic (see `examples/coverage-map.example.json`).

Before delivery run source review, where executable `scripts/verify_publications.py`, `scripts/check_selection_evidence.py` when relevant, and `scripts/validate_report.py` with the internal coverage map. The scripts check declared data, **not source truth**. Render the DOCX internally to page images and visually inspect every page; check legibility, A4, borders, links, orphan headings and the absence of portraits. Claim tests were passed only if actually run. Link only files that actually exist. List unresolved evidence limits without repeating the report.

## Safety and judgment boundaries

No inference of misconduct, personality, work ethic or acceptance probability from demographics, title, single emails, anonymous posts or invented “coded speech.” Allegations require careful attribution and verified proceedings before stating an established finding. Current grant totals are not discretionary student money; student coauthorship is not graduation evidence; an eligible supervisor may have no current vacancy. No third-party messages without explicit user instruction.

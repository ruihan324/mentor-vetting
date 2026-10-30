# Mentor Vetting

An evidence-first academic supervisor due-diligence agent skill. Given a researcher and an institution, it verifies identity and contribution records, then produces a source-linked, decision-useful assessment as an editable Word document.

**Current release:** `5.6.0-beta.1` (pre-release).

## Overview

Mentor Vetting researches, evaluates, and compares academic supervisors and principal investigators for prospective master's, PhD, postdoctoral, and collaboration decisions. It does not guess: every consequential claim is checked against primary sources, and missing evidence is labelled rather than invented.

## Key features

- **Identity-first verification** — disambiguates namesakes, name variants, ORCID records, and affiliation before attributing any achievement.
- **Eight-dimension evaluation** — research output and publication quality, grants and funding, student supervision and outcomes, laboratory and team culture, academic reputation, education and background, research agenda and applicant fit, and communication and accessibility.
- **Project-quality assessment** — separates achieved science from current project feasibility, available funding, staffing, and readiness.
- **Supervision and fit analysis** — evaluates mentoring evidence and research-direction fit for the applicant.
- **Source-linked reporting** — every key claim carries a working primary link and a verification status.
- **Rumor-safe** — unverified community anecdotes prompt questions, never accusations or fabricated facts.

## Supported education systems

- Mainland China
- United States
- United Kingdom
- Canada
- Australia
- New Zealand

Country-specific rules are loaded on demand so that programme policies, funding eligibility, and admission requirements are checked against actual institutional sources rather than assumed national rules.

## Installation

Copy the complete `mentor-vetting/` directory into your agent's skills folder, preserving `SKILL.md`, `references/`, `assets/`, and `scripts/`. Resource loading and Word generation vary by agent; consult your agent's documentation. The underlying directory format follows the [Agent Skills specification](https://agentskills.io/specification).

## Usage

> Evaluate Tristan de Rond at the University of Auckland as a potential research supervisor. Distinguish his published contributions, current proposed projects, and evidence of mentoring. Produce only an evidence-linked editable Word (.docx) report in Chinese.

- Report language follows the query language; skill instructions remain in English.
- The report is a third-party assessment, not the researcher's CV or an institutional endorsement.
- Word-only A4 black-and-white traditional academic CV, with eight visible peer-level topic headings and live citation links; no portraits or decorative profile cards.
- Missing primary evidence is marked unknown rather than filled by guesswork.
- Do not use this project to harass, publicly accuse, or reveal private student information.

## Download

- **Source:** `Code → Download ZIP` on the repository home page, or `git clone https://github.com/ruihan324/mentor-vetting.git`.
- **Release package:** the complete skill archive `mentor-vetting-v5.6.0-beta.1.zip` is attached to the [v5.6.0-beta.1 release](releases/tag/v5.6.0-beta.1).

## Known limitations

- The skill is a **beta** pre-release and has not been tested end-to-end in every agent runtime.
- Public records cannot establish private laboratory conduct, current vacancies, or admission outcomes.
- Word generation and `references/` loading require agent support; `scripts/` are optional with manual fallback.
- Automated scripts validate declared data and document structure, not source truth or subjective judgment.
- Online DOI verification requires a live network connection and does not verify equal-authorship or independent-PI claims.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports, country-policy updates, and regression tests are welcome. Please read [SECURITY.md](SECURITY.md) before reporting privacy or safety issues.

## License

Released under the [MIT License](LICENSE). Copyright © 2026 Ruihan Sun (孙瑞涵).

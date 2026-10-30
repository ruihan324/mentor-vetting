# V5.6.0-beta.1 — Release QA

- Source: V5.5 release candidate, updated to Word-only and visible, peer-level content topics.
- Offline unit tests: **37 passing** (Python 3.13 local runtime). Actual command: `python -m unittest discover -s tests -v`.
- Blank Word master `assets/academic-cv-template.docx`: A4 portrait, **10 full-width heading borders**, **eight named topic sections on the same heading level**, and no embedded portrait; `scripts/validate_report.py --template` passes.
- Word master rendered for visual QA: **one A4 page**, no stray overflow page, no clipping or overlapping text; final generated reports can use natural multiple pages.
- Internal coverage sample: all eight categories map to unique, visible headings; the validator rejects missing/duplicated headings and unequal heading styles when a coverage map is supplied.
- Output policy: **DOCX only**. No PDF is generated or delivered; rendered images are internal QA only.
- Not tested here: WorkBuddy runtime, end-to-end live mentor investigation, online Crossref verification, current third-party content accuracy, actual token cost, client download behavior.
- Automated checks verify structural consistency and declared evidence, **not primary-source scientific truth**.
- Before open-source release, owner must confirm Word template redistribution rights and choose an explicit license.

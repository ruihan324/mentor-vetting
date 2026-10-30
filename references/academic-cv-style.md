# Traditional Academic CV report design and document QA

Read ONLY when building or validating the deliverable. Academic CV style does not imply that the document was authored or endorsed by the researcher; include an independent review label.

## 8. Document specification: classic timeline-style Academic CV

### 8.1 Only approved default visual language

**Do not interpret "Academic CV" as a dark sidebar, colorful profile cards, dashboard, modern corporate résumé, magazine layout, or decorative cover-based due-diligence report.** The default follows a traditional time-aligned scholarly CV:

- **A4 portrait**, plain white paper, black text, **single main column**, classic serif type. Natural pagination with **no page count cap**.
- Center **name, lab/research group, institution, and publicly listed institutional email** on successive lines; bold the name and retain generous top whitespace.
- Left-align section headings in **bold**, with a **solid black paragraph bottom border across the full text width**, identical thickness and spacing throughout. This is not merely underlined text.
- Education, appointments, honors, grants, and dated research projects use **borderless two-column entries: about 20% dates/periods and 80% details**. This is a *date/details table*, **not the old 1:2 portrait sidebar**. The date cell has no colored fill. Bold the role/degree in the first detail line; use normal text for supporting lines; italicize dissertation titles where appropriate.
- **Complete scholarly citations:** authors, year, original title, journal, volume/issue/pages, DOI; bold the subject researcher's name; use consistent hanging indents and citation conventions appropriate to the field. DOI links must remain clickable.
- Analytical sections use **the same heading + black rule + prose**. Compact numbered lists are acceptable. No shadows, banners, icons, tinted badges, progress bars, or decorative cards.
- Secondary details (dates, provenance, notes) may be gray. Hyperlinks must work in Word, but avoid saturated blocks of colored URLs in print.
- No decorative cover or compulsory contents page. A small gray footer may show `Last checked | Page N`.

### 8.2 Physical layout and typography: validate after generation

| Item | Mandatory/allowed specification |
|---|---|
| Page | A4 210 × 297 mm; Word `w:pgSz` 11906 × 16838 twips; **not US Letter** |
| Margins | Left/right 2.4–2.6 cm; top/bottom approximately 2.0–2.3 cm; slight adjustments only to avoid clipping |
| Body font | Times New Roman; Tinos as compatible fallback; for Chinese reports, SimSun, Source Han Serif, or Noto Serif CJK SC |
| Name | 15–17 pt, centered, bold |
| Lab/institution/email | 10.5–12 pt, centered; four-line identity block; italic email permitted |
| Section heading | 11–12 pt, bold, 1–1.5 pt **black bottom rule spanning the text area** |
| Body | 10–11 pt; 1.05–1.18 line spacing; 3–6 pt after paragraph |
| Date/detail entry | Borderless left ~19–23%, right ~77–81%; consistent throughout |
| Publication list | Full citations, researcher's name bold; 0.45–0.65 cm hanging indent |
| Headers/footers | No banner on first page; consistent pagination and understated footers |

**The reference visual is a date/detail CV, not a 1:2 profile sidebar.** Do not carry over the old precise 1:2 dark-sidebar XML requirements. The date/detail proportions are intentional and separate.

### 8.3 Text-only identity block (mandatory)

**No portrait, avatar, photo, or default silhouette appears in the report.** The header contains centered name, laboratory or department (if verified), institution and public institutional email as text only. Do not search for photos or add an empty picture placeholder. Scientific figures are separate from personal portraits and may appear only if specifically requested and properly sourced.

### 8.4 Report structure: eight visible, non-repeated peer-level topics

**Required reader-facing sections, with exactly one main heading for each.** These are content sections, *not* a special eight-dimension scorecard. They share the same Word `CV Section` heading style, size and full-width black rule as any other main heading. Translate headings into the query language. Use these stable names (or direct, unambiguous translations) so coverage can be checked against the DOCX:

| Internal key | English main heading | Chinese main heading | Put here, once |
| --- | --- | --- | --- |
| background | Identity and Background | 身份与背景 | Verified identity, degree, affiliations, timeline, eligibility |
| research_fit | Research Direction and Applicant Fit | 研究方向与适配性 | Scientific questions, methods, applicant's research goals and skills |
| research_output | Research Output and Scientific Capability | 科研成果与研究能力 | Full citation once for selected works, followed by representative-work interpretation referring to numbered entries |
| funding | Funding and Research Projects | 基金与项目 | PI/co-PI project roles, amounts/dates, research facilities, **current scientific project quality and feasibility** |
| supervision | Student Supervision and Outcomes | 学生指导与培养结果 | Verified mentoring roles, student training, graduation and careers; unknowns identified |
| lab_culture | Laboratory Culture and Team Practices | 实验室与团队氛围 | Corroborated conditions, work expectations, lab stability; no stereotypes |
| reputation | Academic Reputation and External Recognition | 学术声誉与外部认可 | Documented recognition and independent field reception, not a repeat of paper list or awards already itemized |
| communication | Communication and Accessibility | 沟通与指导可得性 | Evidence of meeting/feedback practice and availability; public email appears only in the header |

After those eight normal sections, add only:

- **Brief Decision and Open Questions / 综合判断与待核实问题:** concise separate judgments on researcher ability, *current* project, and mentoring/fit; 3–7 targeted questions; no duplicated numerical or bibliographic facts.
- **Sources and Verification / 来源与核验:** live links, dates and material evidence limitations, without duplicating the analysis.

The eight topics are also tracked in the internal coverage JSON. **Never introduce “Eight Dimensions”, “八维评价”, a second eight-point recap, a separate scorecard, or one repeated fact under multiple topics.** Unlike previous versions, the eight topic names **must be visible as peer-level headings**; they must not disappear into an undifferentiated supervision/environment section. For absent evidence, keep the heading and write one brief 'Not publicly verified' statement, not several speculative paragraphs.

Use the dated borderless table where meaningful (degree, appointment, grants); all non-dated narrative is plain editable prose. Avoid repeating complete citations in analysis or grant amounts in the conclusion. Do not fabricate filler to fill pages. The independent third-party assessment label is mandatory.

### 8.5 Accompanying Word template (recommended)

If `assets/academic-cv-template.docx` is present in the installed skill folder, use its `CV Section` style, centered four-line identity block, borderless date/detail table, and hanging publication indents. Replace **all** template placeholders with verified facts and omit irrelevant example content. If the template is absent, still reproduce Sections 8.1–8.4 using native DOCX styles; **do not fall back** to the earlier colorful profile layout.

### 8.6 Word-only creation and inspection

1. Use native Word paragraph styles with bottom borders, borderless date tables, and live text; never compose whole pages as a pasted image.
2. Keep the centered four-line header, aligned date entries, section rules, and publication indents consistent across the entire report.
3. Validate fonts, sizes, A4, margins, section/page breaks, widow/orphan behavior, and excessive whitespace. Allow natural flow; do not force each dimension onto its own page.
4. DOCX must contain real external clickable hyperlink relationships. **Deliver only DOCX, never PDF.** Internal conversion to page PNGs for quality review is permitted.
5. Render **every Word page to PNG** and inspect it: no garbled glyphs, squeezed date columns, inconsistent rule lengths, overlapping citations, orphaned headings, or stranded `Analysis`/`Limitations` paragraphs.
6. When an example screenshot is provided, produce a first-page preview and compare centered header, black rules, date/detail alignment, and absence of color blocks. Rework if materially inconsistent.
7. Display the honest **Level 1/2/3 investigation status** on page one. A longer report does not imply deeper verification.

---

### Document acceptance

- [ ] Page 1 matches a classic chronological CV: centered name/institution, **black full-width section rules**, white paper, Times-family serif, dates on left/details on right; no dark sidebar, colored tiles, or decorative cover.
- [ ] Eight named topics appear exactly once as equal-level report headings and each maps to a verified/gap entry; no additional recap or repeated research claims.
- [ ] Analyzed 3–5 representative outputs (or every identified work if fewer) beyond mere bibliographic listings; properly flagged abstract-based analyses.
- [ ] Field comparisons have defensible selection criteria and sources; no invented ranking when peers cannot be matched.
- [ ] Investigation completion level is candid and supported by evidence.
- [ ] Every page is A4 portrait (`w:pgSz` 11906 × 16838 twips), **never Letter**.
- [ ] No one-page restriction; no hidden content, clipped text, or tiny print to reduce page count.
- [ ] All pages use consistent single-column classic CV typography and no large colored cards or profile sidebars.
- [ ] Centered identity block contains text only, without headshot, avatar, silhouette or empty picture placeholder.
- [ ] Rendered and inspected **every page**, with no blank overflow pages, stranded headings, broken tables, deformed research figures (if any), or broken links.
- [ ] Only an editable DOCX is delivered, with live links; no PDF deliverable is created.
- [ ] Clearly disclosed any verification or rendering checks that could not actually be performed; never falsely claim a file passed QA.

When delivering, briefly summarize the **most important strength, material concern, and leading evidence gap**, and provide verified working file links. Do not deliver merely a filename, document title, or an inaccessible path.

---

#!/usr/bin/env python3
"""Offline Word-only DOCX structural QA; visual render inspection remains mandatory.
Usage: python scripts/validate_report.py REPORT.docx [--coverage coverage.json] [--template]
Checks eight visible, peer-level headings by internal coverage map; this does not verify source truth.
"""
import argparse,json,sys,zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
REL_NS="{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
W='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
WP='{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
R='{http://schemas.openxmlformats.org/package/2006/relationships}'

def docx_check(path,template=False,allow_figures=False):
    errors=[];warnings=[];stats={}
    with zipfile.ZipFile(path) as z:
        root=ET.fromstring(z.read('word/document.xml'))
        docxml=z.read('word/document.xml').decode('utf-8')
        texts=[e.text or '' for e in root.iter(W+'t')]
        content=' '.join(texts)
        sects=list(root.iter(W+'sectPr'))
        sizes=[]
        for sect in sects:
            sz=sect.find(W+'pgSz')
            if sz is not None:sizes.append([int(sz.get(W+'w','0')),int(sz.get(W+'h','0'))])
        if not sizes or any(abs(w-11906)>3 or abs(h-16838)>3 for w,h in sizes):errors.append('Expected A4 portrait 11906x16838 twips on every section')
        stats['section_page_sizes_twips']=sizes
        bdr=len(list(root.iter(W+'pBdr')))
        if bdr<2:errors.append('Section heading bottom borders/rules appear absent (<2 paragraph border groups)')
        stats['paragraph_border_groups']=bdr
        stats['tables']=len(list(root.iter(W+'tbl')))
        if not template:
            # Visible topic headings are required; a second recap or scorecard is not.
            heading_titles=('findings in eight dimensions','eight investigative dimensions','八维背调结果','八维评价','八项维度总结')
            lower=content.casefold()
            if any(h in lower for h in heading_titles):
                errors.append('Redundant standalone eight-dimension report section detected')
        if 'word/_rels/document.xml.rels' in z.namelist():
            rels=ET.fromstring(z.read('word/_rels/document.xml.rels'))
            links={e.get('Id'):e.get('Target','') for e in rels if
                   e.get('Type','').endswith('/hyperlink') and e.get('TargetMode')=='External'
                   and e.get('Target','').startswith(('https://','http://'))}
        else:links={}
        used=[e.get(REL_NS+'id') for e in root.iter(W+'hyperlink') if e.get(REL_NS+'id')]
        valid=[rid for rid in used if rid in links]
        stats['external_link_relationships']=len(links)
        stats['clickable_external_hyperlinks']=len(valid)
        if not template and not valid:
            errors.append('No used external clickable hyperlink relationship in DOCX body')
        dangling=[rid for rid in used if rid not in links]
        if dangling: errors.append('DOCX hyperlink references missing an external HTTP(S) target: '+str(len(dangling)))
        image_count=len([n for n in z.namelist() if n.startswith('word/media/') and not n.endswith('/')])
        stats['embedded_image_files']=image_count
        extent=[(int(e.get('cx','0')),int(e.get('cy','0'))) for e in root.iter(WP+'extent')]
        stats['drawing_extents_emu']=extent
        if image_count:
            if not template and not allow_figures:
                errors.append('Embedded images found; portraits forbidden; use --allow-figures only for requested sourced research figures')
            else:
                warnings.append('Images included: ensure no portraits, avatars or unsourced figures')
        if template:warnings.append('Template mode: populated citations/links/dimensions not required')
        if len(content)<100:warnings.append('Very little document text; check visual result')
    return {'errors':errors,'warnings':warnings,'stats':stats}

REQUIRED_DIMENSIONS=('research_output','funding','supervision','lab_culture',
                     'reputation','background','research_fit','communication')
ALLOWED_STATUSES=('Verified','Partially supported','Needs confirmation','Not found','Not applicable')

def coverage_check(path,docx):
    """An external checklist verifies investigation coverage without printing it in the CV.

    This check validates the *declarations*, not the truth of external evidence.
    """
    errors=[];warnings=[];stats={}
    data=json.loads(Path(path).read_text(encoding='utf-8'))
    dim=data.get('dimensions',{})
    stats['dimensions_reported']=len(dim)
    for key in REQUIRED_DIMENSIONS:
        record=dim.get(key)
        if not isinstance(record,dict):
            errors.append('Missing coverage entry: '+key);continue
        status=record.get('status','')
        if status not in ALLOWED_STATUSES:errors.append('Invalid status for '+key+': '+repr(status))
        section=(record.get('section') or '').strip()
        finding=(record.get('finding') or '').strip()
        if not section:errors.append('No natural report section declared for '+key)
        if not finding:errors.append('No substantive evidence/unknowns note for '+key)
    extra=set(dim)-set(REQUIRED_DIMENSIONS)
    if extra:warnings.append('Unknown extra dimension keys: '+', '.join(sorted(extra)))
    # Every internally mapped topic must have its own peer-level styled heading, not a plain-text mention.
    if docx is not None:
        with zipfile.ZipFile(docx) as z:
            root=ET.fromstring(z.read('word/document.xml'))
        heading_to_styles={}
        for para in root.iter(W+'p'):
            text=''.join(x.text or '' for x in para.iter(W+'t')).strip()
            ppr=para.find(W+'pPr')
            sty=ppr.find(W+'pStyle') if ppr is not None else None
            style=sty.get(W+'val','') if sty is not None else ''
            if text and style:
                heading_to_styles.setdefault(text.casefold(),[]).append(style)
        main_styles=[]
        for key in REQUIRED_DIMENSIONS:
            row=dim.get(key)
            if isinstance(row,dict) and (row.get('section') or '').strip():
                title=row['section'].strip()
                matches=heading_to_styles.get(title.casefold(),[])
                if len(matches)!=1:
                    errors.append('Required peer-level topic heading missing or duplicated: '+key+' -> '+title)
                else:
                    main_styles.append(matches[0])
        if main_styles and len(set(main_styles))>1:
            errors.append('The eight topic headings must share one equal-level paragraph style')
    warnings.append('Coverage map verifies declarations and section placement, not original-source facts')
    return {'errors':errors,'warnings':warnings,'stats':stats}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('docx');p.add_argument('--template',action='store_true')
    p.add_argument('--allow-figures',action='store_true',help='Allow explicitly requested, sourced scientific figures; no portraits')
    p.add_argument('--coverage',help='Internal eight-dimension coverage JSON')
    p.add_argument('--output');args=p.parse_args()
    x=docx_check(args.docx,args.template,args.allow_figures)
    cv=coverage_check(args.coverage,args.docx) if args.coverage else None
    if not args.template and not args.coverage: x['warnings'].append('No internal coverage map supplied: eight-dimension research completeness not validated')
    result={'docx':x,'coverage':cv,
            'visual_inspection':'NOT PERFORMED — render Word pages to images and inspect manually',
            'source_integrity':'NOT PERFORMED — individually open primary research records'}
    result['passed_structural_checks']=not x['errors'] and (not cv or not cv['errors'])
    txt=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:Path(args.output).write_text(txt+'\n',encoding='utf-8')
    print(txt)
    return 0 if result['passed_structural_checks'] else 1
if __name__=='__main__':sys.exit(main())

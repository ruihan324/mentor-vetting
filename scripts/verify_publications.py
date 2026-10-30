#!/usr/bin/env python3
"""Offline publication-evidence pre-screen; never certifies authorship or PI independence.

Input JSON: {"items": [{"claimed": {"doi": "...", "title": "...", "year": 2011,
"researcher": "David C. Goldstone", "orcid": "...", "affiliation": "...",
"roles": ["co_first_author", "corresponding_author", "independent_pi"]},
"record": {"doi": "...", "title": "...", "year": 2011,
"authors": [{"name": "...", "orcid": "...", "affiliations": ["..."]}],
"equal_first": ["..."], "corresponding": ["..."],
"role_source": "https://publisher.example/fulltext", "source": "https://..."}}]}

Publisher contribution notes MUST be independently inspected. `record` is supplied data,
not automatically trusted. Returns structured PASS/FAIL/REVIEW; FAIL exits nonzero.
Use --online-crossref for optional live bibliographic checking; publisher author notes remain manual.
"""
import argparse, json, re, sys, unicodedata
from urllib.request import Request, urlopen
from urllib.parse import quote
from difflib import SequenceMatcher
from pathlib import Path

def norm(s):
    s=unicodedata.normalize('NFKD',str(s or '')).casefold()
    return re.sub(r'[^a-z0-9\u4e00-\u9fff]+','',s)

def doi(s):
    s=str(s or '').strip().lower()
    s=re.sub(r'^https?://(?:dx\.)?doi\.org/','',s)
    return re.sub(r'^doi:\s*','',s)

def similar(a,b):
    if not a or not b:return 0
    return SequenceMatcher(None,norm(a),norm(b)).ratio()

def evaluate(item):
    c=item.get('claimed',{});r=item.get('record',{})
    fails=[];reviews=[];passes=[]
    if not r.get('source'):reviews.append('No original record URL supplied')
    cd,rd=doi(c.get('doi')),doi(r.get('doi'))
    if not cd or not rd:reviews.append('DOI missing; cannot confirm identifier')
    elif cd!=rd:fails.append(f'DOI mismatch: {cd} != {rd}')
    else:passes.append('DOI identical')
    cs,rs=c.get('title'),r.get('title')
    if cs and rs:
        score=similar(cs,rs)
        if score < 0.90:fails.append(f'Title mismatch ({score:.2f} similarity)')
        else:passes.append('Title consistent')
    else:reviews.append('Title not checked')
    if c.get('year') and r.get('year'):
        if int(c['year'])!=int(r['year']):fails.append('Publication year differs')
        else:passes.append('Year matches')
    else:reviews.append('Year not checked')
    name=c.get('researcher','')
    authors=r.get('authors',[])
    matches=[(i,a) for i,a in enumerate(authors) if similar(a.get('name'),name)>.88]
    if not name or not authors:reviews.append('Target author identity not evaluable')
    elif not matches:fails.append('Researcher not present in cited author list')
    elif len(matches)>1:reviews.append('Several author-name matches; disambiguation required')
    else:
        idx,author=matches[0]
        co=c.get('orcid')
        if co and author.get('orcid'):
            if co.casefold()!=author['orcid'].casefold():fails.append('ORCID conflict for matched author')
            else:passes.append('ORCID matches')
        else:reviews.append('ORCID not independently matched')
        aff=c.get('affiliation')
        if aff:
            atext=' '.join(author.get('affiliations',[]))
            if atext and norm(aff) not in norm(atext):reviews.append('Affiliation string differs; verify former institution/aliases')
            if not atext:reviews.append('Affiliation missing from record')
        roles=set(c.get('roles',[]))
        group=r.get('equal_first',None)
        corr=r.get('corresponding',None)
        if 'first_author' in roles and idx!=0:
            if group is not None and any(similar(name,x)>.88 for x in group):passes.append('Co-first author confirmed')
            else:fails.append('First author claim conflicts with author order / verified notes')
        elif 'first_author' in roles:passes.append('First listed author (not necessarily sole-first)')
        if 'sole_first_author' in roles:
            if idx!=0:fails.append('Sole-first claim conflicts with author order')
            elif group is None:reviews.append('Equal-contribution notes not provided; sole-first unverified')
            elif len(group)>1:fails.append('Sole-first false: publisher names multiple equal first contributors')
            else:passes.append('Sole-first consistent with supplied publisher notes')
        if 'co_first_author' in roles:
            if group is None:reviews.append('No publisher equal-contribution note supplied')
            elif not any(similar(name,x)>.88 for x in group):fails.append('Co-first claim not supported by supplied notes')
            else:passes.append('Co-first supported by supplied notes')
        if 'corresponding_author' in roles:
            if corr is None:reviews.append('Corresponding-author note unavailable; cannot verify claim')
            elif not any(similar(name,x)>.88 for x in corr):fails.append('Corresponding-author claim contradicts supplied publisher note')
            else:passes.append('Corresponding author supported by publisher note')
        if 'independent_pi' in roles:
            reviews.append('Independent PI leadership is NEVER established by author order/DOI; require independent contemporaneous PI/grant/lab evidence')
        unknown=roles-{'first_author','sole_first_author','co_first_author','corresponding_author','independent_pi'}
        if unknown:reviews.append('Unrecognized author roles: '+','.join(sorted(unknown)))
    if not r.get('role_source') and c.get('roles'):
        reviews.append('Publisher author/contribution note URL missing; role claims require manual original-source check')
    return {'status':('FAIL' if fails else 'REVIEW_REQUIRED' if reviews else 'PASS_METADATA'),
            'doi':cd,'checks':passes,'errors':fails,'review_required':reviews,
            'important_limit':'Supplied metadata and claimed source URLs are not proof that original sources were read.'}

def crossref_check(claim):
    """Optional network verification of bibliographic metadata only, NOT author roles."""
    identifier=doi(claim.get('doi',''))
    if not identifier:return {'status':'REVIEW_REQUIRED','reason':'DOI missing'}
    endpoint='https://api.crossref.org/works/'+quote(identifier,safe='')
    try:
        req=Request(endpoint,headers={'User-Agent':'MentorVettingSkill/5.0 (+https://github.com/agentskills/agentskills)'})
        with urlopen(req,timeout=12) as resp:data=json.load(resp)['message']
        pub=data.get('published',data.get('issued',{})).get('date-parts',[[None]])[0][0]
        record={'doi':data.get('DOI'),'title':(data.get('title') or [''])[0],
                'year':pub,'authors':[{'name':(' '.join([a.get('given',''),a.get('family','')])).strip()} for a in data.get('author',[])],
                'source':endpoint}
        claim_no_roles=dict(claim);claim_no_roles.pop('roles',None)
        check=evaluate({'claimed':claim_no_roles,'record':record})
        # Crossref does not ordinarily certify corresponding/equal-first author roles.
        return {'status':check['status'],'errors':check['errors'],
                'review_required':check['review_required'],
                'note':'Crossref metadata only; inspect publisher notes for author roles and contribution statements.',
                'url':endpoint}
    except Exception as e:
        return {'status':'REVIEW_REQUIRED','reason':f'Crossref request failed: {type(e).__name__}: {str(e)[:160]}','url':endpoint}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',help='Local JSON with items and source records')
    p.add_argument('--output',help='Optional path to machine-readable results')
    p.add_argument('--online-crossref',action='store_true',help='Optional live Crossref bibliographic check; never verifies author contribution')
    p.add_argument('--strict',action='store_true',help='Exit 2 on REVIEW_REQUIRED (default reports reviews but returns 0)')
    args=p.parse_args()
    data=json.loads(Path(args.input).read_text(encoding='utf-8'))
    items=data.get('items') if isinstance(data,dict) else data
    if not isinstance(items,list):p.error('Input must be {"items": [...]} or a JSON list')
    results=[evaluate(x) for x in items]
    if args.online_crossref:
        for item,result in zip(items,results):
            live=crossref_check(item.get('claimed',{}))
            result['crossref']=live
            if live['status']=='FAIL':
                result['status']='FAIL';result['errors'].extend(['Live Crossref: '+x for x in live.get('errors',[])])
            elif live['status']=='REVIEW_REQUIRED' and result['status']!='FAIL':
                result['status']='REVIEW_REQUIRED'
    output={'results':results,'totals':{key:sum(r['status']==key for r in results) for key in ('PASS_METADATA','REVIEW_REQUIRED','FAIL')},
            'disclaimer':'Does not verify sources online, independent PI leadership or research impact.'}
    txt=json.dumps(output,ensure_ascii=False,indent=2)
    if args.output:Path(args.output).write_text(txt+'\n',encoding='utf-8')
    print(txt)
    if any(r['status']=='FAIL' for r in results):return 1
    if args.strict and any(r['status']=='REVIEW_REQUIRED' for r in results):return 2
    return 0
if __name__=='__main__':sys.exit(main())

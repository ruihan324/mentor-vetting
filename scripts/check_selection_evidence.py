#!/usr/bin/env python3
"""Offline evidence pre-screen: checks structured *declared* proof, not source truth.

Usage: python scripts/check_selection_evidence.py file.json
Schema: {"claims": [{"id", "kind", "status", "sources": [
    {"type": "official|original_paper|primary_interview|anonymous|secondary|other",
     "url": "...", "final_finding": false}], optional fields ...}]}.
"""
import json, sys
from urllib.parse import urlparse
from pathlib import Path

KINDS={"institutional_policy","student_completion_rate","serious_misconduct","student_experience","communication_inference","funding","research_claim","other"}
VERIFIED={"Verified","Partially supported","Needs confirmation","Needs verification","Not found","Not applicable"}
PRIMARY={"official","original_paper","primary_interview"}

def review(data):
    issues=[]
    if not isinstance(data,dict) or not isinstance(data.get('claims'),list):
        return ['Root must contain claims list']
    for i,c in enumerate(data['claims']):
        if not isinstance(c,dict):
            issues.append(f'Claim {i}: must be an object');continue
        cid=c.get('id') or f'claim-{i}'
        k=c.get('kind'); status=c.get('status'); sources=c.get('sources',[])
        if k not in KINDS: issues.append(f'{cid}: unknown kind')
        if status not in VERIFIED: issues.append(f'{cid}: unknown status')
        if not isinstance(sources,list): issues.append(f'{cid}: sources must be list'); continue
        if c.get('basis_type') in ('protected_characteristic','demographic_stereotype','coded_speech_guess'):
            issues.append(f'{cid}: forbidden evidence basis')
        if status=='Verified' and not any(isinstance(s,dict) and s.get('type') in PRIMARY for s in sources):
            issues.append(f'{cid}: verified conclusion lacks direct evidence class')
        if status=='Verified':
            supporting=[s for s in sources if isinstance(s,dict) and s.get('type') in PRIMARY]
            public_records=[s for s in supporting if s.get('type')!='primary_interview']
            public_url=any(isinstance(s.get('url'),str) and urlparse(s['url']).scheme in ('https','http')
                           and urlparse(s['url']).netloc for s in public_records)
            private_firsthand=any(s.get('type')=='primary_interview' and isinstance(s.get('date'),str)
                                  and isinstance(s.get('role'),str) and s.get('role').strip() for s in supporting)
            # Interviews have no public URL; record provenance privately, never expose an interviewee.
            if not (public_url or (k=='student_experience' and private_firsthand)):
                issues.append(f'{cid}: verified conclusion lacks a specific source URL or dated firsthand account; declared evidence cannot be reviewed')
        if k=='student_completion_rate' and status=='Verified':
            n,d=c.get('completed_n'),c.get('cohort_n')
            if not isinstance(d,int) or not isinstance(n,int) or d<=0 or not 0<=n<=d:
                issues.append(f'{cid}: completion rate needs valid entry cohort and outcomes')
        if k=='institutional_policy' and c.get('scope')=='national' and status=='Verified':
            if not any(isinstance(s,dict) and s.get('type')=='official' and s.get('scope')=='national' for s in sources):
                issues.append(f'{cid}: national rule asserted without national official source')
        if k=='serious_misconduct' and status=='Verified':
            if not any(isinstance(s,dict) and s.get('type')=='official' and s.get('final_finding') is True for s in sources):
                issues.append(f'{cid}: serious finding needs final verifiable record')
        if k=='communication_inference' and status=='Verified':
            issues.append(f'{cid}: communication timing/subtext is not a verified character diagnosis')
        if k=='student_experience' and status=='Verified' and sources and all(isinstance(s,dict) and s.get('type') in ('anonymous','secondary') for s in sources):
            issues.append(f'{cid}: social-media experience alone cannot verify lab-wide condition')
    return issues

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('Usage: check_selection_evidence.py <claims.json>')
    try: data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    except (ValueError,OSError) as e: raise SystemExit(str(e))
    errors=review(data)
    print(json.dumps({'pass':not errors,'errors':errors,'claims_count':len(data.get('claims',[])) if isinstance(data,dict) and isinstance(data.get('claims'),list) else 0},indent=2))
    sys.exit(1 if errors else 0)

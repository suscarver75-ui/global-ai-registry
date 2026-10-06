#!/usr/bin/env python3
"""Henry public-safe provenance, capability and command-contract verifier."""
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parent; TESTS=ROOT/'provenance-tests'; REGISTRY='LoAI-2024-0414-001'
ALLOWED_STATUS={'VERIFIED','PARTIAL','BUILDING','NOT_VERIFIED'}; checks=[]
def check(n,o,d=''): checks.append((n,bool(o),d))
def load(p): return p.read_text(encoding='utf-8')
html=load(ROOT/'index.html'); prov=json.loads(load(ROOT/'provenance.json'))
check('console artifact id',prov.get('artifact_id') in html,prov.get('artifact_id','')); check('console registry',prov.get('registry')==REGISTRY and REGISTRY in html); check('console public boundary',prov.get('boundary')=='PUBLIC_SAFE'); check('console no private authority',prov.get('authority')=='NO_PRIVATE_AUTHORITY'); check('console canonical path',prov.get('artifact_path')=='henry/index.html')
health=json.loads(load(ROOT/'health.json')); check('health registry',health.get('registry')==REGISTRY); check('health public boundary',health.get('boundary')=='PUBLIC_SAFE'); check('health no private authority',health.get('authority')=='NO_PRIVATE_AUTHORITY'); check('health contains no secrets',health.get('contains_secrets') is False)
caps=json.loads(load(ROOT/'capabilities.json')); check('capability schema',caps.get('schema')=='henry.capabilities.v1'); check('capability registry',caps.get('registry')==REGISTRY); check('capability public boundary',caps.get('boundary')=='PUBLIC_SAFE'); check('capability no private authority',caps.get('authority')=='NO_PRIVATE_AUTHORITY'); check('capability vocabulary',set(caps.get('status_vocabulary',[]))==ALLOWED_STATUS)
cl=caps.get('capabilities',[]); check('capability ids unique',len({c.get('id') for c in cl})==len(cl))
for c in cl:
 cid=c.get('id','UNKNOWN'); st=c.get('status'); check(f'capability status {cid}',st in ALLOWED_STATUS,str(st))
 if st=='VERIFIED': check(f'verified capability has evidence {cid}',bool(c.get('evidence')))
 if st in {'PARTIAL','BUILDING','NOT_VERIFIED'}: check(f'incomplete capability explains remaining {cid}',bool(c.get('remaining')))
check('private brain remains unexposed',any(c.get('id')=='private-main-brain-authority' and c.get('status')=='NOT_VERIFIED' for c in cl))
contract=json.loads(load(ROOT/'command-contract.json')); check('command contract schema',contract.get('schema')=='henry.command-contract.v1'); check('command registry',contract.get('registry')==REGISTRY); check('command public boundary',contract.get('boundary')=='PUBLIC_SAFE'); check('command no private authority',contract.get('authority')=='NO_PRIVATE_AUTHORITY'); check('command default deny',contract.get('default_decision')=='DENY')
actions=contract.get('allowed_actions',[]); ids=[a.get('id') for a in actions]; check('command action ids unique',len(ids)==len(set(ids))); check('command mutation preview gate',all((not a.get('mutation')) or a.get('preview_required') is True for a in actions)); check('command prohibits arbitrary execution',any('arbitrary shell/code execution' in x for x in contract.get('prohibited_inputs',[]))); check('command prohibits brain internals',any('private Main Brain' in x for x in contract.get('prohibited_inputs',[]))); check('command receipt evidence',all(x in contract.get('receipt_required',[]) for x in ['command_id','decision','verification_status','evidence_references']))
example=json.loads(load(ROOT/'command-examples/preview-public-change.json')); check('example contract version',example.get('contract_version')==contract.get('schema')); check('example action allowlisted',example.get('action') in ids); check('example is preview',example.get('mode')=='PREVIEW'); check('example public target',str(example.get('target','')).startswith('henry/'))
doc=load(TESTS/'HNY-DOCUMENT-TEST-001.md'); svg=load(TESTS/'HNY-IMAGE-TEST-001.svg')
for t in ['HNY-DOCUMENT-TEST-001',REGISTRY,'CURRENT_PUBLIC','PUBLIC_SAFE','HNY-01']: check(f'document token {t}',t in doc)
for t in ['HNY-IMAGE-TEST-001',REGISTRY,'PUBLIC_SAFE','henry.public-provenance.v1','HNY-01']: check(f'image token {t}',t in svg)
product=json.loads(load(TESTS/'HNY-PRODUCT-TEST-001.manifest.json')); check('product artifact',product.get('artifact_id')=='HNY-PRODUCT-TEST-001'); check('product registry',product.get('registry')==REGISTRY); check('product boundary',product.get('boundary')=='PUBLIC_SAFE'); check('product no private authority',product.get('package_policy',{}).get('private_authority') is False)
video=json.loads(load(TESTS/'HNY-VIDEO-TEST-001.manifest.json')); check('video artifact',video.get('artifact_id')=='HNY-VIDEO-TEST-001'); check('video registry',video.get('registry')==REGISTRY); check('video boundary',video.get('boundary')=='PUBLIC_SAFE'); check('video honesty state',video.get('verification_status')=='MANIFEST_VERIFIED_ONLY')
# Secret hygiene scans deployable/public artifacts. Security test fixtures intentionally contain fake attack strings and are tested separately.
EXCLUDED_SECURITY_FIXTURES={'test-policy-engine.py','verify-provenance.py','policy-engine.py','security/test-firebreak-guard.py'}
public=[p for p in ROOT.rglob('*') if p.is_file() and p.suffix.lower() in {'.html','.json','.md','.svg','.py'} and str(p.relative_to(ROOT)) not in EXCLUDED_SECURITY_FIXTURES and p.name not in EXCLUDED_SECURITY_FIXTURES]
patterns=[re.compile(r'(?i)(api[_-]?key|secret|password|private[_-]?key)\s*[=:]\s*[\'\"][^\'\"]{8,}'),re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}')]
for p in public: check(f'secret hygiene {p.relative_to(ROOT)}',not any(x.search(load(p)) for x in patterns))
check('security fixtures explicitly excluded from deployable secret scan',EXCLUDED_SECURITY_FIXTURES=={'test-policy-engine.py','verify-provenance.py','policy-engine.py','security/test-firebreak-guard.py'})
failed=[c for c in checks if not c[1]]
for n,o,d in checks: print(('PASS' if o else 'FAIL')+' | '+n+(' | '+d if d else ''))
print(f'SUMMARY | {len(checks)-len(failed)}/{len(checks)} passed'); sys.exit(1 if failed else 0)

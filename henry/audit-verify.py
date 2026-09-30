#!/usr/bin/env python3
"""Machine checks for Henry's public-safe audit policy. Performs no mutation."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
POLICY=json.loads((ROOT/'audit-policy.json').read_text(encoding='utf-8'))
REQUIRED_CLASSES={'security_failure':365,'mutation_receipt':365,'preview_receipt':90,'health_observation':30}
REQUIRED_LINKS={'receipt_id','command_id','command_fingerprint','previous_receipt_hash','verification_status'}
REQUIRED_PROHIBITED={'credentials','access tokens','wallet secrets','private Main Brain prompts','hidden reasoning'}
def verify(policy=POLICY):
 errors=[]
 if policy.get('schema')!='henry.audit-policy.v1': errors.append('schema')
 if policy.get('boundary')!='PUBLIC_SAFE': errors.append('boundary')
 if policy.get('authority')!='NO_PRIVATE_AUTHORITY': errors.append('authority')
 classes=policy.get('retention_classes',{})
 for name,minimum in REQUIRED_CLASSES.items():
  if classes.get(name,{}).get('minimum_days',-1)<minimum: errors.append('retention:'+name)
 if not REQUIRED_LINKS.issubset(set(policy.get('required_links',[]))): errors.append('required_links')
 if not REQUIRED_PROHIBITED.issubset(set(policy.get('prohibited_content',[]))): errors.append('prohibited_content')
 principles=' '.join(policy.get('principles',[])).lower()
 if 'preserve failures as failures' not in principles: errors.append('failure_preservation')
 if 'do not rewrite history' not in principles: errors.append('append_only_intent')
 if not policy.get('deletion_rule'): errors.append('deletion_rule')
 return errors
if __name__=='__main__':
 e=verify(); print('PASS | audit retention policy verified' if not e else 'FAIL | '+','.join(e)); raise SystemExit(1 if e else 0)

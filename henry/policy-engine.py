#!/usr/bin/env python3
"""Henry public-safe command policy engine. Validation only; performs no mutations."""
from __future__ import annotations
import json, re, hashlib
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CONTRACT=json.loads((ROOT/'command-contract.json').read_text(encoding='utf-8')); ACTIONS={a['id']:a for a in CONTRACT['allowed_actions']}
SECRET_PATTERNS=[re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}'),re.compile(r'(?i)(api[_-]?key|password|private[_-]?key|seed[_-]?phrase)\s*[=:]\s*[^\s,}]{8,}')]
PRIVATE_TERMS=('private main brain','hidden reasoning','chain of thought','private prompt','wallet seed','seed phrase')
def parse_time(v):
 if not isinstance(v,str): return None
 try:return datetime.fromisoformat(v.replace('Z','+00:00'))
 except ValueError:return None
def canonical_hash(value):
 raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode(); return 'sha256:'+hashlib.sha256(raw).hexdigest()
def command_fingerprint(command):
 safe={k:command.get(k) for k in ('command_id','contract_version','issued_at','expires_at','action','mode','target','payload','expected_state','idempotency_key')}; return canonical_hash(safe)
def decide(command,now=None,preview_evidence=False,seen_commands=None,current_state=None):
 now=now or datetime.now(timezone.utc); seen_commands=seen_commands or {}
 action=command.get('action')
 if action not in ACTIONS:return 'DENY_UNKNOWN_ACTION'
 if command.get('contract_version')!=CONTRACT['schema']:return 'DENY_PRECONDITION'
 exp=parse_time(command.get('expires_at')); issued=parse_time(command.get('issued_at'))
 if not exp or not issued or exp<=now or issued>now:return 'DENY_EXPIRED'
 target=str(command.get('target',''))
 if not target.startswith('henry/') or '..' in target:return 'DENY_SCOPE'
 text=json.dumps(command.get('payload',{}),sort_keys=True); low=text.lower()
 if any(t in low for t in PRIVATE_TERMS):return 'DENY_PRIVATE_DATA'
 if any(p.search(text) for p in SECRET_PATTERNS):return 'DENY_SECRET'
 cid=command.get('command_id'); fp=command_fingerprint(command)
 if not cid:return 'DENY_PRECONDITION'
 if cid in seen_commands:
  return 'DENY_REPLAY_CONFLICT' if seen_commands[cid]!=fp else 'DENY_REPLAY_CONFLICT'
 expected=command.get('expected_state')
 if expected is not None and current_state is not None and expected!=current_state:return 'DENY_PRECONDITION'
 spec=ACTIONS[action]; mode=command.get('mode')
 if spec.get('mutation'):
  if mode!='EXECUTE':return 'ALLOW_PREVIEW' if mode=='PREVIEW' else 'DENY_PRECONDITION'
  if not command.get('idempotency_key'):return 'DENY_PRECONDITION'
  if spec.get('preview_required') and not preview_evidence:return 'DENY_MISSING_PREVIEW'
  return 'ALLOW_EXECUTE'
 return 'ALLOW_PREVIEW' if mode=='PREVIEW' else 'ALLOW_EXECUTE'
if __name__=='__main__':
 import sys; data=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')); print(decide(data))

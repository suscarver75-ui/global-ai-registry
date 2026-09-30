#!/usr/bin/env python3
"""Tamper-evident receipt primitives. SHA-256 proves consistency/integrity only, not signer identity."""
import hashlib,json
GENESIS='GENESIS'
def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(value): return 'sha256:'+hashlib.sha256(canonical(value).encode()).hexdigest()
def command_fingerprint(command):
 keys=('command_id','contract_version','issued_at','expires_at','action','mode','target','payload','expected_state','idempotency_key')
 return digest({k:command.get(k) for k in keys})
def seal(receipt,previous_hash=GENESIS,command=None):
 body=dict(receipt); body.pop('receipt_hash',None); body['previous_receipt_hash']=previous_hash
 if command is not None:
  if body.get('command_id')!=command.get('command_id'): raise ValueError('receipt command_id does not match command')
  body['command_fingerprint']=command_fingerprint(command)
 body['receipt_hash']=digest(body); return body
def verify(receipt,expected_previous=GENESIS,command=None):
 body=dict(receipt); claimed=body.pop('receipt_hash',None); previous=body.get('previous_receipt_hash')
 if previous!=expected_previous or claimed!=digest(body): return False
 if command is not None:
  return body.get('command_id')==command.get('command_id') and body.get('command_fingerprint')==command_fingerprint(command)
 return True
def verify_chain(receipts):
 previous=GENESIS
 for r in receipts:
  if not verify(r,previous): return False
  previous=r['receipt_hash']
 return True

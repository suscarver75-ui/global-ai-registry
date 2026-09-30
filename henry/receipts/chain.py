#!/usr/bin/env python3
"""Tamper-evident receipt-chain primitives. Hashing provides integrity evidence, not identity/authentication."""
import hashlib,json
GENESIS='GENESIS'
def canonical(value): return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(value): return 'sha256:'+hashlib.sha256(canonical(value).encode()).hexdigest()
def seal(receipt,previous_hash=GENESIS):
 body=dict(receipt); body.pop('receipt_hash',None); body['previous_receipt_hash']=previous_hash; body['receipt_hash']=digest(body); return body
def verify(receipt,expected_previous=GENESIS):
 body=dict(receipt); claimed=body.pop('receipt_hash',None); previous=body.get('previous_receipt_hash'); return previous==expected_previous and claimed==digest(body)
def verify_chain(receipts):
 previous=GENESIS
 for r in receipts:
  if not verify(r,previous): return False
  previous=r['receipt_hash']
 return True

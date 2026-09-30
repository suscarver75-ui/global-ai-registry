#!/usr/bin/env python3
from pathlib import Path
import importlib.util
P=Path(__file__).resolve().parent/'confidence-gate.py';s=importlib.util.spec_from_file_location('g',P);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def e(**x):
 d={'verification_state':'VERIFIED','recency_band':'CURRENT','sample_size_band':'STRONG','source_independence_band':'MULTI_SOURCE_INDEPENDENT','contradiction_state':'NONE','evidence_class':'VERIFIED_RESULT','decay_state':'ACTIVE'};d.update(x);return d
cases=[
 ('two strong proofs',g.gate([e(),e()])['state'],'STRONG_PUBLIC_PROOF'),
 ('one verified proof limited',g.gate([e()])['state'],'LIMITED_PUBLIC_PROOF'),
 ('conflict requires review',g.gate([e(),e(contradiction_state='MATERIAL_CONFLICT')])['state'],'CONFLICT_REVIEW'),
 ('stale evidence insufficient',g.gate([e(recency_band='STALE')])['state'],'INSUFFICIENT_EVIDENCE'),
 ('expired evidence insufficient',g.gate([e(decay_state='EXPIRED')])['state'],'INSUFFICIENT_EVIDENCE'),
 ('unverified insufficient',g.gate([e(verification_state='UNVERIFIED')])['state'],'INSUFFICIENT_EVIDENCE'),
 ('empty fails closed',g.gate([])['state'],'HOLD'),
 ('incomplete fails closed',g.gate([{'verification_state':'VERIFIED'}])['state'],'HOLD'),
 ('no execution authority',g.gate([e()])['execution_authority'],False),
 ('private weights hidden',g.gate([e()])['private_weighting_exposed'],False)]
f=0
for n,a,b in cases:
 ok=a==b;f+=not ok;print(('PASS' if ok else 'FAIL')+f' | {n} | expected={b} got={a}')
print(f'SUMMARY | {len(cases)-f}/{len(cases)} passed');raise SystemExit(1 if f else 0)

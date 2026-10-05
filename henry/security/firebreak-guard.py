#!/usr/bin/env python3
"""Henry public-repository firebreak guard. Fail closed.
This guard inspects metadata/content intended for GitHub handoff. It never requests
or needs Mac Henry private Brain content.
"""
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
POLICY=json.loads((ROOT/'private-brain-firebreak.json').read_text(encoding='utf-8'))

PATTERNS={
 'PRIVATE_KEY':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'GITHUB_TOKEN':r'\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b',
 'OPENAI_STYLE_KEY':r'\bsk-[A-Za-z0-9_-]{20,}\b',
 'AWS_ACCESS_KEY':r'\bAKIA[0-9A-Z]{16}\b',
 'SEED_PHRASE_LABEL':r'(?i)\b(seed phrase|recovery phrase|wallet private key)\b\s*[:=]',
 'PASSWORD_LABEL':r'(?i)\b(password|passwd)\b\s*[:=]\s*\S+',
 'BEARER_TOKEN':r'(?i)\bauthorization\s*:\s*bearer\s+\S+',
 'PRIVATE_BRAIN_LABEL':r'(?i)\b(mac henry private brain|private brain export|private memory export)\b\s*[:=]'
}

def inspect_text(text:str)->dict:
 hits=[]
 for name,pat in PATTERNS.items():
  if re.search(pat,text): hits.append(name)
 decision='DENY' if hits else 'ALLOW_SANITIZED_HANDOFF'
 return {'schema':'henry.firebreak-result.v2','decision':decision,'findings':hits,'safe_to_publish':not hits}

def main()->int:
 if len(sys.argv)!=2:
  print(json.dumps({'decision':'DENY','error':'USAGE'})); return 2
 p=Path(sys.argv[1])
 try:
  if p.stat().st_size>2_000_000:
   print(json.dumps({'decision':'DENY','error':'INPUT_TOO_LARGE'})); return 1
  result=inspect_text(p.read_text(encoding='utf-8',errors='strict'))
 except Exception as exc:
  result={'schema':'henry.firebreak-result.v2','decision':'DENY','safe_to_publish':False,'error':'FAIL_CLOSED:'+type(exc).__name__}
 print(json.dumps(result,indent=2))
 return 0 if result.get('safe_to_publish') else 1
if __name__=='__main__': raise SystemExit(main())

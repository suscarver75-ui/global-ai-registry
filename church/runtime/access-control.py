#!/usr/bin/env python3
"""Executable Seven-Fold Church authorization kernel.
Developer-safe, dependency-free, default-deny. No private Mac Henry Brain data.
"""
from __future__ import annotations
import json,sys
from dataclasses import dataclass
from pathlib import Path

ZONES={'PUBLIC','MEMBER','MINISTER_STUDENT','CREDENTIALED_LEADER','ADMIN','HENRY','MAC_HENRY_OWNER'}
SENSITIVE={'membership','messages','training-records','assessments','credentials','good-standing','charters','moderation','consent','payments','audit-evidence'}
ROLE_ALLOW={
 'PUBLIC':{'public'},
 'MEMBER':{'public','membership'},
 'MINISTER_STUDENT':{'public','membership','training-records','assessments'},
 'CREDENTIALED_LEADER':{'public','membership','training-records','assessments','credentials','good-standing'},
 'ADMIN':{'public','membership','training-records','assessments','credentials','good-standing','charters','moderation','consent','audit-evidence'},
 'HENRY':{'public','training-records','credentials','good-standing','charters','moderation','audit-evidence'},
 'MAC_HENRY_OWNER':{'public','membership','messages','training-records','assessments','credentials','good-standing','charters','moderation','consent','payments','audit-evidence'}
}
STEP_UP_ACTIONS={'ISSUE_CREDENTIAL','REVOKE_CREDENTIAL','CHANGE_ROLE','EXPORT_PRIVATE_DATA','DELETE_PRIVATE_DATA','PAYMENT_ADMIN','CHARTER_APPROVE'}
HUMAN_ONLY={'ISSUE_CREDENTIAL','REVOKE_CREDENTIAL','CHANGE_ROLE','DELETE_PRIVATE_DATA','PAYMENT_ADMIN','CHARTER_APPROVE'}

@dataclass(frozen=True)
class Decision:
 decision:str; reason:str; zone:str; domain:str; action:str
 def as_dict(self): return {'schema':'seven-fold-church.authz-result.v1',**self.__dict__}

def authorize(req:dict)->Decision:
 try:
  zone=req['zone']; domain=req['domain']; action=req['action']
  authenticated=bool(req.get('authenticated')); step_up=bool(req.get('step_up'))
  human_actor=bool(req.get('human_actor')); owner_approved=bool(req.get('owner_approved'))
 except Exception:
  return Decision('DENY','MALFORMED_REQUEST','UNKNOWN','UNKNOWN','UNKNOWN')
 if zone not in ZONES: return Decision('DENY','UNKNOWN_ZONE',str(zone),str(domain),str(action))
 if domain!='public' and not authenticated: return Decision('DENY','AUTHENTICATION_REQUIRED',zone,domain,action)
 if domain not in ROLE_ALLOW[zone]: return Decision('DENY','DOMAIN_NOT_AUTHORIZED',zone,domain,action)
 if action in STEP_UP_ACTIONS and not step_up: return Decision('DENY','STEP_UP_REQUIRED',zone,domain,action)
 if action in HUMAN_ONLY and not human_actor: return Decision('DENY','HUMAN_AUTHORITY_REQUIRED',zone,domain,action)
 if zone=='HENRY' and action in HUMAN_ONLY: return Decision('DENY','HENRY_CANNOT_EXERCISE_HUMAN_AUTHORITY',zone,domain,action)
 if action in {'CHANGE_ROLE','DELETE_PRIVATE_DATA','PAYMENT_ADMIN'} and not owner_approved:
  return Decision('DENY','OWNER_APPROVAL_REQUIRED',zone,domain,action)
 return Decision('ALLOW','POLICY_ALLOW',zone,domain,action)

def main()->int:
 if len(sys.argv)!=2:
  print(json.dumps(Decision('DENY','USAGE','UNKNOWN','UNKNOWN','UNKNOWN').as_dict())); return 2
 try: req=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
 except Exception:
  print(json.dumps(Decision('DENY','INVALID_INPUT','UNKNOWN','UNKNOWN','UNKNOWN').as_dict())); return 1
 d=authorize(req); print(json.dumps(d.as_dict(),indent=2)); return 0 if d.decision=='ALLOW' else 1
if __name__=='__main__': raise SystemExit(main())

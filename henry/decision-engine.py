#!/usr/bin/env python3
"""Mac Henry business decision engine.
Scores management options across value, cost, risk, evidence and reversibility.
Advisory only: never executes an option or changes authority.
"""
import json, sys
ACTIONS={'KEEP','CHANGE','STOP','SELL','DONATE','TEST','HOLD'}
RISK={'LOW':0,'MEDIUM':20,'HIGH':45,'CRITICAL':80}

def evaluate(option):
 required={'name','action','works_score','earn_score','save_score','cost_score','risk','evidence_score','reversibility_score'}
 missing=required-set(option)
 if missing:return {'valid':False,'name':option.get('name','UNKNOWN'),'decision':'HOLD','reason':'MISSING:'+','.join(sorted(missing))}
 if option['action'] not in ACTIONS:return {'valid':False,'name':option['name'],'decision':'HOLD','reason':'INVALID_ACTION'}
 nums=['works_score','earn_score','save_score','cost_score','evidence_score','reversibility_score']
 if any(not isinstance(option.get(k),(int,float)) or not 0<=option[k]<=100 for k in nums):return {'valid':False,'name':option['name'],'decision':'HOLD','reason':'INVALID_SCORE'}
 if option['risk'] not in RISK:return {'valid':False,'name':option['name'],'decision':'HOLD','reason':'INVALID_RISK'}
 value=.30*option['works_score']+.22*option['earn_score']+.13*option['save_score']+.15*option['evidence_score']+.10*option['reversibility_score']-.10*option['cost_score']-RISK[option['risk']]
 if option['risk']=='CRITICAL': decision='HOLD'
 elif option['evidence_score']<35: decision='TEST'
 elif value>=55: decision=option['action']
 elif value>=35: decision='TEST'
 else: decision='STOP' if option['action'] not in {'DONATE','SELL'} else option['action']
 return {'valid':True,'name':option['name'],'requested_action':option['action'],'decision':decision,'score':round(value,2),'risk':option['risk'],'approval_required':decision in {'SELL','DONATE'} or option['risk'] in {'HIGH','CRITICAL'}}

def decide(options):
 if not isinstance(options,list) or not options:return {'schema':'mac-henry.decision-engine.v1','status':'HOLD','reason':'NO_OPTIONS'}
 results=[evaluate(o) for o in options]
 if any(not r['valid'] for r in results):return {'schema':'mac-henry.decision-engine.v1','status':'HOLD','reason':'INVALID_OPTION','results':results}
 eligible=[r for r in results if r['decision']!='HOLD']
 if not eligible:return {'schema':'mac-henry.decision-engine.v1','status':'HOLD','reason':'ALL_OPTIONS_HELD','results':results}
 best=max(eligible,key=lambda r:r['score'])
 return {'schema':'mac-henry.decision-engine.v1','status':'RECOMMENDATION','next_best_move':best,'results':sorted(results,key=lambda r:r.get('score',-999),reverse=True),'execution_authority':False}

if __name__=='__main__':
 try:data=json.load(sys.stdin)
 except Exception: print(json.dumps({'schema':'mac-henry.decision-engine.v1','status':'HOLD','reason':'INVALID_JSON'})); raise SystemExit(1)
 out=decide(data); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='RECOMMENDATION' else 1)

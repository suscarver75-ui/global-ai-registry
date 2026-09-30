#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'opportunity-funnel-public-contract.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.opportunity-funnel-public-contract.v1':e.append('schema')
stages={'DISCOVER','QUALIFY','ECONOMICS','TEST_DESIGN','VALIDATE','SCALE_REVIEW','COMPOUND_REVIEW','RETIRE_OR_RECYCLE'}
if set(p.get('stages',[]))!=stages:e.append('stages')
needed={'demand_evidence','time_to_first_cash','gross_margin','cash_requirement','owner_attention','delivery_capacity','repeatability','retention','distribution_access','competitive_differentiation','legal_compliance','security_privacy','downside_limit','reversibility','opportunity_cost','asset_compounding_value'}
if set(p.get('required_filters',[]))!=needed:e.append('filters')
a=p.get('public_authority',{})
for k in ('launch_paid_test','spend_funds','sign_contracts','contact_customers','publish_offer','change_private_rankings','request_private_financial_context'):
 if a.get(k) is not False:e.append('authority:'+k)
pro=set(p.get('prohibited_public_fields',[]))
for k in ('private_opportunity_rankings','private_financial_context','private_customer_data','private_growth_weights','private_strategy','credentials','tokens','private_keys','seed_phrases','hidden_reasoning'):
 if k not in pro:e.append('prohibited:'+k)
r=' '.join(p.get('experiment_rules',[])).lower()
for phrase in ('smallest ethical test','success, stop and review thresholds','vanity metrics','disproportionate cash or owner attention','capacity, downside, dependency and owner-review gates','for compounding','preserve useful evidence','never receives private opportunity rankings','never grants spending'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | opportunity funnel favors evidence-led income discovery, bounded testing and compounding' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)

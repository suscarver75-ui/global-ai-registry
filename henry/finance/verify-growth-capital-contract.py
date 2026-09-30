#!/usr/bin/env python3
import json
from pathlib import Path
p=json.loads((Path(__file__).resolve().parent/'growth-capital-public-contract.json').read_text(encoding='utf-8'))
e=[]
if p.get('schema')!='henry.growth-capital-public-contract.v1':e.append('schema')
req={'revenue_potential','recurring_revenue_potential','gross_margin_band','cash_conversion_speed','customer_acquisition_efficiency','retention_potential','pricing_power','cross_sell_potential','asset_creation_potential','automation_leverage','time_requirement','capital_requirement','opportunity_cost','downside_band','reversibility','evidence_quality'}
if set(p.get('required_growth_dimensions',[]))!=req:e.append('dimensions')
outs={'GROWTH_CANDIDATE','TEST_FIRST','PROTECT_CASH','IMPROVE_MARGIN','IMPROVE_RETENTION','REPRICE_REVIEW','CAPACITY_CONSTRAINED','OWNER_REVIEW_REQUIRED','HOLD'}
if set(p.get('public_safe_outputs',[]))!=outs:e.append('outputs')
a=p.get('public_authority',{})
for k in ('spend_funds','move_funds','trade_assets','invest_assets','sign_contracts','change_private_growth_weights','request_private_financial_context'):
 if a.get(k) is not False:e.append('authority:'+k)
pro=set(p.get('prohibited_public_fields',[]))
for k in ('private_account_balances','private_bank_data','private_wallet_data','private_portfolio_positions','private_growth_weights','private_financial_strategy','private_business_context','credentials','tokens','private_keys','seed_phrases','hidden_reasoning'):
 if k not in pro:e.append('prohibited:'+k)
r=' '.join(p.get('capital_rules',[])).lower()
for phrase in ('margin, cash timing, risk and opportunity cost','recurring and repeatable income','destroys margin or liquidity','compounding advantages','scarce resources','human review and authorization','guaranteed profit','cannot access private balances','never grants spending'):
 if phrase not in r:e.append('rule:'+phrase)
print('PASS | growth governance favors durable income and wealth while preserving financial controls' if not e else 'FAIL | '+','.join(e))
raise SystemExit(1 if e else 0)

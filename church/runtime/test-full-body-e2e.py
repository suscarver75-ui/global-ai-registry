#!/usr/bin/env python3
"""Full-body Church runtime integration proof across authoritative reference components."""
import importlib.util,sys
from pathlib import Path
D=Path(__file__).resolve().parent
def load(name,file):
 s=importlib.util.spec_from_file_location(name,D/file);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
identity=load('identity', 'identity-runtime.py'); protected=load('protected','protected-data.py'); training=load('training','training-runtime.py'); credential=load('credential','credential-runtime.py'); community=load('community','community-safety.py'); charter=load('charter','charter-runtime.py'); payment=load('payment','payment-boundary.py'); ops=load('ops','operations-recovery.py')
# Interface-level full body checks deliberately consume existing component APIs rather than reimplement them.
ids=identity.IdentityStore(); ids.create_identity('member1','MEMBER'); tok=ids.issue_session('member1',1000); ctx=ids.authz_request(tok,1001); assert ctx['authenticated']
data=protected.ProtectedStore(); assert data.put_profile(ctx,'member1','Member One',{},1002)
ts=training.TrainingStore(); student=dict(ctx); student['zone']='MINISTER_STUDENT'; assert ts.enroll(student,'program1',1003); assert ts.complete_lesson(student,'program1','L1',1004); assert ts.submit_assessment(student,'program1','A1',95,1005)
admin={'authenticated':True,'subject_id':'admin1','zone':'ADMIN','human_actor':True,'step_up':True,'issuer_authorized':True,'owner_approved':True}
assert ts.approve_assessment(admin,'member1','program1','A1',90,1006); assert ts.training_complete('member1','program1',{'L1'},{'A1'})
cs=credential.CredentialStore(); cid=cs.issue(admin,'member1','MINISTER',True,2000,1007); assert cid and cs.public_verify(cid,1008)['valid']
assert cs.set_good_standing(admin,'member1','GOOD',1009)
safe=community.CommunitySafety(); rid=safe.report(student,'post:1','HARASSMENT',1010); assert rid and safe.resolve(admin,rid,'WARNING',1011)
chs=charter.CharterStore(); chid=chs.apply(student,'Integration Fellowship',1012); assert chid and chs.decide(admin,chid,'APPROVED',1013)
pay=payment.payment_receipt({'payment_ref':'p1','purpose':'DONATION','amount_minor':100,'currency':'USD','status':'SETTLED'}); assert pay['authority_granted'] is False
checks=[ops.Check(n,True,'e2e:'+n) for n in ops.REQUIRED]; assert ops.assess(checks)['promotion_allowed']
print('CHURCH FULL BODY E2E PASS')

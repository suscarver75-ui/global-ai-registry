#!/usr/bin/env python3
"""Authoritative Training -> Credential bridge. No caller-supplied training boolean."""
import hashlib,json
class TrainingEvidence:
 def __init__(self,training_store): self.training=training_store
 def completion(self,subject,program,required_lessons,required_assessments):
  complete=self.training.training_complete(subject,program,required_lessons,required_assessments)
  body={'subject_id':subject,'program_id':program,'required_lessons':sorted(required_lessons),'required_assessments':sorted(required_assessments),'complete':bool(complete)}
  body['evidence_hash']=hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  return body
class ChurchCredentialBridge:
 def __init__(self,training_store,credential_store):self.evidence=TrainingEvidence(training_store);self.credentials=credential_store
 def issue_after_training(self,ctx,subject,program,required_lessons,required_assessments,credential_type,expires_at,now=None):
  ev=self.evidence.completion(subject,program,required_lessons,required_assessments)
  if not ev['complete']:return {'issued':False,'reason':'TRAINING_INCOMPLETE','training_evidence':ev}
  cid=self.credentials.issue(ctx,subject,credential_type,True,expires_at,now)
  return {'issued':bool(cid),'credential_id':cid,'reason':'ISSUED' if cid else 'ISSUER_DENIED','training_evidence':ev}

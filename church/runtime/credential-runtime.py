#!/usr/bin/env python3
"""Seven-Fold Church credential + Good Standing lifecycle reference runtime."""
import sqlite3,time,uuid
ACTIVE={'ACTIVE','SUSPENDED','REVOKED','EXPIRED'}
class CredentialStore:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
  self.db.executescript("""CREATE TABLE IF NOT EXISTS credentials(credential_id TEXT PRIMARY KEY,subject_id TEXT NOT NULL,credential_type TEXT NOT NULL,status TEXT NOT NULL,issued_at INTEGER NOT NULL,expires_at INTEGER NOT NULL,issuer_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS standing(subject_id TEXT PRIMARY KEY,status TEXT NOT NULL,reviewed_at INTEGER NOT NULL,reviewer_id TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,event TEXT NOT NULL,credential_id TEXT,subject_id TEXT NOT NULL,actor_id TEXT NOT NULL,created_at INTEGER NOT NULL);""");self.db.commit()
 def _issuer(self,c):
  return bool(c and c.get('authenticated') and c.get('human_actor') and c.get('step_up') and c.get('issuer_authorized') and c.get('zone') in {'ADMIN','MAC_HENRY_OWNER'})
 def issue(self,c,subject,ctype,training_verified,expires_at,now=None):
  now=int(time.time() if now is None else now)
  if not self._issuer(c) or not training_verified or expires_at<=now:return None
  cid='SFC-'+uuid.uuid4().hex[:16].upper()
  self.db.execute("INSERT INTO credentials VALUES(?,?,?,'ACTIVE',?,?,?)",(cid,subject,ctype,now,expires_at,c['subject_id']))
  self.db.execute("INSERT INTO events(event,credential_id,subject_id,actor_id,created_at) VALUES('ISSUED',?,?,?,?)",(cid,subject,c['subject_id'],now));self.db.commit();return cid
 def set_status(self,c,cid,status,now=None):
  if not self._issuer(c) or status not in {'ACTIVE','SUSPENDED','REVOKED'}:return False
  r=self.db.execute("SELECT subject_id FROM credentials WHERE credential_id=?",(cid,)).fetchone()
  if not r:return False
  now=int(time.time() if now is None else now);self.db.execute("UPDATE credentials SET status=? WHERE credential_id=?",(status,cid));self.db.execute("INSERT INTO events(event,credential_id,subject_id,actor_id,created_at) VALUES(?,?,?,?,?)",(status,cid,r['subject_id'],c['subject_id'],now));self.db.commit();return True
 def set_good_standing(self,c,subject,status,now=None):
  if not self._issuer(c) or status not in {'GOOD','REVIEW','NOT_GOOD'}:return False
  now=int(time.time() if now is None else now);self.db.execute("INSERT INTO standing VALUES(?,?,?,?) ON CONFLICT(subject_id) DO UPDATE SET status=excluded.status,reviewed_at=excluded.reviewed_at,reviewer_id=excluded.reviewer_id",(subject,status,now,c['subject_id']));self.db.commit();return True
 def public_verify(self,cid,now=None):
  now=int(time.time() if now is None else now);r=self.db.execute("SELECT credential_id,credential_type,status,expires_at FROM credentials WHERE credential_id=?",(cid,)).fetchone()
  if not r:return {'valid':False,'reason':'NOT_FOUND'}
  status='EXPIRED' if r['expires_at']<=now else r['status']
  return {'credential_id':r['credential_id'],'credential_type':r['credential_type'],'status':status,'valid':status=='ACTIVE'}

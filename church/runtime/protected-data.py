#!/usr/bin/env python3
"""Seven-Fold Church protected member datastore reference runtime.
Developer-safe SQLite integration. No production PII/secrets. Server-side ownership checks.
"""
import sqlite3,json,hashlib,time
SCHEMA_VERSION=1
class ProtectedStore:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path); self.db.row_factory=sqlite3.Row; self.migrate()
 def migrate(self):
  self.db.executescript("""CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY,v TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS profiles(subject_id TEXT PRIMARY KEY, display_name TEXT NOT NULL DEFAULT '', preferences TEXT NOT NULL DEFAULT '{}', updated_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS consents(subject_id TEXT NOT NULL, policy_version TEXT NOT NULL, granted INTEGER NOT NULL, recorded_at INTEGER NOT NULL, PRIMARY KEY(subject_id,policy_version));
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT,event TEXT NOT NULL,actor_id TEXT NOT NULL,resource_owner_id TEXT NOT NULL,receipt_hash TEXT NOT NULL,created_at INTEGER NOT NULL);""")
  self.db.execute("INSERT OR REPLACE INTO meta(k,v) VALUES('schema_version',?)",(str(SCHEMA_VERSION),)); self.db.commit()
 def _allowed(self,ctx,owner,write=False):
  if not ctx or not ctx.get('authenticated'): return False
  actor=ctx.get('subject_id'); zone=ctx.get('zone')
  if actor==owner:return True
  if zone in {'ADMIN','MAC_HENRY_OWNER'} and ctx.get('human_actor') is True:return True
  return False
 def _audit(self,event,actor,owner,now):
  payload=f"{event}|{actor}|{owner}|{now}".encode(); h=hashlib.sha256(payload).hexdigest()
  self.db.execute("INSERT INTO audit(event,actor_id,resource_owner_id,receipt_hash,created_at) VALUES(?,?,?,?,?)",(event,actor,owner,h,now))
 def put_profile(self,ctx,owner,display_name,preferences=None,now=None):
  if not self._allowed(ctx,owner,True):return False
  now=int(time.time() if now is None else now); prefs=json.dumps(preferences or {},sort_keys=True)
  self.db.execute("INSERT INTO profiles VALUES(?,?,?,?) ON CONFLICT(subject_id) DO UPDATE SET display_name=excluded.display_name,preferences=excluded.preferences,updated_at=excluded.updated_at",(owner,display_name,prefs,now)); self._audit('PROFILE_WRITE',ctx['subject_id'],owner,now); self.db.commit(); return True
 def get_profile(self,ctx,owner):
  if not self._allowed(ctx,owner):return None
  r=self.db.execute("SELECT subject_id,display_name,preferences,updated_at FROM profiles WHERE subject_id=?",(owner,)).fetchone()
  return None if not r else {'subject_id':r['subject_id'],'display_name':r['display_name'],'preferences':json.loads(r['preferences']),'updated_at':r['updated_at']}
 def record_consent(self,ctx,owner,policy_version,granted,now=None):
  if ctx.get('subject_id')!=owner or not ctx.get('authenticated'):return False
  now=int(time.time() if now is None else now)
  self.db.execute("INSERT OR REPLACE INTO consents VALUES(?,?,?,?)",(owner,policy_version,1 if granted else 0,now)); self._audit('CONSENT_RECORDED',owner,owner,now); self.db.commit(); return True
 def export_subject(self,ctx,owner):
  if not self._allowed(ctx,owner):return None
  return {'profile':self.get_profile(ctx,owner),'consents':[dict(x) for x in self.db.execute("SELECT policy_version,granted,recorded_at FROM consents WHERE subject_id=?",(owner,))]}
 def delete_subject_data(self,ctx,owner):
  if not (ctx.get('zone')=='MAC_HENRY_OWNER' and ctx.get('owner_approved') and ctx.get('step_up')):return False
  self.db.execute("DELETE FROM profiles WHERE subject_id=?",(owner,)); self.db.execute("DELETE FROM consents WHERE subject_id=?",(owner,)); self._audit('SUBJECT_DATA_DELETED',ctx['subject_id'],owner,int(time.time())); self.db.commit(); return True
 def backup_to(self,path):
  dst=sqlite3.connect(path); self.db.backup(dst); dst.close()
 def integrity_ok(self): return self.db.execute("PRAGMA integrity_check").fetchone()[0]=='ok'

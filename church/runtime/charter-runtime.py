#!/usr/bin/env python3
"""Seven-Fold Church charter administration reference runtime."""
import sqlite3,time,uuid
class CharterStore:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
  self.db.executescript("""CREATE TABLE IF NOT EXISTS charters(charter_id TEXT PRIMARY KEY,applicant_id TEXT NOT NULL,name TEXT NOT NULL,status TEXT NOT NULL,created_at INTEGER NOT NULL,approved_by TEXT);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,event TEXT NOT NULL,charter_id TEXT NOT NULL,actor_id TEXT NOT NULL,created_at INTEGER NOT NULL);""");self.db.commit()
 def _auth(self,c):return bool(c and c.get('authenticated') and c.get('subject_id'))
 def _approver(self,c):return bool(self._auth(c) and c.get('human_actor') and c.get('step_up') and c.get('owner_approved') and c.get('zone') in {'ADMIN','MAC_HENRY_OWNER'})
 def apply(self,c,name,now=None):
  if not self._auth(c) or not name.strip():return None
  now=int(time.time() if now is None else now);cid='CH-'+uuid.uuid4().hex[:12].upper()
  self.db.execute("INSERT INTO charters VALUES(?,?,?,'PENDING',?,NULL)",(cid,c['subject_id'],name.strip(),now));self.db.commit();return cid
 def decide(self,c,cid,decision,now=None):
  if not self._approver(c) or decision not in {'APPROVED','DENIED','SUSPENDED','REVOKED'}:return False
  r=self.db.execute("SELECT status FROM charters WHERE charter_id=?",(cid,)).fetchone()
  if not r:return False
  allowed={'PENDING':{'APPROVED','DENIED'},'APPROVED':{'SUSPENDED','REVOKED'},'SUSPENDED':{'APPROVED','REVOKED'}}
  if decision not in allowed.get(r['status'],set()):return False
  now=int(time.time() if now is None else now);self.db.execute("UPDATE charters SET status=?,approved_by=? WHERE charter_id=?",(decision,c['subject_id'] if decision=='APPROVED' else None,cid));self.db.execute("INSERT INTO events(event,charter_id,actor_id,created_at) VALUES(?,?,?,?)",(decision,cid,c['subject_id'],now));self.db.commit();return True
 def public_verify(self,cid):
  r=self.db.execute("SELECT charter_id,name,status FROM charters WHERE charter_id=?",(cid,)).fetchone();return None if not r else dict(r)

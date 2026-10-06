#!/usr/bin/env python3
"""Seven-Fold Church community moderation/safeguarding reference runtime."""
import sqlite3,time,uuid
class CommunitySafety:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
  self.db.executescript("""CREATE TABLE IF NOT EXISTS reports(report_id TEXT PRIMARY KEY,reporter_id TEXT NOT NULL,target_ref TEXT NOT NULL,category TEXT NOT NULL,status TEXT NOT NULL,created_at INTEGER NOT NULL,resolution TEXT);
CREATE TABLE IF NOT EXISTS appeals(appeal_id TEXT PRIMARY KEY,report_id TEXT NOT NULL,appellant_id TEXT NOT NULL,status TEXT NOT NULL,created_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,event TEXT NOT NULL,actor_id TEXT NOT NULL,ref TEXT NOT NULL,created_at INTEGER NOT NULL);""");self.db.commit()
 def _auth(self,c):return bool(c and c.get('authenticated') and c.get('subject_id'))
 def _moderator(self,c):return bool(self._auth(c) and c.get('human_actor') and c.get('zone') in {'ADMIN','MAC_HENRY_OWNER'})
 def report(self,c,target,category,now=None):
  if not self._auth(c) or category not in {'HARASSMENT','THREAT','SPAM','PRIVACY','OTHER'}:return None
  now=int(time.time() if now is None else now);rid='R-'+uuid.uuid4().hex[:12]
  self.db.execute("INSERT INTO reports VALUES(?,?,?,?, 'OPEN',?,NULL)",(rid,c['subject_id'],target,category,now));self.db.commit();return rid
 def resolve(self,c,rid,resolution,now=None):
  if not self._moderator(c) or resolution not in {'NO_ACTION','WARNING','CONTENT_REMOVED','ACCOUNT_RESTRICTED','ESCALATED'}:return False
  r=self.db.execute("SELECT 1 FROM reports WHERE report_id=?",(rid,)).fetchone()
  if not r:return False
  self.db.execute("UPDATE reports SET status='RESOLVED',resolution=? WHERE report_id=?",(resolution,rid));self.db.commit();return True
 def appeal(self,c,rid,now=None):
  if not self._auth(c):return None
  r=self.db.execute("SELECT reporter_id,status FROM reports WHERE report_id=?",(rid,)).fetchone()
  if not r or r['status']!='RESOLVED':return None
  now=int(time.time() if now is None else now);aid='A-'+uuid.uuid4().hex[:12]
  self.db.execute("INSERT INTO appeals VALUES(?,?,?,'OPEN',?)",(aid,rid,c['subject_id'],now));self.db.commit();return aid
 def public_status(self,rid):
  r=self.db.execute("SELECT report_id,status FROM reports WHERE report_id=?",(rid,)).fetchone();return None if not r else dict(r)

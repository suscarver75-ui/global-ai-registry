#!/usr/bin/env python3
"""Seven-Fold Church minister/training state machine. Developer-safe reference runtime."""
import sqlite3,time,hashlib
class TrainingStore:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path); self.db.row_factory=sqlite3.Row
  self.db.executescript("""CREATE TABLE IF NOT EXISTS enrollment(subject_id TEXT,program_id TEXT,status TEXT,PRIMARY KEY(subject_id,program_id));
CREATE TABLE IF NOT EXISTS progress(subject_id TEXT,program_id TEXT,lesson_id TEXT,completed INTEGER,PRIMARY KEY(subject_id,program_id,lesson_id));
CREATE TABLE IF NOT EXISTS assessment(subject_id TEXT,program_id TEXT,assessment_id TEXT,score REAL,status TEXT,reviewer_id TEXT,PRIMARY KEY(subject_id,program_id,assessment_id));
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,event TEXT,subject_id TEXT,actor_id TEXT,created_at INTEGER);""");self.db.commit()
 def _own(self,c,s):return bool(c and c.get('authenticated') and c.get('subject_id')==s)
 def _reviewer(self,c):return bool(c and c.get('authenticated') and c.get('human_actor') and c.get('zone') in {'ADMIN','MAC_HENRY_OWNER'})
 def enroll(self,c,s,p):
  if not self._own(c,s):return False
  self.db.execute("INSERT OR IGNORE INTO enrollment VALUES(?,?,'ENROLLED')",(s,p));self.db.commit();return True
 def complete_lesson(self,c,s,p,l):
  if not self._own(c,s):return False
  if not self.db.execute("SELECT 1 FROM enrollment WHERE subject_id=? AND program_id=?",(s,p)).fetchone():return False
  self.db.execute("INSERT OR REPLACE INTO progress VALUES(?,?,?,1)",(s,p,l));self.db.commit();return True
 def submit_assessment(self,c,s,p,a,score):
  if not self._own(c,s) or not 0<=score<=100:return False
  self.db.execute("INSERT OR REPLACE INTO assessment VALUES(?,?,?,?,?,NULL)",(s,p,a,score,'SUBMITTED'));self.db.commit();return True
 def approve_assessment(self,c,s,p,a,required_score=80):
  if not self._reviewer(c):return False
  r=self.db.execute("SELECT score,status FROM assessment WHERE subject_id=? AND program_id=? AND assessment_id=?",(s,p,a)).fetchone()
  if not r or r['status']!='SUBMITTED' or r['score']<required_score:return False
  self.db.execute("UPDATE assessment SET status='APPROVED',reviewer_id=? WHERE subject_id=? AND program_id=? AND assessment_id=?",(c['subject_id'],s,p,a));self.db.commit();return True
 def training_complete(self,s,p,required_lessons,required_assessments):
  done={r[0] for r in self.db.execute("SELECT lesson_id FROM progress WHERE subject_id=? AND program_id=? AND completed=1",(s,p))}
  approved={r[0] for r in self.db.execute("SELECT assessment_id FROM assessment WHERE subject_id=? AND program_id=? AND status='APPROVED'",(s,p))}
  return set(required_lessons)<=done and set(required_assessments)<=approved

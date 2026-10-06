#!/usr/bin/env python3
"""Church payment/donation authority-separation reference runtime. No payment processor or card data."""
import sqlite3,time,uuid
class PaymentLedger:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
  self.db.executescript("""CREATE TABLE IF NOT EXISTS receipts(receipt_id TEXT PRIMARY KEY,subject_id TEXT,purpose TEXT NOT NULL,amount_cents INTEGER NOT NULL,status TEXT NOT NULL,external_ref TEXT UNIQUE,created_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,event TEXT NOT NULL,receipt_id TEXT NOT NULL,created_at INTEGER NOT NULL);""");self.db.commit()
 def record_provider_event(self,purpose,amount_cents,external_ref,status='CONFIRMED',subject_id=None,now=None):
  if purpose not in {'DONATION','DUES','PROGRAM_FEE','CHARter_FEE'.upper()} or not isinstance(amount_cents,int) or amount_cents<=0 or not external_ref:return None
  if status not in {'CONFIRMED','REFUNDED','DISPUTED'}:return None
  now=int(time.time() if now is None else now);rid='PAY-'+uuid.uuid4().hex[:12].upper()
  try:self.db.execute("INSERT INTO receipts VALUES(?,?,?,?,?,?,?)",(rid,subject_id,purpose,amount_cents,status,external_ref,now));self.db.commit();return rid
  except sqlite3.IntegrityError:return self.db.execute("SELECT receipt_id FROM receipts WHERE external_ref=?",(external_ref,)).fetchone()[0]
 def authority_projection(self,receipt_id):
  r=self.db.execute("SELECT receipt_id,purpose,status FROM receipts WHERE receipt_id=?",(receipt_id,)).fetchone()
  if not r:return None
  return {'receipt_id':r['receipt_id'],'purpose':r['purpose'],'payment_status':r['status'],'grants_role':False,'grants_credential':False,'grants_good_standing':False,'grants_charter':False}

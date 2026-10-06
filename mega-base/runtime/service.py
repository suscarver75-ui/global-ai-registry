"""Scoped service identity and persistent tamper-evident evidence."""
import hashlib, json, time
def register_service(conn, sid, department, capabilities):
 caps=",".join(sorted(set(capabilities)))
 conn.execute("INSERT INTO service_identities(id,department,capabilities,active) VALUES(?,?,?,1)",(sid,department,caps)); conn.commit()
def authorize(conn,sid,department,capability):
 row=conn.execute("SELECT department,capabilities,active FROM service_identities WHERE id=?",(sid,)).fetchone()
 return bool(row and row[2] and row[0]==department and capability in set(filter(None,row[1].split(","))))
def record(conn,actor,action,subject):
 prev=conn.execute("SELECT receipt_hash FROM audit_receipts ORDER BY seq DESC LIMIT 1").fetchone()
 prev_hash=prev[0] if prev else "GENESIS"
 created=int(time.time())
 payload=json.dumps([actor,action,subject,prev_hash,created],separators=(",",":"))
 h=hashlib.sha256(payload.encode()).hexdigest()
 conn.execute("INSERT INTO audit_receipts(actor,action,subject,prev_hash,receipt_hash,created_at) VALUES(?,?,?,?,?,?)",(actor,action,subject,prev_hash,h,created)); conn.commit(); return h
def verify_chain(conn):
 prev="GENESIS"
 for actor,action,subject,ph,h,created in conn.execute("SELECT actor,action,subject,prev_hash,receipt_hash,created_at FROM audit_receipts ORDER BY seq"):
  if ph!=prev: return False
  payload=json.dumps([actor,action,subject,ph,created],separators=(",",":"))
  if hashlib.sha256(payload.encode()).hexdigest()!=h: return False
  prev=h
 return True

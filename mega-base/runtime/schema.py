"""MEGA BASE developer-safe persistent schema and migration registry."""
import hashlib, sqlite3, time
MIGRATIONS = [
 ("0001_core", """CREATE TABLE IF NOT EXISTS schema_migrations(id TEXT PRIMARY KEY, checksum TEXT NOT NULL, applied_at INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS service_identities(id TEXT PRIMARY KEY, department TEXT NOT NULL, capabilities TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1);
CREATE TABLE IF NOT EXISTS audit_receipts(seq INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT NOT NULL, action TEXT NOT NULL, subject TEXT NOT NULL, prev_hash TEXT NOT NULL, receipt_hash TEXT NOT NULL UNIQUE, created_at INTEGER NOT NULL);""")
]
def checksum(sql): return hashlib.sha256(sql.encode()).hexdigest()
def connect(path): 
 c=sqlite3.connect(path); c.execute("PRAGMA foreign_keys=ON"); return c
def migrate(conn):
 for mid,sql in MIGRATIONS:
  row=conn.execute("SELECT checksum FROM schema_migrations WHERE id=?",(mid,)).fetchone() if _has(conn,"schema_migrations") else None
  want=checksum(sql)
  if row and row[0]!=want: raise RuntimeError("migration checksum drift")
  if not row:
   conn.executescript(sql)
   conn.execute("INSERT OR IGNORE INTO schema_migrations VALUES(?,?,?)",(mid,want,int(time.time())))
 conn.commit()
def _has(conn,name):
 return conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",(name,)).fetchone() is not None

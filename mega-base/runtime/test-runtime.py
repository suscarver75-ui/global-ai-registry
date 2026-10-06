import os, tempfile, unittest
from schema import connect,migrate
from service import register_service,authorize,record,verify_chain
class TestRuntime(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.NamedTemporaryFile(delete=False); self.tmp.close()
  self.db=connect(self.tmp.name); migrate(self.db)
 def tearDown(self): self.db.close(); os.unlink(self.tmp.name)
 def test_migration_idempotent(self): migrate(self.db); self.assertEqual(self.db.execute("select count(*) from schema_migrations").fetchone()[0],1)
 def test_scoped_identity(self):
  register_service(self.db,"church-runtime","seven-fold",["profile.read","training.verify"])
  self.assertTrue(authorize(self.db,"church-runtime","seven-fold","training.verify"))
  self.assertFalse(authorize(self.db,"church-runtime","mac-henry-private","training.verify"))
  self.assertFalse(authorize(self.db,"church-runtime","seven-fold","owner.override"))
 def test_persistent_evidence(self):
  record(self.db,"church-runtime","training.verify","member:opaque-1"); record(self.db,"church-runtime","credential.request","member:opaque-1")
  self.assertTrue(verify_chain(self.db))
  self.db.execute("update audit_receipts set action='tampered' where seq=1"); self.db.commit()
  self.assertFalse(verify_chain(self.db))
if __name__=="__main__": unittest.main()

#!/usr/bin/env python3
import importlib.util,sys,tempfile,os,sqlite3
from pathlib import Path
P=Path(__file__).resolve().parent/'protected-data.py'; s=importlib.util.spec_from_file_location('pd',P); m=importlib.util.module_from_spec(s); sys.modules[s.name]=m;s.loader.exec_module(m)
st=m.ProtectedStore(); a={'authenticated':True,'subject_id':'a','zone':'MEMBER','human_actor':True}; b={'authenticated':True,'subject_id':'b','zone':'MEMBER','human_actor':True}
assert st.put_profile(a,'a','Member A',{'locale':'en'}); assert st.get_profile(a,'a')['display_name']=='Member A'
assert st.get_profile(b,'a') is None; assert not st.put_profile(b,'a','attack')
assert st.record_consent(a,'a','privacy-v1',True,10); assert not st.record_consent(b,'a','privacy-v1',False,11)
assert st.export_subject(a,'a')['consents'][0]['granted']==1
assert st.integrity_ok()
fd,path=tempfile.mkstemp();os.close(fd); st.backup_to(path); db=sqlite3.connect(path); assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'; assert db.execute('SELECT count(*) FROM profiles').fetchone()[0]==1; db.close();os.unlink(path)
owner={'authenticated':True,'subject_id':'owner','zone':'MAC_HENRY_OWNER','human_actor':True,'owner_approved':True,'step_up':True}
assert st.delete_subject_data(owner,'a'); assert st.get_profile(a,'a') is None
assert st.db.execute("SELECT count(*) FROM audit WHERE event='SUBJECT_DATA_DELETED'").fetchone()[0]==1
print('ALL PROTECTED DATA TESTS PASS')

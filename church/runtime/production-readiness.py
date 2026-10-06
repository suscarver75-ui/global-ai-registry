#!/usr/bin/env python3
"""Production-readiness gate: proves configuration completeness without storing secrets."""
import os,json
REQUIRED=('CHURCH_ENV','CHURCH_BASE_URL','CHURCH_IDENTITY_PROVIDER','CHURCH_DATABASE_PROVIDER','CHURCH_SECRET_PROVIDER','CHURCH_AUDIT_SINK','CHURCH_HEALTH_ENDPOINT','CHURCH_BACKUP_TARGET')
SECRET_NAMES=('CHURCH_SESSION_SECRET','CHURCH_DATABASE_URL','CHURCH_PROVIDER_TOKEN')
def assess(env):
 missing=[k for k in REQUIRED if not env.get(k)]
 placeholders=[k for k in REQUIRED if str(env.get(k,'')).lower() in {'todo','placeholder','example','changeme'}]
 secret_presence={k:bool(env.get(k)) for k in SECRET_NAMES}
 ready=not missing and not placeholders and all(secret_presence.values())
 return {'ready':ready,'missing_configuration':missing,'placeholder_configuration':placeholders,'secret_presence':secret_presence,'secret_values_exposed':False}
if __name__=='__main__': print(json.dumps(assess(os.environ),sort_keys=True))

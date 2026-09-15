#!/usr/bin/env python3
"""Replays only labeled closure fixtures for the authorized resident demo identity."""
import json,urllib.request,os,sys
if "--authorized-demo" not in sys.argv:
 raise SystemExit("Explicit --authorized-demo and PGR_ACCEPTANCE_CREDENTIALS are required.")
from pathlib import Path
base='https://android.pgsims.alshifalab.pk/'
credentials=json.loads(Path(os.environ['PGR_ACCEPTANCE_CREDENTIALS']).read_text())['resident']
def call(path,payload=None,token=None):
 headers={'Content-Type':'application/json'}
 if token: headers['Authorization']='Bearer '+token
 request=urllib.request.Request(base+path,data=json.dumps(payload).encode() if payload is not None else None,headers=headers)
 with urllib.request.urlopen(request,timeout=30) as response: return response.status,json.load(response)
_,session=call('api/auth/login/',{'username':credentials[0],'password':credentials[1]})
token=session['access']
def rows(path):
 _,value=call(path,token=token)
 return value if isinstance(value,list) else value.get('results',[])
prefix='ANDROID-ACCEPTANCE-20260915-CLOSURE-'
leaves=[r for r in rows('api/my/leaves/') if r.get('reason','').startswith(prefix)]
books=[r for r in rows('api/academics/logbook-entries/') if r.get('title','').startswith(prefix)]
assert len(leaves)==1 and len(books)==1
for kind,record in [('leave',leaves[0]),('logbook',books[0])]:
 if kind=='leave':
  key=record['client_request_id'];payload={k:record[k] for k in ('resident_training','leave_type','start_date','end_date','reason','client_request_id')};path='api/leaves/'
 else:
  key=record['extra_data']['mobile_client_request_id'];payload={k:record[k] for k in ('category','entry_date','title')};payload['client_request_id']=key;path='api/academics/logbook-entries/'
 assert key
 for attempt in range(2):
  code,replay=call(path,payload,token)
  assert code==200 and replay['id']==record['id'],(kind,code)
 print(kind,'record',record['id'],'key',key,'two HTTPS replays HTTP200/same ID PASS')
call('api/auth/logout/',{'refresh':session['refresh']},token)

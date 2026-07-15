from pathlib import Path
import json, sys, yaml
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
def fail(m): print('ERROR:',m,file=sys.stderr); raise SystemExit(1)
def load(p):
 try:return json.loads((ROOT/p).read_text())
 except Exception as e: fail(f'{p}: {e}')
manifest=load('contracts/manifest.json')
for a in manifest['artifacts']:
 if not (ROOT/a['path']).is_file(): fail(f"missing {a['path']}")
fixtures={}; all_defs={}
for artifact in manifest['artifacts']:
 if artifact['kind']=='schemas':
  document=load(artifact['path']); Draft202012Validator.check_schema(document); all_defs.update(document['$defs'])
 if artifact['kind']=='fixtures': fixtures.update(load(artifact['path'])['fixtures'])
for name,instance in fixtures.items():
 if name not in all_defs: fail(f'fixture without schema: {name}')
 wrapper={'$schema':'https://json-schema.org/draft/2020-12/schema','$defs':all_defs,'$ref':f'#/$defs/{name}'}
 errors=sorted(Draft202012Validator(wrapper,format_checker=FormatChecker()).iter_errors(instance),key=lambda e:list(e.path))
 if errors: fail(f"{name}: "+'; '.join(f'{list(e.path)} {e.message}' for e in errors[:5]))
manifest_defs=set().union(*(set(a.get('definitions',[])) for a in manifest['artifacts'] if a['kind']=='schemas'))
if manifest_defs!=set(fixtures): fail('manifest/schema/fixture definition drift')
schemas={'$defs':all_defs}
regs=load('contracts/registries.json')['registries']
life=regs['lifecycle-states']['aggregates']
checks={'Run':('run-header','status'),'ActivityRun':('activity-run','status'),'DurableCommand':('durable-command','status'),'Effect':('effect','status'),'Invocation':('invocation','status'),'WorkerLease':('worker-lease','status'),'ApprovalCase':('approval-case','status'),'CancellationBarrier':('cancellation-barrier','status')}
for agg,(name,prop) in checks.items():
 if schemas['$defs'][name]['properties'][prop]['enum']!=life[agg]: fail(f'lifecycle drift: {agg}')
cmd=[e['id'] for e in regs['durable-command-kinds']['entries']]
if cmd!=schemas['$defs']['durable-command']['properties']['commandKind']['enum']: fail('command registry drift')
profiles=[e['id'] for e in regs['execution-authority-profiles']['entries']]
for name,prop in [('deployment-snapshot','executionAuthorityProfile'),('run-authority','profile'),('run-header','authorityProfile')]:
 if schemas['$defs'][name]['properties'][prop]['enum']!=profiles: fail(f'authority profile drift: {name}')
openapi=yaml.safe_load((ROOT/'contracts/profiles/openapi.yaml').read_text()); asyncapi=yaml.safe_load((ROOT/'contracts/profiles/asyncapi.yaml').read_text())
if openapi.get('openapi')!='3.1.1': fail('OpenAPI version')
ops={op.get('operationId') for item in openapi['paths'].values() for method,op in item.items() if method in {'get','post','put','patch','delete'}}
if ops!={'startRun','getRun','signalRun','cancelRun','decideApprovalCase','streamRunEvents'}: fail('OpenAPI operations')
if asyncapi.get('asyncapi')!='3.0.0': fail('AsyncAPI version')
print(f"Validated {len(fixtures)} schema definitions and fixtures, {len(regs)} registries, OpenAPI, and AsyncAPI.")

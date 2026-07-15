from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
def fail(m): print('ERROR:',m,file=sys.stderr); raise SystemExit(1)
def read(p): return (ROOT/p).read_text()
docs=json.loads(read('docs.json')); tabs=docs['navigation']['tabs']
if [t['tab'] for t in tabs]!=['Specification','Build','Reference','Project']: fail('canonical tabs')
pages=[p for t in tabs for g in t['groups'] for p in g.get('pages',[])]
if len(pages)!=len(set(pages)): fail('duplicate page')
for p in pages:
 if not (ROOT/f'{p}.mdx').is_file(): fail(f'missing page {p}')
public=sorted(p.relative_to(ROOT).with_suffix('').as_posix() for p in ROOT.rglob('*.mdx'))
if sorted(pages)!=public: fail(f'navigation mismatch missing={sorted(set(public)-set(pages))} extra={sorted(set(pages)-set(public))}')
fm=re.compile(r'^---\n.*?^title:\s*.+$.*?^description:\s*.+$.*?^---\n',re.M|re.S)
for p in public:
 if not fm.match(read(f'{p}.mdx')): fail(f'frontmatter {p}')
live={'/'+p for p in public}; seen=set()
for r in docs['redirects']:
 if r['source'] in seen: fail(f'duplicate redirect {r["source"]}')
 seen.add(r['source'])
 if r['source'] in live: fail(f'redirect shadows live page {r["source"]}')
 if r['destination'] not in live: fail(f'missing redirect destination {r}')
text='\n'.join(read(f'{p}.mdx') for p in public)+read('README.md')+read('AGENTS.md')
for phrase in ['one sequenced execution authority','DurableCommand','ApprovalCase','CancellationBarrier','ara_log_v1','temporal_history_v1']:
 if phrase not in text: fail(f'missing {phrase}')
for pattern,label in [(r'An independent `AgentRun` \*\*MUST\*\* own exactly one root `WorkflowRun`','wrapper Run'),(r'interface ExecutionContext\s*\{','god context'),(r'nextState:\s*RunState','full-state commit'),(r'cumulative ARA Core','cumulative modules')]:
 if re.search(pattern,text,re.I): fail(f'stale {label}')
minimal=read('guides/minimal-internal-app.mdx')
required_sections=['## Decision','## Intended scope','## Explicit non-goals','## Physical topology','## Repository layout','## Minimal runtime model','## Command and execution flow','## Fenced Run commit','## Idempotency','## Retry and ambiguous outcomes','## Human approval','## Cancellation','## API surface','## Authentication and authorization','## Testing and evaluation','## Production deployment','## Acceptance criteria','## Growth triggers']
for section in required_sections:
 if section not in minimal: fail(f'minimal profile missing {section}')
for technology in ['TypeScript + Bun','React + Next.js App Router','PostgreSQL','S3-compatible object storage','company OIDC provider','OpenTelemetry']:
 if technology not in minimal: fail(f'minimal profile missing technology: {technology}')
if (ROOT/'guides/database-runtime.mdx').exists(): fail('database-runtime guide must remain consolidated into minimal-internal-app')
print(f'Validated {len(public)} public pages, navigation, redirects, frontmatter, terminology, and minimal profile completeness.')

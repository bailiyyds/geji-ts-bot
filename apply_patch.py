from pathlib import Path
import hashlib,json,sys
manifest=json.loads(Path(__file__).with_name('patch.json').read_text(encoding='utf-8'))
source=Path(sys.argv[1]).read_bytes()
if hashlib.sha256(source).hexdigest()!=manifest['base_sha256']:raise SystemExit('Unsupported upstream bundle: refusing to patch')
text=source.decode('utf-8')
for op in reversed(manifest['operations']):
 if text[op['start']:op['end']]!=op['old']:raise SystemExit('Patch context mismatch')
 text=text[:op['start']]+op['new']+text[op['end']:]
result=text.encode('utf-8')
if hashlib.sha256(result).hexdigest()!=manifest['output_sha256']:raise SystemExit('Output mismatch')
out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(result)
print('Patch verified:',out)

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, existsSync, mkdirSync, readFileSync, writeFileSync, symlinkSync, statSync, utimesSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
const CLI = fileURLToPath(new URL('../bin/delegrix.js', import.meta.url));
function run(cwd, ...args) {
  const r = spawnSync(process.execPath, [CLI, ...args], {cwd, encoding:'utf8'});
  return {code:r.status, output:r.stdout+r.stderr};
}
function fixture() { return mkdtempSync(join(tmpdir(),'delegrix-')); }
test('install/status/uninstall codex without editing user config', ()=>{
  const dir=fixture();
  mkdirSync(join(dir,'.codex'),{recursive:true});
  writeFileSync(join(dir,'.codex','config.toml'), '[agents]\nmax_depth = 1\n');
  assert.equal(run(dir,'install','--client','codex').code,0);
  assert.ok(existsSync(join(dir,'.agents','skills','delegrix','SKILL.md')));
  assert.match(run(dir,'status','--client','codex').output,/installed/);
  assert.equal(run(dir,'uninstall','--client','codex').code,0);
  assert.ok(!existsSync(join(dir,'.agents','skills','delegrix')));
  assert.equal(readFileSync(join(dir,'.codex','config.toml'),'utf8'),'[agents]\nmax_depth = 1\n');
});
test('dry-run never writes, all clients install with shared codex/cursor path', ()=>{
  const dir=fixture();
  assert.equal(run(dir,'install','--dry-run').code,0);
  assert.ok(!existsSync(join(dir,'.agents')));
  assert.equal(run(dir,'install').code,0);
  assert.ok(existsSync(join(dir,'.agents','skills','delegrix','SKILL.md')));
  assert.ok(existsSync(join(dir,'.claude','skills','delegrix','SKILL.md')));
  assert.equal(run(dir,'uninstall').code,0);
});
test('force refresh preserves unrelated user-owned files', ()=>{
  const dir=fixture();
  assert.equal(run(dir,'install').code,0);
  const dest=join(dir,'.agents','skills','delegrix');
  writeFileSync(join(dest,'user-notes.txt'),'mine');
  assert.match(run(dir,'install').output,/skip/);
  assert.equal(run(dir,'install','--force').code,0);
  assert.ok(existsSync(join(dest,'user-notes.txt')));
  assert.equal(run(dir,'uninstall').code,0);
  assert.equal(readFileSync(join(dest,'user-notes.txt'),'utf8'),'mine');
});
test('refuse overwrite/uninstall of unmanaged skill',()=>{
  const dir=fixture();
  const dest=join(dir,'.agents','skills','delegrix');
  mkdirSync(dest,{recursive:true});
  writeFileSync(join(dest,'SKILL.md'),'---\nname: unrelated\n---\n');
  assert.equal(run(dir,'install','--force').code,1);
  assert.equal(run(dir,'uninstall').code,1);
  assert.match(readFileSync(join(dest,'SKILL.md'),'utf8'),/unrelated/);
});
test('argument validation and version',()=>{
 const dir=fixture();
 assert.equal(run(dir,'install','--client','invalid').code,1);
 assert.equal(run(dir,'install','--client').code,1);
 assert.equal(run(dir,'unknown').code,1);
 assert.match(run(dir,'--version').output,/0\.1\.0/);
});

test('refuse nested symlink paths when refreshing or uninstalling', {skip: process.platform === 'win32'}, ()=>{
 const dir=fixture();
 assert.equal(run(dir,'install','--client','codex').code,0);
 const dest=join(dir,'.agents','skills','delegrix');
 const external=fixture();
 const link=join(dest,'unmanaged-link');
 symlinkSync(external, link, 'dir');
 assert.equal(run(dir,'install','--client','codex','--force').code,1);
 assert.equal(run(dir,'uninstall','--client','codex').code,1);
 assert.ok(existsSync(link));
});

test('update refreshes a managed installation and retains unrelated files', ()=>{
 const dir=fixture();
 assert.equal(run(dir,'install','--client','codex').code,0);
 const dest=join(dir,'.agents','skills','delegrix');
 const skill=join(dest,'SKILL.md');
 writeFileSync(skill,'---\nname: delegrix\nmetadata:\n  version: "0.0.9"\n---\nLegacy Delegrix\n');
 writeFileSync(join(dest,'my-notes.txt'),'do not delete');
 const preview=run(dir,'update','--client','codex','--dry-run');
 assert.equal(preview.code,0,preview.output);
 assert.match(preview.output,/would update/);
 assert.match(readFileSync(skill,'utf8'),/0\.0\.9/);
 const updated=run(dir,'update','--client','codex');
 assert.equal(updated.code,0,updated.output);
 assert.match(updated.output,/update/);
 assert.match(readFileSync(skill,'utf8'),/version: "0\.1\.0"/);
 assert.equal(readFileSync(join(dest,'my-notes.txt'),'utf8'),'do not delete');
 assert.match(run(dir,'status','--client','codex').output,/installed v0\.1\.0/);
 const again=run(dir,'update','--client','codex');
 assert.equal(again.code,0,again.output);
 assert.match(again.output,/up to date/);
});

test('update restores missing managed files without rewriting unchanged files', () => {
  const dir = fixture();
  const dest = join(dir, '.agents', 'skills', 'delegrix');
  const skill = join(dest, 'SKILL.md');
  const source = new URL('../skills/delegrix/', import.meta.url);
  mkdirSync(dest, { recursive: true });
  writeFileSync(skill, readFileSync(new URL('SKILL.md', source)));
  const oldTime = new Date('2000-01-01T00:00:00Z');
  utimesSync(skill, oldTime, oldTime);
  const originalMtime = statSync(skill).mtimeMs;

  const result = run(dir, 'update', '--client', 'codex');

  assert.equal(result.code, 0, result.output);
  assert.deepEqual(readFileSync(join(dest, 'agents', 'openai.yaml')), readFileSync(new URL('agents/openai.yaml', source)));
  assert.equal(statSync(skill).mtimeMs, originalMtime, 'unchanged SKILL.md was rewritten');
});

test('update refuses missing and unmanaged installations', ()=>{
 const dir=fixture();
 const absent=run(dir,'update','--client','codex');
 assert.equal(absent.code,1);
 assert.match(absent.output,/use install first/);
 assert.ok(!existsSync(join(dir,'.agents')));
 const dest=join(dir,'.agents','skills','delegrix');
 mkdirSync(dest,{recursive:true});
 writeFileSync(join(dest,'SKILL.md'),'---\nname: someone-else\n---\n');
 const other=run(dir,'update','--client','codex');
 assert.equal(other.code,1);
 assert.match(other.output,/unmanaged skill/);
 assert.match(readFileSync(join(dest,'SKILL.md'),'utf8'),/someone-else/);
});

test('update respects existing symlink protection', {skip: process.platform === 'win32'}, ()=>{
 const dir=fixture();
 assert.equal(run(dir,'install','--client','codex').code,0);
 const dest=join(dir,'.agents','skills','delegrix');
 const external=fixture();
 symlinkSync(external, join(dest,'external'), 'dir');
 const result=run(dir,'update','--client','codex');
 assert.equal(result.code,1);
 assert.match(result.output,/symbolic-link/);
});

test('update all refreshes both Codex/Cursor shared and Claude targets', ()=>{
 const dir=fixture();
 assert.equal(run(dir,'install').code,0);
 for(const base of [join(dir,'.agents','skills'),join(dir,'.claude','skills')])
   writeFileSync(join(base,'delegrix','SKILL.md'),'---\nname: delegrix\nmetadata:\n  version: "0.0.1"\n---\n');
 const result=run(dir,'update');
 assert.equal(result.code,0,result.output);
 assert.match(result.output,/codex\+cursor/);
 assert.match(result.output,/claude/);
 for(const base of [join(dir,'.agents','skills'),join(dir,'.claude','skills')])
   assert.match(readFileSync(join(base,'delegrix','SKILL.md'),'utf8'),/version: "0\.1\.0"/);
});

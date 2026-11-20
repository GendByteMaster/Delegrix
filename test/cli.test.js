import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, existsSync, mkdirSync, readFileSync, writeFileSync, symlinkSync } from 'node:fs';
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

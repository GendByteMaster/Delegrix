#!/usr/bin/env node
import { cpSync, existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, rmdirSync, unlinkSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const SOURCE = fileURLToPath(new URL('../skills/delegrix/', import.meta.url));
const VERSION = '0.1.0';
const CLIENTS = ['codex', 'claude', 'cursor'];

function options(argv) {
  const result = { action: 'help', client: 'all', global: false, force: false, dryRun: false };
  const args = [...argv];
  if (args[0] && !args[0].startsWith('-')) result.action = args.shift();
  while (args.length) {
    const arg = args.shift();
    if (arg === '--client') {
      if (!args[0] || args[0].startsWith('-')) throw new Error('--client requires a value');
      result.client = args.shift();
    } else if (arg === '--global') result.global = true;
    else if (arg === '--force') result.force = true;
    else if (arg === '--dry-run') result.dryRun = true;
    else if (arg === '--help' || arg === '-h') result.action = 'help';
    else if (arg === '--version' || arg === '-v') result.action = 'version';
    else throw new Error('unknown argument: ' + arg);
  }
  if (!['help', 'version', 'install', 'update', 'status', 'uninstall'].includes(result.action)) throw new Error('unknown command: ' + result.action);
  if (result.client !== 'all' && !CLIENTS.includes(result.client)) throw new Error('unsupported client: ' + result.client);
  return result;
}

function targets(opts) {
  const clients = opts.client === 'all' ? CLIENTS : [opts.client];
  const home = homedir();
  const root = process.cwd();
  const out = new Map();
  for (const client of clients) {
    const base = opts.global
      ? (client === 'codex' ? join(home, '.agents', 'skills') : join(home, client === 'claude' ? '.claude' : '.cursor', 'skills'))
      : (client === 'claude' ? join(root, '.claude', 'skills') : join(root, '.agents', 'skills'));
    const dest = join(base, 'delegrix');
    out.set(dest, [...(out.get(dest) || []), client]);
  }
  return out;
}

function assertNoSymlinks(path) {
  if (!existsSync(path)) return;
  const entry = lstatSync(path);
  if (entry.isSymbolicLink()) throw new Error('refuse symbolic-link path: ' + path);
  if (entry.isDirectory()) {
    for (const name of readdirSync(path)) assertNoSymlinks(join(path, name));
  }
}

function validOwner(dest) {
  if (!existsSync(dest)) return false;
  assertNoSymlinks(dest);
  const skill = join(dest, 'SKILL.md');
  return existsSync(skill) && /^name:\s*delegrix\s*$/m.test(readFileSync(skill, 'utf8'));
}

function filesBelow(root, prefix = '') {
  let files = [];
  for (const entry of readdirSync(join(root, prefix), { withFileTypes: true })) {
    const rel = join(prefix, entry.name);
    if (entry.isDirectory()) files = files.concat(filesBelow(root, rel));
    else if (entry.isFile()) files.push(rel);
  }
  return files;
}

function sourceChanges(dest) {
  return filesBelow(SOURCE).filter(rel => {
    const installed = join(dest, rel);
    return !existsSync(installed) || !readFileSync(installed).equals(readFileSync(join(SOURCE, rel)));
  });
}

function installedVersion(dest) {
  const content = readFileSync(join(dest, 'SKILL.md'), 'utf8');
  const match = content.match(/^\s+version:\s*["']?([a-zA-Z0-9.-]+)/m);
  return match ? match[1] : 'unknown';
}

function removeManaged(dest) {
  const sourceFiles = filesBelow(SOURCE);
  for (const rel of sourceFiles) {
    const target = join(dest, rel);
    if (existsSync(target)) unlinkSync(target);
  }
  const dirs = [...new Set(sourceFiles.map(x => dirname(x)).filter(x => x !== '.'))].sort((a,b)=>b.length-a.length);
  for (const dir of dirs) {
    const target = join(dest, dir);
    if (existsSync(target) && readdirSync(target).length === 0) rmdirSync(target);
  }
  if (existsSync(dest) && readdirSync(dest).length === 0) rmdirSync(dest);
}

function main() {
  const opts = options(process.argv.slice(2));
  if (opts.action === 'help') {
    console.log('Delegrix v' + VERSION + '\nUsage: delegrix <install|update|status|uninstall> [--client all|codex|claude|cursor] [--global] [--force] [--dry-run]');
    return;
  }
  if (opts.action === 'version') { console.log(VERSION); return; }
  for (const [dest, clients] of targets(opts)) {
    const label = clients.join('+');
    if (opts.action === 'status') {
      const managed = validOwner(dest);
      console.log((managed ? 'installed v' + installedVersion(dest) : 'missing') + ' ' + label + ': ' + dest);
      continue;
    }
    if (opts.action === 'update') {
      if (!existsSync(dest)) {
        console.error('not installed ' + label + ': ' + dest + ' (use install first)');
        process.exitCode = 1;
        continue;
      }
      if (!validOwner(dest)) throw new Error('refuse to update unmanaged skill: ' + dest);
      const changes = sourceChanges(dest);
      if (changes.length === 0) {
        console.log('up to date  ' + label + ': ' + dest + ' (v' + VERSION + ')');
        continue;
      }
      console.log((opts.dryRun ? 'would update ' : 'update     ') + label + ': ' + dest +
        ' (' + changes.length + ' managed file(s); v' + installedVersion(dest) + ' -> v' + VERSION + ')');
      if (!opts.dryRun) {
        for (const rel of changes) {
          const installed = join(dest, rel);
          mkdirSync(dirname(installed), { recursive: true });
          cpSync(join(SOURCE, rel), installed, { force: true });
        }
      }
      continue;
    }
    if (opts.action === 'install') {
      if (existsSync(dest) && !opts.force) { console.log('skip      ' + label + ': ' + dest); continue; }
      if (existsSync(dest) && !validOwner(dest)) throw new Error('refuse to overwrite unmanaged skill: ' + dest);
      console.log((opts.dryRun ? 'would install ' : 'install   ') + label + ': ' + dest);
      if (!opts.dryRun) { mkdirSync(dest, {recursive:true}); cpSync(SOURCE, dest, {recursive:true, force:true}); }
    } else {
      if (!existsSync(dest)) { console.log('missing   ' + label + ': ' + dest); continue; }
      if (!validOwner(dest)) throw new Error('refuse to uninstall unmanaged skill: ' + dest);
      console.log((opts.dryRun ? 'would remove ' : 'remove    ') + label + ': ' + dest);
      if (!opts.dryRun) removeManaged(dest);
    }
  }
}
try { main(); } catch(e) { console.error('delegrix: ' + e.message); process.exitCode = 1; }

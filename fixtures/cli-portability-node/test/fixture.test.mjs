import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const entry = fileURLToPath(new URL('../bin/fixture.mjs', import.meta.url));
const result = spawnSync(process.execPath, [entry, '--help'], {
  encoding: 'utf8',
  windowsHide: true,
});

assert.equal(result.error, undefined);
assert.equal(result.status, 0, result.stderr);
assert.match(result.stdout, /^Usage: cli-portability-fixture/);
assert.equal(result.stderr, '');

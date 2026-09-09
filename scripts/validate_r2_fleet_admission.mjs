import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, resolve } from 'node:path';

if (process.argv.length !== 2) {
  throw new Error('validate_r2_fleet_admission.mjs accepts no command-line arguments');
}

const ROOT = resolve(import.meta.dirname, '..');
const CONTRACT = join(ROOT, 'contracts', 'r2-fleet-admission');
const PROGRAM_PATH = join(CONTRACT, 'program.json');
const TYPESPEC_PATH = join(CONTRACT, 'main.tsp');
const SCHEMA_PATH = join(CONTRACT, 'authored.schema.json');

const ADMISSION_STATES = new Set(['planned', 'in_progress', 'blocked', 'verified', 'not_applicable']);
const EVIDENCE_STATES = new Set([
  'unknown', 'not_executed', 'stale', 'stopped_for_evaluation', 'failed', 'passed',
]);
const TASK_CATEGORIES = new Set([
  'inventory_state', 'credentials', 'ci', 'contracts', 'migration', 'lifecycle',
  'application', 'isolation', 'crypto', 'retention', 'observability', 'recovery',
]);
const EXPECTED_TASK_ISSUES = new Map([
  ['R2-01', 42], ['R2-02', 45], ['R2-03', 47], ['R2-04', 48],
  ['R2-05', 49], ['R2-06', 50], ['R2-07', 51], ['R2-08', 52],
  ['R2-09', 53], ['R2-10', 56], ['R2-11', 58], ['R2-12', 61],
]);
const EXPECTED_ORGANIZATIONS = new Set([
  'claimgraph', 'cliptown', 'daedalus-fab', 'elenkos-systems', 'fiducia-cloud',
  'memebank', 'messaging-intel', 'ores-legal', 'quaestor-ledger',
  'sonus-auris', 'zed-pkg',
]);
const PROGRAM_KEYS = [
  'authorityPrecedence', 'generatedEvidenceRole', 'githubProgramIssue',
  'linearIssue', 'organizations', 'programState', 'schemaVersion', 'tasks',
];
const TASK_KEYS = ['category', 'code', 'dependsOn', 'issue', 'state', 'title'];
const ORG_KEYS = [
  'applicationAuthorization', 'credentialScope', 'documentAdmission',
  'keyRecovery', 'liveInventory', 'namespaceState', 'organization',
  'readIsolation', 'recovery', 'retention', 'stateOwnership', 'writeIsolation',
];
const EVIDENCE_FIELDS = [
  'liveInventory', 'stateOwnership', 'credentialScope', 'readIsolation',
  'writeIsolation', 'applicationAuthorization', 'keyRecovery', 'retention', 'recovery',
];
const FORBIDDEN_PUBLIC_KEYS = new Set([
  'accountId', 'accessKeyId', 'bucketName', 'customerId', 'objectKey',
  'providerPayload', 'runtimeTokenId', 'secret', 'stateSnapshot', 'token',
]);

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function denseArray(value, label) {
  assert(Array.isArray(value), `${label} must be an array`);
  assert(Object.keys(value).every((key, index) => key === String(index)),
    `${label} must be dense and free of custom properties`);
  return value;
}

function plainObject(value, label) {
  assert(value !== null && typeof value === 'object' && !Array.isArray(value),
    `${label} must be an object`);
  const prototype = Object.getPrototypeOf(value);
  assert(prototype === Object.prototype || prototype === null,
    `${label} must be a plain object`);
  return value;
}

function exactKeys(value, expected, label) {
  const actual = Object.keys(plainObject(value, label)).sort();
  assert(JSON.stringify(actual) === JSON.stringify([...expected].sort()),
    `${label} has missing or unexpected fields`);
}

function assertNoForbiddenFields(value, pointer = '#') {
  if (Array.isArray(value)) {
    value.forEach((item, index) => assertNoForbiddenFields(item, `${pointer}/${index}`));
    return;
  }
  if (value === null || typeof value !== 'object') return;
  for (const [key, child] of Object.entries(value)) {
    assert(!FORBIDDEN_PUBLIC_KEYS.has(key), `forbidden public field ${pointer}/${key}`);
    assertNoForbiddenFields(child, `${pointer}/${key}`);
  }
}

function filesRecursively(path) {
  const files = [];
  for (const name of readdirSync(path)) {
    const child = join(path, name);
    if (statSync(child).isDirectory()) files.push(...filesRecursively(child));
    else files.push(child);
  }
  return files;
}

function assertAcyclic(tasks) {
  const byCode = new Map(tasks.map((task) => [task.code, task]));
  const visiting = new Set();
  const visited = new Set();
  function visit(code) {
    if (visited.has(code)) return;
    assert(!visiting.has(code), `task dependency cycle includes ${code}`);
    visiting.add(code);
    for (const dependency of byCode.get(code).dependsOn) visit(dependency);
    visiting.delete(code);
    visited.add(code);
  }
  for (const code of byCode.keys()) visit(code);
}

const program = readJson(PROGRAM_PATH);
assertNoForbiddenFields(program);
exactKeys(program, PROGRAM_KEYS, 'program');
assert(program.schemaVersion === 'ores.r2-fleet-admission/v1', 'unsupported schemaVersion');
assert(program.linearIssue === 'DEN-3109', 'unexpected Linear parent');
assert(program.githubProgramIssue === 'https://github.com/ORESoftware/.github/issues/39',
  'unexpected GitHub program issue');
assert(program.programState === 'in_progress', 'program must remain in progress until live admission closes');
assert(program.generatedEvidenceRole === 'comparison_evidence_only',
  'generated evidence cannot become an authority');
assert(program.authorityPrecedence === 'none', 'peer authorities cannot have precedence');

const tasks = denseArray(program.tasks, 'tasks');
assert(tasks.length === EXPECTED_TASK_ISSUES.size, 'task inventory is incomplete');
const taskCodes = new Set();
const issueUrls = new Set();
for (const [index, task] of tasks.entries()) {
  exactKeys(task, TASK_KEYS, `tasks/${index}`);
  assert(/^R2-(?:0[1-9]|1[0-2])$/u.test(task.code), `invalid task code at ${index}`);
  assert(!taskCodes.has(task.code), `duplicate task code ${task.code}`);
  taskCodes.add(task.code);
  const issueNumber = EXPECTED_TASK_ISSUES.get(task.code);
  assert(issueNumber !== undefined, `unregistered task ${task.code}`);
  assert(task.issue === `https://github.com/ORESoftware/.github/issues/${issueNumber}`,
    `task ${task.code} points to the wrong issue`);
  assert(!issueUrls.has(task.issue), `duplicate task issue ${task.issue}`);
  issueUrls.add(task.issue);
  assert(typeof task.title === 'string' && task.title.trim() === task.title && task.title.length >= 12,
    `invalid title for ${task.code}`);
  assert(TASK_CATEGORIES.has(task.category), `invalid category for ${task.code}`);
  assert(ADMISSION_STATES.has(task.state), `invalid state for ${task.code}`);
  denseArray(task.dependsOn, `${task.code}.dependsOn`);
  assert(new Set(task.dependsOn).size === task.dependsOn.length,
    `duplicate dependencies for ${task.code}`);
  for (const dependency of task.dependsOn) {
    assert(EXPECTED_TASK_ISSUES.has(dependency), `unknown dependency ${dependency}`);
    assert(dependency !== task.code, `self dependency for ${task.code}`);
  }
}
assertAcyclic(tasks);
for (const task of tasks) {
  if (task.state !== 'verified') continue;
  for (const dependency of task.dependsOn) {
    assert(tasks.find((candidate) => candidate.code === dependency).state === 'verified',
      `${task.code} cannot be verified before ${dependency}`);
  }
}

const organizations = denseArray(program.organizations, 'organizations');
assert(organizations.length === EXPECTED_ORGANIZATIONS.size, 'organization inventory is incomplete');
const observedOrganizations = new Set();
for (const [index, organization] of organizations.entries()) {
  exactKeys(organization, ORG_KEYS, `organizations/${index}`);
  assert(EXPECTED_ORGANIZATIONS.has(organization.organization),
    `unregistered organization ${organization.organization}`);
  assert(!observedOrganizations.has(organization.organization),
    `duplicate organization ${organization.organization}`);
  observedOrganizations.add(organization.organization);
  assert(organization.namespaceState === 'verified',
    `organization namespace is not verified for ${organization.organization}`);
  for (const field of EVIDENCE_FIELDS) {
    assert(EVIDENCE_STATES.has(organization[field]),
      `invalid ${field} state for ${organization.organization}`);
  }
  assert(['blocked', 'verified'].includes(organization.documentAdmission),
    `invalid document admission state for ${organization.organization}`);
  if (organization.documentAdmission !== 'verified') continue;
  for (const field of EVIDENCE_FIELDS) {
    assert(organization[field] === 'passed',
      `${organization.organization} cannot be admitted while ${field} is not passed`);
  }
}

const typeSpec = readFileSync(TYPESPEC_PATH, 'utf8');
const authored = readJson(SCHEMA_PATH);
const declarationNames = [...typeSpec.matchAll(
  /^\s*(?:enum|model|scalar|union|alias)\s+([A-Za-z_][A-Za-z0-9_]*)/gmu,
)].map((match) => match[1]);
assert(declarationNames.length >= 8, 'TypeSpec declaration inventory is incomplete');
assert(new Set(declarationNames).size === declarationNames.length,
  'TypeSpec declarations must be unique');
assert(JSON.stringify([...declarationNames].sort())
  === JSON.stringify(Object.keys(authored.$defs ?? {}).sort()),
'TypeSpec and authored JSON Schema top-level declarations differ');
assert(authored.$schema === 'https://json-schema.org/draft/2020-12/schema',
  'authored schema must use Draft 2020-12');

const corpusFiles = filesRecursively(join(CONTRACT, 'instances')).filter((path) => path.endsWith('.json'));
assert(corpusFiles.length >= 4, 'instance corpus is incomplete');
for (const path of corpusFiles) readJson(path);

const credentialPattern = new RegExp('(?:gh' + 'p_|lin' + '_api_)[A-Za-z0-9_-]+', 'u');
for (const path of [
  PROGRAM_PATH, TYPESPEC_PATH, SCHEMA_PATH, ...corpusFiles,
  join(ROOT, 'docs', 'r2-fleet-admission.md'),
  join(ROOT, '.github', 'ISSUE_TEMPLATE', 'r2_storage_admission.yml'),
  join(ROOT, '.github', 'workflows', 'r2-fleet-admission.yml'),
]) {
  assert(!credentialPattern.test(readFileSync(path, 'utf8')), `credential-like value in ${path}`);
}

console.log(`R2 fleet admission contract passed: ${tasks.length} tasks, ${organizations.length} organizations.`);

#!/usr/bin/env node

if (process.argv.includes('--help') || process.argv.includes('-h')) {
  process.stdout.write('Usage: cli-portability-fixture [--help]\n');
  process.exit(0);
}

process.stdout.write('cli-portability-fixture\n');

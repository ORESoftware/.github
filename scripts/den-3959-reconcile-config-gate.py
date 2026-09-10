#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

FLEET = Path('.github/workflows/ores-config-contract-fleet.yml')
SELFTEST = Path('.github/workflows/ores-config-contract-fleet-selftest.yml')
OLD_RPC = '802d655357ec4d4b3bb8ec07acb9250bc033b17c'
RPC_REV = '12127a82ff1c0c34096faaf6df1a2a8484ea2feb'
RPC_TJSV = 'd60d0d79d83e075077382623ec9e23a401ab601f'
GENERIC_TJSV = 'a4b731fbf82c4d162abd74fd03758fa32bb76176'


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected one anchor, found {count}')
    return text.replace(old, new, 1)


def reconcile_fleet(text: str) -> str:
    if OLD_RPC not in text:
        raise SystemExit('superseded RPC revision not present in fleet workflow')
    text = text.replace(OLD_RPC, RPC_REV)

    env_anchor = f'      TJSV_REVISION: {GENERIC_TJSV}\n'
    if f'      RPC_TJSV_REVISION: {RPC_TJSV}\n' not in text:
        text = once(text, env_anchor, env_anchor + f'      RPC_TJSV_REVISION: {RPC_TJSV}\n', 'rpc TJSV env')

    dict_anchor = f"            'tjsv': ('ORESoftware/typespec-json-schema-validator', '{GENERIC_TJSV}'),\n"
    rpc_dict = f"            'rpcTjsv': ('ORESoftware/typespec-json-schema-validator', '{RPC_TJSV}'),\n"
    if rpc_dict not in text:
        text = once(text, dict_anchor, dict_anchor + rpc_dict, 'rpc TJSV authority')

    start = text.index('          def validate_rpc(doc, root):\n')
    end = text.index('          def validate_fanwaave(doc, root):\n', start)
    replacement = '''          def validate_rpc(doc, root):
            # Deep RPC semantics are delegated to the merged api-docs loader.
            # This local check exists only for cross-family role/mode convergence.
            req(doc.get('schemaVersion') == 'ores.rpc.config.v1', 'rpc: schemaVersion invalid')
            req(doc.get('strict') is True, 'rpc: strict=true required')
            mode = {'client-only':'client','server-only':'server','hybrid':'hybrid'}.get(doc.get('repositoryMode'))
            req(mode is not None, 'rpc: repositoryMode invalid')
            targets = doc.get('targets')
            req(isinstance(targets, list) and targets, 'rpc: targets required')
            roles = {t.get('role') for t in targets if isinstance(t, dict)}
            expected_roles = {'client','server'} if mode == 'hybrid' else {mode}
            req(roles == expected_roles, f'rpc: repository role mismatch: {sorted(roles)}')
            return mode

'''
    text = text[:start] + replacement + text[end:]

    checkout_anchor = '      - name: Check out immutable flags-2-env\n'
    rpc_checkout = f'''      - name: Check out RPC-certified TJSV revision
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
        with:
          repository: ORESoftware/typespec-json-schema-validator
          ref: {RPC_TJSV}
          path: .authority/tjsv-rpc
          persist-credentials: false
          fetch-depth: 1
          show-progress: false

'''
    if '.authority/tjsv-rpc' not in text:
        text = once(text, checkout_anchor, rpc_checkout + checkout_anchor, 'rpc TJSV checkout')

    install_anchor = '          npm ci --prefix .authority/tjsv --no-audit --no-fund\n'
    rpc_install = '          npm ci --prefix .authority/tjsv-rpc --no-audit --no-fund\n'
    if rpc_install not in text:
        text = once(text, install_anchor, install_anchor + rpc_install, 'rpc TJSV install')

    validate_anchor = '      - name: Validate authority lock, role projections, env-name boundaries, and mode convergence\n'
    rpc_semantic = '''      - name: Validate RPC through merged api-docs semantic loader
        if: ${{ hashFiles('.ores-rpc.toml') != '' }}
        shell: bash
        run: |
          set -euo pipefail
          python3 .authority/rpc/scripts/ores_rpc_config.py --manifest .ores-rpc.toml --repo-root . check

'''
    if 'Validate RPC through merged api-docs semantic loader' not in text:
        text = once(text, validate_anchor, rpc_semantic + validate_anchor, 'rpc semantic loader step')

    rpc_step_start = text.index('      - name: Normalize and re-admit RPC consumer through TJSV\n')
    rpc_step_end = text.index('      - name: Record exact authority revisions\n', rpc_step_start)
    rpc_step = '''      - name: Normalize and re-admit RPC consumer through certified TJSV
        if: ${{ hashFiles('.ores-rpc.toml') != '' }}
        shell: bash
        run: |
          set -euo pipefail
          mkdir -p target/rpc-instances/OresRpcConfigV1/valid
          python3 .authority/rpc/scripts/ores_rpc_config.py \\
            --manifest .ores-rpc.toml --repo-root . normalize \\
            > target/rpc-instances/OresRpcConfigV1/valid/repo.json
          node .authority/tjsv-rpc/bin/typespec-json-schema-validator.mjs check \\
            --typespec=.authority/rpc/contracts/ores-rpc-config/typespec/main.tsp \\
            --schema=.authority/rpc/contracts/ores-rpc-config/json-schema/ores-rpc-config.schema.json \\
            --mapping=.authority/rpc/contracts/ores-rpc-config/tjsv.mapping.json \\
            --instances=target/rpc-instances \\
            --report=target/ores-config/rpc-report.json \\
            --sarif=target/ores-config/rpc-report.sarif \\
            --contract-ir=target/ores-config/rpc-ir.json \\
            --output-dir=target/ores-config/rpc-generated \\
            --int64-strategy=number --seal-object-schemas=true --polymorphic-models-strategy=oneOf

'''
    text = text[:rpc_step_start] + rpc_step + text[rpc_step_end:]

    record_anchor = '          git -C .authority/tjsv rev-parse HEAD > target/ores-config/tjsv-revision.txt\n'
    record_rpc = '          git -C .authority/tjsv-rpc rev-parse HEAD > target/ores-config/rpc-tjsv-revision.txt\n'
    if record_rpc not in text:
        text = once(text, record_anchor, record_anchor + record_rpc, 'rpc TJSV evidence')

    return text


def reconcile_selftest(text: str) -> str:
    text = text.replace(OLD_RPC, RPC_REV)
    fixture_anchor = f"            'tjsv': ('ORESoftware/typespec-json-schema-validator', '{GENERIC_TJSV}'),\n"
    fixture_rpc = f"            'rpcTjsv': ('ORESoftware/typespec-json-schema-validator', '{RPC_TJSV}'),\n"
    if fixture_rpc not in text:
        text = once(text, fixture_anchor, fixture_anchor + fixture_rpc, 'selftest rpc TJSV authority')
    return text


def assert_result(fleet: str, selftest: str) -> None:
    required = [
        RPC_REV,
        RPC_TJSV,
        '.authority/rpc/scripts/ores_rpc_config.py',
        'contracts/ores-rpc-config/typespec/main.tsp',
        'contracts/ores-rpc-config/json-schema/ores-rpc-config.schema.json',
        'contracts/ores-rpc-config/tjsv.mapping.json',
        '.authority/tjsv-rpc',
        "schemaVersion') == 'ores.rpc.config.v1'",
        "repositoryMode'))",
    ]
    missing = [item for item in required if item not in fleet]
    if missing:
        raise SystemExit(f'missing canonical RPC gate elements: {missing}')
    if OLD_RPC in fleet + selftest:
        raise SystemExit('superseded RPC candidate revision survived reconciliation')
    if "doc.get('schema_version')" in fleet or "doc.get('mode')" in fleet:
        raise SystemExit('superseded #81 RPC dialect survived reusable gate')


def main() -> None:
    fleet = reconcile_fleet(FLEET.read_text())
    selftest = reconcile_selftest(SELFTEST.read_text())
    assert_result(fleet, selftest)
    FLEET.write_text(fleet)
    SELFTEST.write_text(selftest)
    print('canonical merged RPC closure reconciled into reusable fleet gate')


if __name__ == '__main__':
    main()

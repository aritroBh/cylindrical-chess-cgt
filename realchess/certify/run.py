"""Run an existing realchess stage with this workstream's prober, ledger,
knowledge base and results directory (see infra.py). The realchess code is
imported read-only and patched at module level only.

    PYTHONPATH=. .venv/bin/python -m realchess.certify.run solve_candidate resolve --component ... \
        --fen "<FEN>" --cap 1200 --max-new 5 --per-target 5 --ext 0
    PYTHONPATH=. .venv/bin/python -m realchess.certify.run verify_proof "<FEN>" --claim win --kb

The ledger is forced to realchess/certify/logs/ledger.jsonl.
"""
from __future__ import annotations

import sys

from . import infra


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    name, rest = sys.argv[1], sys.argv[2:]
    if "--ledger" in rest:
        i = rest.index("--ledger")
        if rest[i + 1] != infra.LEDGER:
            raise SystemExit(f"--ledger must be {infra.LEDGER}")
    elif name == "solve_candidate":
        rest += ["--ledger", infra.LEDGER]
    infra.patch_realchess()
    mod = __import__(f"realchess.{name}", fromlist=["main"])
    if hasattr(mod, "Prober"):
        mod.Prober = infra.CertProber
    sys.argv = [f"realchess.{name}"] + rest
    sys.setrecursionlimit(100000)
    if name == "solve_candidate":
        mod.main(rest)
    else:
        mod.main()


if __name__ == "__main__":
    main()

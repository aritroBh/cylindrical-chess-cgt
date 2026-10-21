#!/bin/sh
# Build (a) the UNPATCHED vendored sf_19 source and (b) my instrumented copy (patched, no ABL flag,
# fprintf logging at Step 10 entry and at the Step 15 guard). Fake git on PATH.
set -e
V=$(cd "$(dirname "$0")" && pwd)
export PATH="$V/fakebin:$PATH"
(cd "$V/unpatched/src" && make -j6 all ARCH=apple-silicon > "$V/build_unpatched.log" 2>&1 && mv stockfish "$V/sf/bin/sf_unpatched")
(cd "$V/instr/src" && make -j6 all ARCH=apple-silicon > "$V/build_instr.log" 2>&1 && mv stockfish "$V/sf/bin/sf_instr")
ls -la "$V/sf/bin"

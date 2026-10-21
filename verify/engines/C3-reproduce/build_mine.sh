#!/bin/sh
# Rebuild selected ablation variants from a fresh copy of the vendored sf_19 source + worker's patch,
# into verify/engines/C3-reproduce/sf/bin. A fake `git` (exit 1) is put first on PATH so the Makefile's
# git calls never touch any repository (release build: git info is not compiled in anyway).
set -e
V=$(cd "$(dirname "$0")" && pwd)
export PATH="$V/fakebin:$PATH"
for v in "$@"; do
  flag=""; [ "$v" != base ] && flag="-DABL_$v"
  echo "== building $v ($flag)"
  (cd "$V/sf/src" && make objclean >/dev/null && make -j6 all ARCH=apple-silicon EXTRACXXFLAGS="$flag" > "$V/build_$v.log" 2>&1 && mv stockfish "$V/sf/bin/sf_$v")
  ls -la "$V/sf/bin/sf_$v"
done

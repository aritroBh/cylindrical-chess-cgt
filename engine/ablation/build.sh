#!/bin/sh
# Build Stockfish 19 (tag sf_19, commit edb0d9db) with one search heuristic switched off at a time.
# Needs the sf_19 source and its network in engine/vendor/Stockfish/src (git-ignored; built there earlier).
# Nothing is downloaded: the `all` target is used, never `build`/`net`.
# Run from the project root:  sh engine/ablation/build.sh [variant ...]
set -e
root=$(pwd)
src=engine/vendor/sf19_ablate/src
out=engine/vendor/sf19_ablate/bin
if [ ! -d "$src" ]; then
  mkdir -p engine/vendor/sf19_ablate
  rsync -a --exclude '*.o' --exclude stockfish --exclude .depend engine/vendor/Stockfish/src/ "$src/"
  rsync -a engine/vendor/Stockfish/scripts/ engine/vendor/sf19_ablate/scripts/
  (cd engine/vendor/sf19_ablate && patch -p1 < "$root/engine/ablation/sf19_ablate.patch")
fi
mkdir -p "$out"
variants=${*:-"base NMP SHALLOW RFP RAZOR SE PROBCUT LMR CORR IIR"}
for v in $variants; do
  flag=""
  [ "$v" != base ] && flag="-DABL_$v"
  echo "== building $v ($flag)"
  (cd "$src" && make objclean >/dev/null && make -j14 all ARCH=apple-silicon EXTRACXXFLAGS="$flag" >/dev/null 2>&1 && mv stockfish "$root/$out/sf_$v")
  ls -la "$out/sf_$v"
done

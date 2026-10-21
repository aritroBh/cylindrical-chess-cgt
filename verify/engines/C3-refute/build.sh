#!/bin/sh
# Verifier build for claim C3. Run from the project root:  sh verify/engines/C3-refute/build.sh
# Copies the pristine sf_19 source (blob of search.cpp checked against the sf_19 tree), symlinks the net,
# applies the verifier's own #ifdef edits (make_src.py), and builds 4 binaries with `make all` (no download).
set -e
root=$(pwd)
v=verify/engines/C3-refute
src=$v/sf/src
out=$v/bin
rm -rf "$v/sf"
mkdir -p "$src" "$out"
rsync -a --exclude '*.o' --exclude stockfish --exclude '*.nnue' --exclude .depend engine/vendor/Stockfish/src/ "$src/"
ln -s "$root/engine/vendor/Stockfish/src/nn-1a298aa575a0.nnue" "$src/nn-1a298aa575a0.nnue"
python3 "$v/make_src.py" "$src/search.cpp"
for pair in base: nonmp:-DMY_NONMP nos15:-DMY_NOS15 count:-DMY_COUNT; do
  name=${pair%%:*}; flag=${pair#*:}
  echo "== $name ($flag)"
  (cd "$src" && make objclean >/dev/null && make -j12 all ARCH=apple-silicon EXTRACXXFLAGS="$flag" >"$root/$out/build_$name.log" 2>&1 && mv stockfish "$root/$out/my_$name")
  ls -la "$out/my_$name"
done

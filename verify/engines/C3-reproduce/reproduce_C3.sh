#!/bin/sh
# Reproduce the C3 verification. Run from the project root. Writes only under verify/engines/C3-reproduce/.
set -e
V=verify/engines/C3-reproduce
# 1. Fresh copy of vendored sf_19 source + worker's patch (setup was done once by hand):
#    rsync -a --exclude '*.o' --exclude stockfish --exclude .depend engine/vendor/Stockfish/src/ $V/sf/src/
#    rsync -a engine/vendor/Stockfish/scripts/ $V/sf/scripts/ ; (cd $V/sf && patch -p1 < ../../../../engine/ablation/sf19_ablate.patch)
sh $V/build_mine.sh base NMP SHALLOW        # -> $V/sf/bin/sf_{base,NMP,SHALLOW}; md5 == worker's binaries
sh $V/build_extra.sh                        # -> sf_unpatched (md5 == sf_base == vendor), sf_instr (logging)
$V/sf/bin/sf_base bench 16 1 13 2>&1 | grep "Nodes searched"     # 2497913
for v in base NMP SHALLOW; do .venv/bin/python $V/run_ablation_redirect.py --depth 16 --timeout 300 --bin "$v=$V/sf/bin/sf_$v"; done
.venv/bin/python $V/analyze_redirect.py > $V/analyze_my_results.txt
for v in base NMP SHALLOW; do .venv/bin/python $V/raw_runner.py $v $V/sf/bin/sf_$v 16; done
.venv/bin/python $V/compare_raw.py
.venv/bin/python $V/instr_runner.py 6      # earliest iteration at which NMP / Step 15 is entered, per position

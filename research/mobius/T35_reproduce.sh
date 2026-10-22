#!/bin/sh
# T35 reproduce commands, run from the project root:  sh research/mobius/T35_reproduce.sh
# Heavy steps: the pawn enumerations (width 3 and width 4, about 10 and 20 minutes). Run them one at a time
# with nice, as the machine rules require. Everything else takes under a minute.
set -e
P=research/mobius
PY=.venv/bin/python

# --- T9 smallest reproduce command: 4-man KQK on the Mobius strip (expect 99,013 legal, 100%, max DTM 5)
cc -O2 -pthread $P/mobius_replica.c -o $P/mobius_replica_T35
(cd $P && ./mobius_replica_T35 mobius Q)

# --- KPK, 8x8 Mobius board, cylinder and flat controls (kings/kpsolve.c patched: step() for WRAP==2)
cc -O2 -Wall -Wextra -pthread $P/kpsolve_mob.c -o $P/kpsolve_mob
for B in cyl flat mob; do
  $PY $P/gen_kpk_positions.py --board ${B}:8x8 > $P/kpk_${B}8x8_positions.txt
done
$P/kpsolve_mob --board mob:8x8 --ep on --promote QRBN --cap 1 < $P/kpk_mob8x8_positions.txt > $P/kpk_mob8x8_results.txt
# controls: the unpatched solver on the cylinder and flat lists (the patch must not change them)
cc -O2 -Wall -Wextra -pthread kings/kpsolve.c -o $P/kpsolve_orig
$P/kpsolve_orig --board cyl:8x8 --ep on --promote QRBN --cap 1 < $P/kpk_cyl8x8_positions.txt > $P/kpk_cyl8x8_results_orig.txt
$P/kpsolve_orig --board flat:8x8 --ep on --promote QRBN --cap 1 < $P/kpk_flat8x8_positions.txt > $P/kpk_flat8x8_results_orig.txt
$PY $P/analyse_kpk_mob.py $P/kpk_cyl8x8_results_orig.txt --label cylinder
$PY $P/analyse_kpk_mob.py $P/kpk_flat8x8_results_orig.txt --label flat
$PY $P/analyse_kpk_mob.py $P/kpk_mob8x8_results.txt --label mobius
$PY $P/compare_kpk_boards.py $P/kpk_cyl8x8_results_orig.txt $P/kpk_mob8x8_results.txt

# --- independent second implementation (CHECKED-2): patched Python reference solver
PYTHONPATH=. $PY -m research.mobius.ref_mob_solve --board mob:8x8 --ep on --promote QRBN --cap 1 \
  < $P/kpk_mob8x8_positions.txt > $P/kpk_mob8x8_results_pyref.txt
PYTHONPATH=. $PY -m research.mobius.ref_mob_solve --board cyl:8x8 --ep on --promote QRBN --cap 1 \
  < $P/kpk_cyl8x8_positions.txt > $P/kpk_cyl8x8_results_pyref.txt
cmp $P/kpk_mob8x8_results.txt $P/kpk_mob8x8_results_pyref.txt && echo "mobius C = Python: identical"
cmp $P/kpk_cyl8x8_results_orig.txt $P/kpk_cyl8x8_results_pyref.txt && echo "cylinder C = Python: identical"

# --- pawn-only values (T35 part B): width 3 and width 4, up to 4 pawns
PYTHONPATH=. nice -n 10 $PY $P/check_mob_pawns.py 3 3
PYTHONPATH=. nice -n 10 $PY $P/check_mob_symmetry.py 3 3
PYTHONPATH=. nice -n 10 $PY $P/pawn_values_mobius.py 3 4 $P/pawn_w3_p4c
PYTHONPATH=. nice -n 10 $PY $P/pawn_values_mobius.py 4 4 $P/pawn_w4_p4c

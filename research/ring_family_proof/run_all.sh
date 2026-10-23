#!/bin/sh
# Reproduce every check of T50 (research/ring_family_proof).  Run from the project root:
#   sh research/ring_family_proof/run_all.sh [quick|slow]
# 'quick' (default; about 20 minutes on the loaded shared machine): engine build, differential tests, lemma checks, pumping checks, sweeps.
# 'slow'  (about 25 minutes): value-level test against cylcgt, whole-board cylcgt on family members (n <= 10).
D=research/ring_family_proof
L=$D/logs
mkdir -p $L
PY=.venv/bin/python
export PYTHONPATH=.
cc -O2 -DMAXN=64 -o $D/rg $D/rg.c 2>/dev/null
if [ "${1:-quick}" = quick ]; then
  nice -n 15 $PY $D/difftest.py 20000 1 > $L/difftest_seed1.log
  nice -n 15 $PY $D/difftest.py 20000 2 > $L/difftest_seed2.log
  nice -n 15 $PY $D/difftest.py 20000 3 > $L/difftest_seed3.log
  nice -n 15 $PY $D/locality_test.py 20000 2 > $L/locality.log
  nice -n 15 $PY $D/lemmaR_test.py 30000 4 > $L/lemmaR.log
  nice -n 15 $PY $D/lemma4_test.py > $L/lemma4.log
  nice -n 15 $PY $D/lemma2_test.py > $L/lemma2.log
  for f in odd even F; do nice -n 15 $PY $D/lemmaL_test.py $f 100000 11 5 > $L/lemmaL_$f.log; done
  : > $L/lemmaL_sensitivity.log
  for r in 1 2 3; do nice -n 15 $PY $D/lemmaL_test.py odd 30000 11 $r | tail -1 >> $L/lemmaL_sensitivity.log; done
  MUTATE=1 nice -n 15 $PY $D/lemmaL_test.py odd 30000 11 5 | tail -1 >> $L/lemmaL_sensitivity.log
  nice -n 15 $PY $D/lemmaL_nodes.py odd 17 35 > $L/lemmaL_nodes_odd.log
  nice -n 15 $PY $D/lemmaL_nodes.py even 16 34 > $L/lemmaL_nodes_even.log
  nice -n 15 $PY $D/lemmaL_nodes.py Fodd 19 33 > $L/lemmaL_nodes_Fodd.log
  nice -n 15 $PY $D/lemmaL_nodes.py Feven 18 34 > $L/lemmaL_nodes_Feven.log
  nice -n 15 $PY $D/lemma1_family.py > $L/lemma1_family.log
  nice -n 15 $PY $D/fullsweep.py 61 > $L/fullsweep.log
  nice -n 15 $PY $D/reduced_cyl.py odd 5 7 9 11 13 15 17 19 21 23 > $L/reduced_cyl_odd.log
  nice -n 15 $PY $D/reduced_cyl.py even 6 8 10 12 14 16 18 20 22 > $L/reduced_cyl_even.log
  nice -n 15 $PY $D/reduced_value.py odd 5 7 9 11 13 15 17 19 21 23 25 > $L/reduced_value.log
  nice -n 15 $PY $D/reduced_value.py even 6 8 10 12 14 16 18 20 22 24 26 >> $L/reduced_value.log
  nice -n 15 $PY $D/reduced_value.py F 5 7 8 9 10 11 12 >> $L/reduced_value.log
  FIXC=9 nice -n 15 $PY $D/pump_verify.py odd 9 61 > $L/pump_odd_c9.log
  FIXC=8 nice -n 15 $PY $D/pump_verify.py even 8 60 > $L/pump_even_c8.log
  FIXC=6 nice -n 15 $PY $D/pump_verify.py Fodd 15 61 > $L/pump_Fodd_c6.log
  FIXC=4 nice -n 15 $PY $D/pump_verify.py Feven 8 60 > $L/pump_Feven_c4.log
else
  nice -n 15 $PY $D/difftest_solve.py 1500 21 > $L/difftest_solve.log
  nice -n 15 $PY $D/cyl_whole.py odd 5 7 9 > $L/cyl_whole_odd.log
  nice -n 15 $PY $D/cyl_whole.py even 6 8 10 > $L/cyl_whole_even.log
fi

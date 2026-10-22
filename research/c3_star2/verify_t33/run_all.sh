#!/bin/sh
# Verifier T33: reproduce every number in VERIFY_T33.md.  Run from anywhere; light compute (< 1 minute total).
cd "$(dirname "$0")" || exit 1
PY=../../../.venv/bin/python
for s in run_settings walk_checks_c3 walk_omitted walk_omitted2 walk_checks_c4 reach_mine ep_pos ep_select ep_subsets ep_lines ep_select_c4 c4_epoff_k16 ep_ablate_cylcgt xcheck_resolve; do
  echo "### $s"
  if [ "$s" = "ep_select" ]; then
    nice -n 10 $PY $s.py aware > $s.out 2>&1; nice -n 10 $PY $s.py textbook >> $s.out 2>&1
  else
    nice -n 10 $PY $s.py > $s.out 2>&1
  fi
done

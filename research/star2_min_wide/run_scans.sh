#!/bin/bash
# run_scans.sh WIDTH P [NW ...]   -- scan flat width WIDTH with P pawns, every white/black split (or only the given NW),
# default setting (count, e.p. on, e.p.-aware = --only-setting 2), scanner = scan_fixed2 (= frontier_split1_fixed2.c).
# Outputs scan/w{W}p{P}_{NW}_{NB}.{summary,hits.tsv,log}.  Raw TSV is not kept (too big); the per-row histogram and every nimber>=2 row are.
set -u
cd "$(dirname "$0")"; mkdir -p scan
W=$1; P=$2; shift 2
SPLITS="$@"; [ -z "$SPLITS" ] && SPLITS=$(seq 1 $((P-1)))
for NW in $SPLITS; do
  NB=$((P-NW)); T=scan/w${W}p${P}_${NW}_${NB}
  [ -f $T.summary ] && continue
  s=$(date +%s)
  nice -n 15 ./scan_fixed2 --flat --width $W --min $P --max $P --nw $NW --nb $NB --only-setting 2 --max-entries 67108864 2> $T.log \
    | python3 -I filt.py $T
  echo "elapsed_s $(( $(date +%s) - s ))" >> $T.log
done

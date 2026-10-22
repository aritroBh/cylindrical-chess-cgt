#!/bin/bash
# scan.sh W NW NB MODE [BIN] [ONLY] [CHUNK_I CHUNK_N] [PROGRESS]
#
# Runs one frontier_split scan on the cylinder of width W with the given
# (nw, nb) pawn split and the given total pawn count p = nw+nb.
# MODE=pilot samples 2000 roots (--pilot 2000) to project the full cost.
# MODE=full scans every root.
# BIN   = frontier_split (default, all nine settings) or frontier_split1
# ONLY  = setting index 0..8 for BIN=frontier_split1 (2 = count/epon/aware,
#         the default setting); ignored for the nine-setting binary.
# CHUNK_I/CHUNK_N = split the white-combination space into N chunks and keep
#         chunk I; the chunks partition the root set exactly.
# PROGRESS = print a progress line every PROGRESS roots (0 = off).
#
# Outputs (in this directory):
#   cyl_w<W>_p<P>_<NW>_<NB>[_sK][_cIofN].log          stderr of the scanner + elapsed time
#   cyl_w<W>_p<P>_<NW>_<NB>[_sK][_cIofN].hits.tsv     only rows with nimber >= 2
#   cyl_w<W>_p<P>_<NW>_<NB>[_sK][_cIofN].summary.txt  per-split counts
set -u
W=$1; NW=$2; NB=$3; MODE=${4:-full}; BIN=${5:-frontier_split}; ONLY=${6:-2}
CH_I=${7:-0}; CH_N=${8:-1}; PROG=${9:-0}
P=$((NW+NB))
D="$(cd "$(dirname "$0")" && pwd)"
cd "$D" || exit 1
TAG="cyl_w${W}_p${P}_${NW}_${NB}"
PILOT=""
if [ "$MODE" = "pilot" ]; then PILOT="--pilot 2000"; TAG="${TAG}_pilot"; fi
EXTRA=""
if [ "$BIN" = "frontier_split1" ]; then
    EXTRA="--only-setting $ONLY"
    TAG="${TAG}_s${ONLY}"
    if [ "$CH_N" -gt 1 ]; then EXTRA="$EXTRA --chunk $CH_I $CH_N"; TAG="${TAG}_c${CH_I}of${CH_N}"; fi
    if [ "$PROG" -gt 0 ]; then EXTRA="$EXTRA --progress $PROG"; fi
fi
start=$(date +%s)
nice -n 10 ./"$BIN" --cylinder --width "$W" --min "$P" --max "$P" \
    --nw "$NW" --nb "$NB" $PILOT $EXTRA 2> "${TAG}.log" \
  | awk -v sumfile="${TAG}.summary.txt" -f filter.awk > "${TAG}.hits.tsv"
end=$(date +%s)
echo "elapsed_s $((end-start))" >> "${TAG}.log"
echo "done $TAG elapsed=$((end-start))s"

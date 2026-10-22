#!/bin/bash
# run_chunks.sh TAG NCHUNKS PARALLEL "s3 args without --chunk"   e.g.
#   ./run_chunks.sh flat_w5_p9_4_5 24 2 "--flat --width 5 --nw 4 --nb 5 --single"
# optional 5th/6th args: first and last chunk index (default all).  chunk I of N splits the white combinations; results go to scans/TAG/cIofN.{tsv,err}; skip finished chunks.
cd "$(dirname "$0")"
TAG=$1; N=$2; P=$3; ARGS=$4; START=${5:-0}; END=${6:-$((N-1))}
mkdir -p scans/$TAG
run_one() {
  tag=$1; n=$2; i=$3; args=$4
  out=scans/$tag/c${i}of${n}.tsv
  if [ -f $out ] && grep -q '^#summary' $out; then return; fi
  nice -n 15 ./s3 $args --chunk $i $n --max-entries 33554432 > $out.part 2> scans/$tag/c${i}of${n}.err && mv $out.part $out
}
export -f run_one
seq $START $END | xargs -P $P -I{} bash -c 'run_one "$0" "$1" "$2" "$3"' "$TAG" "$N" {} "$ARGS"
echo "ALL DONE $TAG"

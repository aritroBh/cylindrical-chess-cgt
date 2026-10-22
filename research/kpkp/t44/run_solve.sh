#!/bin/bash
# Re-solve every legal KPKP position on one 8x8 board with kings/kpsolve, in 4 chunks (each input < 100 MB,
# streamed, never written uncompressed).  usage: run_solve.sh cyl|flat   (run from the project root)
set -o pipefail
B=$1
OUT=research/kpkp/t44
for i in 0 1 2 3; do
  if [ -s $OUT/kpkp_${B}_$i.out.zst ]; then echo "skip $B $i"; continue; fi
  nice -n 15 $OUT/enum_kpkp $B $i 4 2> $OUT/kpkp_${B}_$i.enum.err \
   | nice -n 15 kings/kpsolve --board $B:8x8 --ep on --promote QRBN --cap 1 2> $OUT/kpkp_${B}_$i.err \
   | zstd -q -3 -o $OUT/kpkp_${B}_$i.out.zst.part && mv $OUT/kpkp_${B}_$i.out.zst.part $OUT/kpkp_${B}_$i.out.zst
  echo "done $B $i rc=$?"
done

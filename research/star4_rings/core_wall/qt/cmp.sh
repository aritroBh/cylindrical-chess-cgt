#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/star4_rings/core_wall
for cfg in "3 5 4 0" "3 5 5 0" "3 5 5 1"; do set -- $cfg; ./gen $cfg | QUIET=1 ./rgq solveq 7 | grep -E "^#H" | sort > qt/pipe_$1_$2_$3_$4.h; grep -E "^#H" qt/t_$1_$2_$3_$4.res | sort > qt/cwq_$1_$2_$3_$4.h; if cmp -s qt/pipe_$1_$2_$3_$4.h qt/cwq_$1_$2_$3_$4.h; then echo "same $cfg"; else echo "DIFF $cfg"; fi; done
grep -E "^#" qt/t_5_9_4_s.res | head -20; grep HIT qt/t_5_9_4_s.res | head

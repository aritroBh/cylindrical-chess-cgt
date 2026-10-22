#!/bin/bash
# second queue (after cyl_w5_p9_4_5): completes width 5 / 9 pawns, then 10-pawn narrow boards, then width 6
cd "$(dirname "$0")"
while pgrep -f "run_chunks.sh cyl_w5_p9_4_5" >/dev/null; do sleep 5; done
runq() { P=$(cat tmp/P 2>/dev/null || echo 1); ./run_chunks.sh "$1" "$2" "$P" "$3"; }
runq flat_w5_p9_3_6 24 "--flat --width 5 --nw 3 --nb 6 --single"
runq flat_w5_p9_2_7 8 "--flat --width 5 --nw 2 --nb 7 --single"
runq flat_w5_p9_1_8 1 "--flat --width 5 --nw 1 --nb 8 --single"
runq cyl_w4_p9_4_5 12 "--cylinder --width 4 --nw 4 --nb 5 --single"
runq flat_w4_p10_5_5 24 "--flat --width 4 --nw 5 --nb 5 --single --colsym"
runq flat_w4_p10_4_6 24 "--flat --width 4 --nw 4 --nb 6 --single"
runq cyl_w4_p10_5_5 12 "--cylinder --width 4 --nw 5 --nb 5 --single --colsym"
runq flat_w6_p9_4_5 96 "--flat --width 6 --nw 4 --nb 5 --single"
echo QUEUE3 DONE

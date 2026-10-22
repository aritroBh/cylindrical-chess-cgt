#!/bin/bash
# third queue: remaining 9-pawn splits on width 6/7, then 10-pawn ring C5 and width 5
cd "$(dirname "$0")"
runq() { P=$(cat tmp/P 2>/dev/null || echo 1); ./run_chunks.sh "$1" "$2" "$P" "$3"; }
runq flat_w6_p9_2_7 8 "--flat --width 6 --nw 2 --nb 7 --single"
runq flat_w6_p9_3_6 48 "--flat --width 6 --nw 3 --nb 6 --single"
runq flat_w7_p9_3_6 32 "--flat --width 7 --nw 3 --nb 6 --single"
runq flat_w7_p9_4_5 128 "--flat --width 7 --nw 4 --nb 5 --single"
runq cyl_w5_p10_5_5 48 "--cylinder --width 5 --nw 5 --nb 5 --single --colsym"
runq flat_w5_p10_5_5 96 "--flat --width 5 --nw 5 --nb 5 --single --colsym"
echo QUEUE4 DONE

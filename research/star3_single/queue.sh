#!/bin/bash
# sequential queue of exhaustive single-component scans; parallelism read from tmp/P before each scan
cd "$(dirname "$0")"
while pgrep -f "run_chunks.sh flat_w5_p9_4_5 48 1" >/dev/null; do sleep 5; done
runq() { P=$(cat tmp/P 2>/dev/null || echo 1); ./run_chunks.sh "$1" "$2" "$P" "$3"; }
runq flat_w5_p9_4_5 48 "--flat --width 5 --nw 4 --nb 5 --single"
runq cyl_w5_p9_4_5 24 "--cylinder --width 5 --nw 4 --nb 5 --single"
runq flat_w4_p10_5_5 24 "--flat --width 4 --nw 5 --nb 5 --single --colsym"
runq flat_w4_p10_4_6 48 "--flat --width 4 --nw 4 --nb 6 --single"
runq flat_w6_p9_4_5 96 "--flat --width 6 --nw 4 --nb 5 --single"
runq cyl_w4_p9_4_5 24 "--cylinder --width 4 --nw 4 --nb 5 --single"
runq cyl_w4_p10_5_5 24 "--cylinder --width 4 --nw 5 --nb 5 --single --colsym"
runq cyl_w6_p10_5_5 96 "--cylinder --width 6 --nw 5 --nb 5 --single --colsym"
echo QUEUE DONE

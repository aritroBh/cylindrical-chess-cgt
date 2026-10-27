#!/bin/zsh
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K22
until grep -q ALLDONE $D/logs/scan_B.txt && grep -q ALLDONE $D/logs/scan_C.txt && grep -q ALLDONE $D/logs/strategy_check.txt && grep -q ALLDONE $D/logs/compare_log.txt; do sleep 20; done
echo finished

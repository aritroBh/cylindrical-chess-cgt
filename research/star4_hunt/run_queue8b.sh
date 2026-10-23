#!/bin/bash
# dense scans, finer chunks, flat w4 first (partial coverage accumulates chunk by chunk)
cd "$(dirname "$0")"
source ./scanlib.sh
scan w4p11 flat 4 3 8 8
scan w4p11 flat 4 4 7 32
scan w4p11 flat 4 5 6 48
scan c4p11 cylinder 4 3 8 8
scan c4p11 cylinder 4 4 7 32
scan c4p11 cylinder 4 5 6 48
echo ALLDONE > logs/queue8.done

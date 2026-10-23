#!/bin/bash
cd "$(dirname "$0")"
source ./scanlib.sh
while [ ! -f logs/scan_w5p10.done ]; do sleep 20; done
scan w6p10 flat 6 4 6 48
scan w6p10 flat 6 3 7 16
echo ALLDONE > logs/queue1.done

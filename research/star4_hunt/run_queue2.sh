#!/bin/bash
cd "$(dirname "$0")"
source ./scanlib.sh
while [ ! -f logs/queue4.done ]; do sleep 20; done
scan w4p11 flat 4 3 8 4
scan w4p11 flat 4 4 7 8
scan w4p11 flat 4 5 6 12
scan w4p12 flat 4 4 8 8
scan w4p12 flat 4 5 7 16
scan w4p12 flat 4 6 6 12 --colsym
echo ALLDONE > logs/queue2.done

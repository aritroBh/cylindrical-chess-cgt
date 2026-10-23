#!/bin/bash
cd "$(dirname "$0")"
source ./scanlib.sh
while [ ! -f logs/queue12.done ]; do sleep 15; done
scan w4p12 flat 4 4 8 16
scan w4p12 flat 4 5 7 48
scan w4p12 flat 4 6 6 48 --colsym
echo ALLDONE > logs/queue13.done

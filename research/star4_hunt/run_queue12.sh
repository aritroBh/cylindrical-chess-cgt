#!/bin/bash
cd "$(dirname "$0")"
source ./scanlib.sh
while [ ! -f logs/queue9.done ]; do sleep 15; done
scan w4p11 flat 4 4 7 32
scan w4p11 flat 4 5 6 48
echo ALLDONE > logs/queue12.done

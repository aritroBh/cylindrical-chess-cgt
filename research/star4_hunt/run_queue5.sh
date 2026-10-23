#!/bin/bash
# exhaustive cylinder C6, 10 pawns, single component (every file occupied); chunked
cd "$(dirname "$0")"
source ./scanlib.sh
scan c6p10 cylinder 6 4 6 64
scan c6p10 cylinder 6 5 5 64 --colsym
scan c6p10 cylinder 6 3 7 16
echo ALLDONE > logs/queue5.done

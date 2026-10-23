#!/bin/bash
# usage: count_roots.sh kind width nw nb
kind=$1; w=$2; nw=$3; nb=$4; cs=""
[ "$nw" -eq "$nb" ] && cs="--colsym"
nice -n 15 ./h4_scan --$kind --width $w --single --nw $nw --nb $nb $cs --count 2>&1 | grep -o "roots=[0-9]*" | head -1

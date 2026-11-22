#!/bin/bash
cd /Users/aritro/Downloads/Research/Chessendgames/research/sum_whole_census
P=../../.venv/bin/python
for t in 1 0; do
 nice -n 15 $P crosscheck.py 2000 $t 20261122 data/cc_uniform_t$t.tsv uniform > logs/cc_uniform_t$t.log 2>&1
 nice -n 15 $P crosscheck.py 1000 $t 777 data/cc_multi_t$t.tsv multi > logs/cc_multi_t$t.log 2>&1
 nice -n 15 $P crosscheck.py 1000 $t 4242 data/cc_dis_t$t.tsv dis > logs/cc_dis_t$t.log 2>&1
done

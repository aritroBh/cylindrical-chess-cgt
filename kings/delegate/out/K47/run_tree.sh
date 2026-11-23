#!/bin/zsh
# K47: proof-aid trees (P values with depth) for the four roots and the two freezes
cd "$(dirname $0)"
./ztree_k47 8 6 roots8.txt q_roots.txt 3 > logs/tree_d3.txt 2> logs/tree.err
grep -v '^#' q_roots.txt | tail -4 > logs/q_only.txt
./ztree_k47 8 6 roots8.txt logs/q_only.txt 40 > logs/tree_q_full.txt 2>> logs/tree.err
echo done > logs/tree.done

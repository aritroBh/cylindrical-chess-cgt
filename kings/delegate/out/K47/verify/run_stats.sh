#!/bin/zsh
cd "$(dirname $0)"
./rzs_k47ref 8 6 roots_ref.txt t0.txt C > /dev/null 2> logs/stats.err

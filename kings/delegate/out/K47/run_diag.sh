#!/bin/zsh
cd "$(dirname $0)"
./za_k47 8 6 roots_diag.txt tests_diag.txt N > logs/diag_A_N.out 2> logs/diag_A_N.err
echo done > logs/diag.done

#!/bin/zsh
# K47 referee item 2: r(Z_O + T) by the referee's own solver rz.cpp, convention N; then principal lines beside *, under, down
cd "$(dirname $0)"
/usr/bin/time -l ./rz_k47ref 8 6 roots_ref.txt tests_ref.txt N > logs/main_N.out 2> logs/main_N.err
/usr/bin/time -l ./rz_k47ref 8 6 roots_ref.txt tstar.txt N pv > logs/pv_star.out 2> logs/pv_star.err
/usr/bin/time -l ./rz_k47ref 8 6 roots_ref.txt tunder.txt N pv > logs/pv_under.out 2> logs/pv_under.err
/usr/bin/time -l ./rz_k47ref 8 6 roots_ref.txt tdown.txt N pv > logs/pv_down.out 2> logs/pv_down.err
echo done > logs/main.done

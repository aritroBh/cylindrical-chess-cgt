#!/bin/zsh
# named games: args per game: name K M n L0 R0 L1 R1 ...
C=./chk
run(){ name=$1; shift; echo "== $name"; nice -n 15 $C graph 3 8 "$@" ; }
run "0" 1 0 0
run "on" 1 1 0
run "off" 1 0 1
run "over {0|over}" 2 2 1 0 0
run "under {under|0}" 2 1 2 0 0
run "* {0|0}" 2 2 2 0 0
run "1 {0|}" 2 2 0 0 0
run "-1 {|0}" 2 0 2 0 0
run "2 {1|}" 3 2 0 4 0 0 0
run "-2 {|-1}" 3 0 2 0 4 0 0
run "1/2 {0|1}" 3 4 2 4 0 0 0
run "up {0|*}" 3 2 4 0 0 2 2
run "down {*|0}" 3 4 2 0 0 2 2
run "+-1 {1|-1}" 4 2 4 8 0 0 8 0 0
run "{on|off}" 3 2 4 2 0 0 4
run "{0|off}" 3 2 4 0 0 0 4
run "{on|0}" 3 2 4 2 0 0 0
run "K21 S_abc" 3 4 6 0 3 6 0

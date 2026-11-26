#!/bin/zsh
# K65: second class of part a, {b,e,f} = files 1,4,5: r48 after the r48 run on {b,c,f}, p45a after the group checks of
# {b,c,f}.  Both through run_search.sh (heavy.sh, time -l, 2.2 GB watchdog).
cd "$(dirname $0)/.."
( until [[ -f logs/search/R88_f1_2_5.done ]]; do sleep 20; done; zsh src/run_search.sh R 1,4,5 ) &
( until [[ -f logs/grp/C125_23_cmp.txt ]]; do sleep 20; done; zsh src/run_search.sh A 1,4,5 ) &
wait

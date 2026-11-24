#!/bin/zsh
# K48 part 1, restricted cap 2 as in K39 (one officer a side): A' = bound A with Black held to one queen (upper bound of the true value),
# B' = bound B with White held to one queen (lower bound). kp39 with the capture refinement. 3 GB watchdog.
cd "$(dirname $0)/.."
B=cyl:8x6; I=in/ZO_cyl_8x6.in
scripts/hrun.sh ZO_c2_Ap 3300 $I bin/kp39 --board $B --ep on --cap 2 --capw 1 --capb 1 --promb Q --bound A --refine --moves
scripts/hrun.sh ZO_c2_Bp 3300 $I bin/kp39 --board $B --ep on --cap 2 --capw 1 --capb 1 --promw Q --bound B --refine --moves
echo done > logs/p1_cap2.done

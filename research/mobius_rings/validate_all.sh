#!/bin/sh
# Re-runs every validation of task 1 with the final binaries (sequential, one worker).
# The full C5 / 8-pawn ring list (2,869,124 rings of enum_rings, all splits) is piped, not stored.
cd "$(dirname "$0")" || exit 1
RG=../c9_rings/rg_copy
for t in cyl3_6 cyl4_7 cyl5_8_sample2000; do
  nice -n 15 $RG solve 3 < val/$t.txt | awk '{print $1}' > val/rg_$t.sig
  nice -n 15 ./mob1 solve --kind 1 < val/$t.txt > val/m1_$t.sig 2>/dev/null
  nice -n 15 ./mob2 solve --kind 1 < val/$t.txt > val/m2_$t.sig 2>/dev/null
  cmp val/rg_$t.sig val/m1_$t.sig && cmp val/rg_$t.sig val/m2_$t.sig && echo "cylinder $t: $(wc -l < val/$t.txt) rings, rg == C1 == C2"
done
for nw in 1 2 3 4 5 6 7; do ../c9_rings/enum_rings 5 8 $nw $((8-nw)) 2>/dev/null; done | nice -n 15 ./mob2 solve --kind 1 > val/m2_cyl5full.sig 2>/dev/null
cmp val/rg_cyl5full.sig val/m2_cyl5full.sig && echo "cylinder C5 8 pawns full: $(wc -l < val/rg_cyl5full.sig) rings, rg == C2 (C1 checked separately)"
nice -n 15 ./mob1 solve --kind 2 < val/partb_pos.txt > val/partb_m1.sig 2>/dev/null
nice -n 15 ./mob2 solve --kind 2 < val/partb_pos.txt > val/partb_m2.sig 2>/dev/null
cmp val/partb_py.sig val/partb_m1.sig && cmp val/partb_py.sig val/partb_m2.sig && echo "Part B: $(wc -l < val/partb_pos.txt) positions, python == C1 == C2"
nice -n 15 python3 symtests.py > val/symtests.log 2>&1
tail -1 val/symtests.log

#!/bin/zsh
# Independent minimality check for C7: every nine-pawn ring, T43's solver with the model's conventions
# (persistent e.p. rights; double-step discount in the race count). One process at a time, nice 15.
cd "${0:A:h}"
for i in {0..511}; do
  [[ -s enum9/c$i.tsv ]] && continue
  nice -n 15 ./c7check_persist_ds --enum $i 512 > enum9/c$i.tsv 2> enum9/c$i.err
done
awk -F'[ =]' '/^chunk/{for(i=1;i<=NF;i++){if($i=="canonical_classes")c+=$(i+1); if($i=="star2")s+=$(i+1)}} END{print "classes", c, "star2", s}' enum9/c*.tsv > enum9/TOTAL.txt

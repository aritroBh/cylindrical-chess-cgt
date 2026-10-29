#!/bin/zsh
# verification chain: the four survivors of cyl7x6_f3, one heavy.sh call each (Psi computed in the first call).
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K29
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
for Z in "Kb3 Pa2 Pc2 kb1 pa3 pc3" "Kb1 Pa2 Pb3 ka3 pb2 pc5" "Kb3 Pa2 Pa4 ka5 pa3 pb4" "Kb3 Pc2 Pa4 ka5 pc3 pb4"; do
  $H /usr/bin/time -l zsh scripts/ver2.sh cyl7x6_f3 cyl:7x6 cyl:7x6 ef a1 a6 "$Z" >> logs/ver_cyl7x6_f3.out 2>> logs/ver_cyl7x6_f3.err
done
echo "ver cyl7x6_f3 done $(date +%H:%M)" >> logs/progress.txt

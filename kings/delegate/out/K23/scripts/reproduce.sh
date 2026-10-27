#!/bin/zsh
# reproduce.sh: every number of the K23 report. Run from the K23 directory. The enumerations take 10-140 s of CPU each:
# run them through /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh when the machine is shared.
set -e
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K23
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
mkdir -p bin data logs
cc -O2 -o bin/kp /Users/aritro/Downloads/Research/Chessendgames/kings/kpsolve.c -lpthread
cc -O2 -o bin/kp_p /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K7/scripts/draft/kp_p.c -lpthread   # --pmodel
cc -O2 -o bin/pk2 scripts/pk2.c                                                                                        # independent P / frozen solver
# 1. the key positions (small): both implementations, P and frozen; needs data/key_7x6.txt, dist8.txt, g88.txt, pair.txt
scripts/run_key.sh && $PY scripts/digest.py logs/key_results.txt > logs/key_digest.txt
# 2. enumerations: Z_T + every context (e.p. '-', both sides to move)
$PY scripts/gen_ctx.py 'Ka4 Pb3 kc3 pb4' ef  2 2 2-5 > data/ctx_7x6_22.txt      # 885 contexts, cyl:7x6
$PY scripts/gen_ctx.py 'Ka4 Pb3 kc3 pb4' ef  3 3 2-5 > data/ctx_7x6_33.txt      # 3237 contexts
$PY scripts/gen_ctx.py 'Ka4 Pb3 kc3 pb4' efg 2 2 2-5 > data/ctx_8x6_22.txt      # 4579 contexts, cyl:8x6
$PY scripts/gen_ctx.py 'Ka4 Pb3 kc3 pb4' f   4 4 2-5 > data/ctx_8x6_f.txt       # 81 contexts on f
for x in "7x6_22 cyl:7x6" "7x6_33 cyl:7x6" "8x6_22 cyl:8x6" "8x6_f cyl:8x6"; do
  set -- ${=x}; n=$1; b=$2
  ./bin/pk2 --board $b          < data/ctx_$n.txt > data/ctx_$n.P
  ./bin/pk2 --board $b --frozen < data/ctx_$n.txt > data/ctx_$n.F
  ./bin/kp_p --board $b --pmodel --ep on --promote Q < data/ctx_$n.txt > data/ctx_$n.P2 2>/dev/null
  ./bin/kp   --board $b --frozen --ep on --promote Q < data/ctx_$n.txt > data/ctx_$n.F2 2>/dev/null
  scripts/agree.sh data/ctx_$n.P data/ctx_$n.P2; scripts/agree.sh data/ctx_$n.F data/ctx_$n.F2
  w=${b#cyl:}; w=${w%x*}
  $PY scripts/classify.py $w data/ctx_$n.P data/ctx_$n.F 4 0
done
# 3. the result of G does not depend on the kings: Z_T against parked kings (Ka1 ka6), frozen, both solvers
sed 's/^Ka4 Pb3 kc3 pb4/Ka1 ka6/' data/ctx_7x6_22.txt > data/ctx_7x6_22_parked.txt
./bin/pk2 --board cyl:7x6 --frozen < data/ctx_7x6_22_parked.txt > data/ctx_7x6_22_parked.F
./bin/kp --board cyl:7x6 --frozen --ep on --promote Q < data/ctx_7x6_22_parked.txt > data/ctx_7x6_22_parked.F2 2>/dev/null
# (compare the context part of data/ctx_7x6_22.F with data/ctx_7x6_22_parked.F: 0 differences)

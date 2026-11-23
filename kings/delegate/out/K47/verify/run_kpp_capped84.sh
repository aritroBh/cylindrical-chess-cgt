#!/bin/zsh
# kp_p --pmodel on the 21 sampled cyl:10x6 contexts (84 positions), killed (own PID only) if its RSS passes 2.9 GB
cd "$(dirname $0)"
./kpp_k47ref --board cyl:10x6 --pmodel --cap 1 --threads 1 < ctx_ref.pos > logs/ctx_ref.kpp 2> logs/ctx_ref_kpp.err &
P=$!; echo "$P kpp_k47ref (child of run_kpp_capped.sh) $(date)" >> pids.log
peak=0
while kill -0 $P 2>/dev/null; do
  r=$(ps -o rss= -p $P 2>/dev/null | tr -d ' '); [[ -n $r ]] && (( r > peak )) && peak=$r
  if [[ -n $r ]] && (( r > 2900000 )); then kill $P; echo "killed at rss ${r} KB" >> logs/ctx_ref_kpp.err; fi
  sleep 2
done
echo "peak rss ${peak} KB" >> logs/ctx_ref_kpp.err
echo done > logs/ctx_ref_kpp.done

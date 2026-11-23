#!/bin/zsh
cd "$(dirname $0)"
../../heavy.sh ./bin/ref3m_k45 --board cyl:10x6 < ctx_positions.txt > ctx_ref3m.out 2> logs/ctx_ref3m.err
../../heavy.sh ./bin/kp_p10_k45 --board cyl:10x6 --pmodel --cap 1 --threads 1 < ctx_positions.txt > ctx_kpp.out 2> logs/ctx_kpp.err
echo done > logs/ctx.done

#!/bin/zsh
# K47 item 3: P values of the group beside contexts, two solvers (ref3m, kp_p --pmodel)
cd "$(dirname $0)"
tag=$1; board=$2
./ref3m_k47 --board $board < ctx_$tag.pos > logs/ctx_${tag}.ref3m 2> logs/ctx_${tag}_ref3m.err
./kpp_k47 --board $board --pmodel --cap 1 --threads 1 < ctx_$tag.pos > logs/ctx_${tag}.kpp 2> logs/ctx_${tag}_kpp.err
echo done > logs/ctx_${tag}.done

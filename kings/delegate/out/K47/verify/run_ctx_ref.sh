#!/bin/zsh
# K47 referee item 3: the cyl:10x6 exception and 20 other sampled contexts, ref3m and kp_p --pmodel
cd "$(dirname $0)"
/usr/bin/time -l ./ref3m_k47ref --board cyl:10x6 < ctx_ref.pos > logs/ctx_ref.ref3m 2> logs/ctx_ref_ref3m.err
/usr/bin/time -l ./ref3m_k47ref --board cyl:10x6 --moves < ctx_exc.pos > logs/ctx_exc_moves.ref3m 2> logs/ctx_exc_moves_ref3m.err
/usr/bin/time -l ./kpp_k47ref --board cyl:10x6 --pmodel --cap 1 --threads 1 --moves < ctx_ref.pos > logs/ctx_ref.kpp 2> logs/ctx_ref_kpp.err
echo done > logs/ctx_ref.done

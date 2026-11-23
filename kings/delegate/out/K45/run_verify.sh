#!/bin/zsh
cd "$(dirname $0)"
{
for s in ref3m kpp; do
 python3 verify_hit.py $s 10 1 "Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5 b -" g6
 python3 verify_hit.py $s 10 1 "Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5 b -" d5
 python3 verify_hit.py $s 10 0 "Kf1 kg3 Pa2 Pb3 Pe2 pb4 pe5 w -" f2
 python3 verify_hit.py $s 10 0 "Kd2 kf2 Pa3 Pb2 Pe2 pb3 pb5 pe5 w -" d3
 echo "negative control (K44 root, expected FAIL at U4):"
 python3 verify_hit.py $s 10 1 "Kc3 ka4 Pa2 pa3 Pc4 pc5 Pf2 pf3 b -" a5
done
} > verify_hits_ref3m_kpp.txt 2>&1
echo done > logs/verify.done

#!/bin/zsh
# the named counterexamples: certificate (chk), frozen kpsolve, P with real kings (kp_p), independent Python P solver, strategy failure
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
PY=/Users/aritro/Downloads/Research/Chessendgames/.venv/bin/python
export PYTHONPATH=/Users/aritro/Downloads/Research/Chessendgames
ex() {  # board position beta psq
  echo "== $1  $2   (beta=$3, p=$4)"
  echo "$2" | $D/work/chk --board $1 --mode cert
  echo -n "frozen: "; echo "$2" | $D/work/kp --board $1 --frozen 2>/dev/null
  echo -n "P real kings (kp_p): "; echo "$2" | $D/work/kpp --board $1 --pmodel 2>/dev/null
  echo -n "P real kings (pyp.py): "; $PY $D/scripts/pyp.py $1 "$2"
  echo -n "strategy 'beta pushes p': "; $PY $D/scripts/classify.py $1 "$2" $3 $4
}
ex cyl:8x6 'Ka1 ka6 Pc2 w -' W c2
ex cyl:6x6 'Ka4 ka6 Pa5 Pd5 b -' W d5
ex flat:6x6 'Kc1 ka1 Pc2 pa2 w -' W c2
ex flat:6x6 'Kc1 ka1 Pc2 pa3 w -' W c2
ex flat:6x6 'Kd2 kf1 Pa2 Pf3 pf2 pd3 w -' W a2
ex flat:6x6 'Kc1 ka1 Pc2 pa3 b -' W c2

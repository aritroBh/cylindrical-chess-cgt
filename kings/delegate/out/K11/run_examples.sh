#!/bin/zsh
set -eu
ROOT_DIR=/Users/aritro/Downloads/Research/Chessendgames
OUT_DIR=$ROOT_DIR/kings/delegate/out/K11
IN_FILE=$OUT_DIR/cases.in
OUT_FILE=$OUT_DIR/cases.out
cat > "$IN_FILE" <<'EOF'
Ka1 ka6 Pc4 pf4 w -
Ka1 ka6 Pc4 pf4 b -
Ka1 ka6 Pc4 pf2 w -
Ka1 ka6 Pc4 pf2 b -
Ka1 ka6 Pc3 Pd4 pf4 b -
Ka1 ka6 Pc4 pd4 w -
Ka1 ka6 Pd4 w -
Ka1 ka6 Pc4 Pe3 pd4 w -
Ka1 ka6 Pc4 Pe3 Pg4 pd4 b c3
Ka1 ka6 Pc4 Pe2 pf3 b -
Ke2 ka6 Pc4 Pf2 pf3 w -
EOF
trap 'rm -f "$IN_FILE" "$OUT_FILE"' EXIT
"$ROOT_DIR/kings/delegate/heavy.sh" "$OUT_DIR/kp" --board cyl:8x6 --frozen --cap 1 --threads 2 < "$IN_FILE" > "$OUT_FILE"
cat "$OUT_FILE"

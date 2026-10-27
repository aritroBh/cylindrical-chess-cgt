#!/bin/zsh
# run_key.sh: regenerates every small number quoted in the report, with both implementations (all runs are < 5 s)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K23
O=logs/key_results.txt; : > $O
run() { # label board file
  echo "=== $1  board $2  file $3" >> $O
  for m in "P:pk2 --board $2" "F:pk2 --board $2 --frozen"; do
    echo "--- pk2 ${m%%:*}" >> $O; nice ./bin/${=m#*:} < $3 | grep -v '^#' >> $O; done
  echo "--- kp_p --pmodel (P)" >> $O; nice ./bin/kp_p --board $2 --pmodel --ep on --promote Q < $3 2>/dev/null | grep -v '^#' >> $O
  echo "--- kp --frozen (F)" >> $O; nice ./bin/kp --board $2 --frozen --ep on --promote Q < $3 2>/dev/null | grep -v '^#' >> $O
}
run key7x6 cyl:7x6 data/key_7x6.txt
run dist8 cyl:8x6 data/dist8.txt
run g88 cyl:8x8 data/g88.txt
echo "--- kp_p --moves, the pair" >> $O
nice ./bin/kp_p --board cyl:7x6 --pmodel --ep on --promote Q --moves < data/pair.txt 2>/dev/null >> $O

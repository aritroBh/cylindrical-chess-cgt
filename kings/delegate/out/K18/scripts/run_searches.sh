#!/bin/zsh
# sequential group searches, then the bare cross-check (one heavy slot for the whole chain)
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
run() { # board fz maxw maxb tag [extra]
  nice -n 15 bin/lg --board $1 --fz $2 --maxw $3 --maxb $4 --search ${@:6} > logs/search_$5.out 2> logs/search_$5.err
}
run cyl:8x6 0:3 2 2 c8x6_f3_22 --dumpbare logs/bare_c8x6_f3_22.txt
awk -F' \\| ' '{print $1}' logs/bare_c8x6_f3_22.txt | sort -u > logs/bare_in.txt
nice -n 15 bin/kpp --board cyl:8x6 --ep on --pmodel --promote Q --cap 0 --threads 2 < logs/bare_in.txt > logs/bare_out.txt 2> logs/bare_out.err
run cyl:7x6 0:3 2 2 c7x6_f3_22
run cyl:8x6 0:4 2 2 c8x6_f4_22
run cyl:7x6 0:4 2 2 c7x6_f4_22
run cyl:8x6 0:3 3 2 c8x6_f3_32
run cyl:7x6 0:3 3 2 c7x6_f3_32
run flat:6x6 0:3 2 2 flat6x6_f3_22
echo done > logs/searches_done

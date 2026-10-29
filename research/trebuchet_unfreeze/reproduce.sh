#!/bin/zsh
# Exact commands (run from this folder; every heavy command under nice -n 15, record PIDs, one or two at a time).
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
cc -O2 -pthread -o src/kpsolve_orig src/kpsolve_orig.c      # copy of kings/kpsolve.c
cc -O2 -pthread -o src/kpv src/kpv.c                        # kp_p.c (K7 draft, --pmodel) + --pmode 2|3|4 --stale 0|1|2
cc -O2 -pthread -o src/kpw src/kpw.c                        # kpv + --kids (prints child positions)
cc -O2 -pthread -o src/kpv5 src/kpv5.c                      # kpv + --pmode 5
# (a) baseline, cap 2, QRBN, 6 refuted rows (253 MB RSS):
nice -n 15 src/kpsolve_orig --board cyl:7x6 --cap 2 --promote QRBN --moves < data/p4_refuted6.txt
# (a) grid on the 12 P4 rows (jobs.txt, run_grid.sh 0 and 1), flat12 (see logs/flat12_*), walker per refuted row:
./run_grid.sh 0 & ./run_grid.sh 1
python3 walker.py "Ka4 Pb3 kc3 pb4 Pe3 pe4 b -" cyl:7x6 data/walks/H0.json
python3 walker.py "Ka4 Pb3 kc3 pb4 Pe3 pe5 w -" cyl:7x6 data/walks/Hstar.json
for v in "chess:" "m2:--pmode 2" "m3:--pmode 3" "m4:--pmode 4" "P:--pmodel"; do ... src/kpv --board flat:7x6 --cap 2 --promote Q ... --moves < data/p4_all12.txt; done
# (b) suite (tablebase cache, no network):
python3 suite_features.py; python3 suite_fit.py
nice -n 15 src/kpv --board flat:8x8 --frozen --promote Q --moves < data/suite275_kp.txt     # + data/suite275_flip_kp.txt
nice -n 15 src/kpv --board flat:8x8 --cap 1 --promote Q --moves < data/suite_pilot.txt       # 9-position pilot, 1.6 GB
python3 suite_pilot_cmp.py
# (b) cyl:6x6 sample:
python3 sample6x6.py; python3 sampleB.py             # data/s6x6.txt (2000), data/sB.txt (384)
./run_b6.sh 0 & ./run_b6.sh 1                         # 34 batches of 60: chess cap 1 (<= 0.7 GB each) + frozen
./run_bB.sh 0 & ./run_bB.sh 1
./run_u.sh 0 & ./run_u.sh 1                           # cap 2 on cap-1-unresolved (B: all 164; main: 9 of 15 batches)
src/kpv --board cyl:6x6 --frozen --promote Q --moves < data/s6x6_flip.txt                    # tempo ("pass") test
python3 s6_analyze.py s6; python3 s6_analyze.py B; python3 s6_fit.py s6; python3 s6_fit.py B  # data/*_table.json.zst: zstd -d first

#!/bin/bash
# Reproduce the T42 results.  Each step is independent; every s3 process is capped at 2^25 table entries (1.9 GB).
# Roughly: scans 45 CPU-minutes, Python checks 90 CPU-minutes.  Run from anywhere.
cd "$(dirname "$0")"
ROOT=../..
cc -O2 -o s3 s3.c -lm        # solver core copied unchanged from ../star26_rings/frontier_split1_fixed2.c
mkdir -p tmp

# 1. headline: A is *2, A + a one-file * group on the adjacent file is *3 (columns: outcome, nimber, outcome of G+*k)
printf 'W: a4 b3 d2 d3 / B: a7 b7 c5\nW: a4 b3 d2 d3 e4 / B: a7 b7 c5 e6\n' > tmp/t42_pos.txt
./s3 --flat --width 5 --eval tmp/t42_pos.txt
# 1b. every position within two pawn edits of A on five files (finds the *3 above in 0.4 s)
echo 'W: a4 b3 d2 d3 / B: a7 b7 c5' > tmp/t42_seedA.txt
./s3 --flat --width 5 --single --ball tmp/t42_seedA.txt --radius 2 --pmin 7 --pmax 9
# 1c. same, around every single-component 8-pawn *2 (tmp/seeds2_*.txt are the *2 lines of small/*.tsv): 10-pawn *3
#     ./s3 --flat --width 6 --single --ball tmp/seeds2_flat_w5.txt --radius 2 --pmin 7 --pmax 10

# 2. exhaustive scans of single-component roots (every file occupied), default setting; merge_chunks.py sums the chunks
./run_chunks.sh flat_w5_p9_4_5 48 2 "--flat --width 5 --nw 4 --nb 5 --single"       # 18,603,810 roots: *3 x4
./run_chunks.sh flat_w5_p9_3_6 24 2 "--flat --width 5 --nw 3 --nb 6 --single"       #  8,167,217 roots: none
./run_chunks.sh flat_w5_p9_2_7 8 2 "--flat --width 5 --nw 2 --nb 7 --single"        #  1,149,962 roots: none
./run_chunks.sh flat_w6_p9_4_5 96 2 "--flat --width 6 --nw 4 --nb 5 --single"       # 35,093,597 roots: *3 x4
./run_chunks.sh flat_w6_p9_3_6 48 2 "--flat --width 6 --nw 3 --nb 6 --single"       # 12,658,906 roots: none
./run_chunks.sh flat_w6_p9_2_7 8 2 "--flat --width 6 --nw 2 --nb 7 --single"        #    740,425 roots: none
./run_chunks.sh flat_w7_p9_4_5 128 2 "--flat --width 7 --nw 4 --nb 5 --single"      # 31,591,330 roots: none
./run_chunks.sh flat_w7_p9_3_6 32 2 "--flat --width 7 --nw 3 --nb 6 --single"       #  8,444,841 roots: none
./run_chunks.sh flat_w4_p10_5_5 24 2 "--flat --width 4 --nw 5 --nb 5 --single --colsym"   # 6,275,963 roots: none
./run_chunks.sh flat_w4_p10_4_6 24 2 "--flat --width 4 --nw 4 --nb 6 --single"      #  9,360,358 roots: none
./run_chunks.sh cyl_w4_p9_4_5 12 2 "--cylinder --width 4 --nw 4 --nb 5 --single"    #  1,491,833 roots: none
./run_chunks.sh cyl_w4_p10_5_5 12 2 "--cylinder --width 4 --nw 5 --nb 5 --single --colsym"  # 2,169,192 roots: none
./run_chunks.sh cyl_w5_p9_4_5 24 2 "--cylinder --width 5 --nw 4 --nb 5 --single"    #  5,596,948 roots: none
./run_chunks.sh cyl_w5_p10_5_5 48 2 "--cylinder --width 5 --nw 5 --nb 5 --single --colsym"  # 13,114,414 roots: none
for d in scans/*; do python3 merge_chunks.py $d; done; python3 coverage.py

# 3. at most 8 pawns: every flat board of width <= 8 (gaps allowed) and every ring C3..C8, nw <= nb (colour reversal)
./run_le8.sh > tmp/run_le8.out                                   # 110,276,698 roots, largest nimber *2
bash ./rerun_capped.sh                                           # the three memory-hungry ones again with the table capped
(cd $ROOT && PYTHONPATH=. .venv/bin/python research/star3_single/sums_le8.py)     # k>=3 components, pairs up to (2,5)
(cd $ROOT && PYTHONPATH=. .venv/bin/python research/star3_single/sums_span9.py)    # pairs (4,4) (3,5) (2,6) of span >= 9

# 4. independent verification of the *3 positions
(cd $ROOT && PYTHONPATH=. .venv/bin/python research/star3_single/verify.py all 5 flat "W: a4 b3 d2 d3 e4 / B: a7 b7 c5 e6")
bash ./verify_batch.sh                                           # cylcgt sum + whole board for the other seven classes
python3 images.py 5 tmp/classes5.txt > tmp/all16.txt
(cd $ROOT && PYTHONPATH=. .venv/bin/python research/star3_single/verify_masks.py 5 research/star3_single/tmp/all16.txt)   # Codex solver, 16 images
(cd $ROOT && PYTHONPATH=. .venv/bin/python research/star3_single/crosscheck_near.py 60 7)      # s3 vs Codex on 60 positions near A
python3 classify.py 5 tmp/classes5.txt

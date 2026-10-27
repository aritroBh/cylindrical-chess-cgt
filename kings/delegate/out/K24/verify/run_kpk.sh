#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K24/verify
echo "== cyl:8x8"; ./kp --board cyl:8x8 --ep on --promote QRBN --cap 1 < kpk_pos8.txt
echo "== flat:8x8"; ./kp --board flat:8x8 --ep on --promote QRBN --cap 1 < <(echo "Ke7 Pd7 kc7 b -")
echo "== cyl:7x6"; ./kp --board cyl:7x6 --ep on --promote QRBN --cap 1 < kpk_pos5.txt

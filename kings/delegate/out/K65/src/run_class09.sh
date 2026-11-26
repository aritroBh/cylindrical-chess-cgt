#!/bin/zsh
# K65: classification of C125_09 = Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7 (flat 8x8), which fails (B1) at ...Ke5-d6 and ...Ke5-e6:
# (C) by Aux (aux60, K60's program, on the K56 referee's generator); ladders T_0..T_6 beside every bad Black root move by
# vgsum59 (--tests, K57 referee's sum solver) and by pr57 (--sum with --probe, K56's separately written generator).
cd "$(dirname $0)/.."
G="Kc4 ke4 Pb5 Pf2 Pf6 pb6 pf7"
zsh src/hrun3.sh cls/C125_09_aux bin/aux60 --board flat:8x8 --root "$G" --shuttle e5
zsh src/hrun3.sh cls/C125_09_TN_vgsum bin/vgsum59 --lowmem --board flat:8x8 --root "$G" --shuttle e5 --tests in/T_N.txt
zsh src/hrun3.sh cls/C125_09_TN_pr57 bin/pr57 --board flat:8x8 --root "$G" --shuttle e5 --orient over --sum in/TN_pr57.txt --probe in/probes_C125_09.txt

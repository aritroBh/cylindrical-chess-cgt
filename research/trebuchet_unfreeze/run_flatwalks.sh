#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
echo $$ > logs/flatwalks.pid
nice -n 15 python3 walker.py "Ka4 Pb3 kc3 pb4 Pe3 pe4 b -" flat:7x6 data/walks/H0_flat.json > logs/walk_H0_flat.out 2>&1
nice -n 15 python3 walker.py "Ka4 Pb3 kc3 pb4 Pe3 pe5 w -" flat:7x6 data/walks/Hstar_flat.json > logs/walk_Hstar_flat.out 2>&1

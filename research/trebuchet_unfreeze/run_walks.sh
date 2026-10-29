#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/research/trebuchet_unfreeze
echo $$ > logs/walks.pid
nice -n 15 python3 walker.py "Ka4 Pb3 kc3 pb4 Pe3 pe5 w -" cyl:7x6 data/walks/Hstar.json > logs/walk_Hstar.out 2>&1
nice -n 15 python3 walker.py "Ka4 Pb3 kc3 pb4 Pe2 pe5 w -" cyl:7x6 data/walks/Hstar2.json > logs/walk_Hstar2.out 2>&1

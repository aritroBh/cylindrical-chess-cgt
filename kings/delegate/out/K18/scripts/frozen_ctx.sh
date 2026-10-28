#!/bin/zsh
cd /Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K18
bin/kp --board cyl:8x6 --frozen --ep on --promote Q --cap 0 < logs/ctx8x6_efg_22_frozen_in.txt > logs/ctx8x6_efg_22_frozen_out.txt 2> logs/ctx8x6_efg_22_frozen.err
bin/kp --board cyl:7x6 --frozen --ep on --promote Q --cap 0 < logs/ctx7x6_ef_22_frozen_in.txt > logs/ctx7x6_ef_22_frozen_out.txt 2> logs/ctx7x6_ef_22_frozen.err

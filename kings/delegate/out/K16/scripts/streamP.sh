#!/bin/zsh
# exhaustive sim sweeps, one heavy.sh acquisition per bundle
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
S=$D/scripts
$H /bin/zsh $S/bundle_ex.sh cyl:6x6 3 3 2 0 1 EX_c66_33
$H /bin/zsh $S/bundle_ex.sh cyl:6x6 4 4 6 0 5 EX_c66_44
$H /bin/zsh $S/bundle_ex.sh cyl:7x6 3 3 4 0 3 EX_c76_33
$H /bin/zsh $S/bundle_ex.sh flat:6x6 3 3 8 0 7 EX_f66_33
for ((k=0; k<16; k+=4)); do $H /bin/zsh $S/bundle_ex.sh cyl:8x6 3 3 16 $k $((k+3)) EX_c86_33; done
for ((k=0; k<24; k+=6)); do $H /bin/zsh $S/bundle_ex.sh flat:7x6 3 3 24 $k $((k+5)) EX_f76_33; done
$H /bin/zsh $S/bundle_ex.sh cyl:6x6 4 3 6 0 5 EX_c66_43
$H /bin/zsh $S/bundle_ex.sh cyl:6x6 3 4 6 0 5 EX_c66_34
for ((k=0; k<24; k+=6)); do $H /bin/zsh $S/bundle_ex.sh cyl:7x6 4 4 24 $k $((k+5)) EX_c76_44; done

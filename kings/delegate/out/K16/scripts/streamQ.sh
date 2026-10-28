#!/bin/zsh
# kp_p validation samples, one heavy.sh acquisition per bundle
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
S=$D/scripts
$H /bin/zsh $S/bundle_rand.sh flat:6x6 3 3 net 3 100000 1300 RN_f66
$H /bin/zsh $S/bundle_enum.sh cyl:7x6 2 2 40 0 39 EN_c76_22
$H /bin/zsh $S/bundle_rand.sh cyl:7x6 3 3 net 2 100000 1100 RN_c76
$H /bin/zsh $S/bundle_rand.sh cyl:6x6 3 3 scene 3 100000 2000 RS_c66
$H /bin/zsh $S/bundle_rand.sh flat:6x6 3 3 scene 3 100000 2100 RS_f66
$H /bin/zsh $S/bundle_rand.sh cyl:8x6 3 3 net 2 100000 1200 RN_c86
$H /bin/zsh $S/bundle_rand.sh flat:7x6 3 3 net 2 100000 1400 RN_f76
$H /bin/zsh $S/bundle_rand.sh cyl:7x6 3 3 scene 3 100000 2200 RS_c76
$H /bin/zsh $S/bundle_rand.sh cyl:8x6 3 3 scene 3 100000 2300 RS_c86
$H /bin/zsh $S/bundle_rand.sh flat:7x6 3 3 scene 3 100000 2400 RS_f76
$H /bin/zsh $S/bundle_rand.sh cyl:6x6 3 3 uniform 2 150000 3000 RU_c66
$H /bin/zsh $S/bundle_rand.sh flat:6x6 3 3 uniform 2 150000 3100 RU_f66
$H /bin/zsh $S/bundle_rand.sh cyl:7x6 3 3 uniform 2 150000 3200 RU_c76
$H /bin/zsh $S/bundle_rand.sh cyl:8x6 3 3 uniform 2 150000 3300 RU_c86
$H /bin/zsh $S/bundle_rand.sh flat:7x6 3 3 uniform 2 150000 3400 RU_f76
$H /bin/zsh $S/bundle_enum.sh flat:6x6 2 2 100 0 3 EN_f66_22
$H /bin/zsh $S/bundle_enum.sh cyl:6x6 3 2 100 0 2 EN_c66_32
$H /bin/zsh $S/bundle_enum.sh cyl:6x6 2 3 40 0 4 EN_c66_23
$H /bin/zsh $S/bundle_enum.sh cyl:6x6 3 3 200 0 2 EN_c66_33

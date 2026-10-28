#!/bin/zsh
# variants and controls (after Q): KV=1, KV=2, drop-one-hypothesis; exhaustive sim with KV=1/2
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
S=$D/scripts
$H /bin/zsh $S/bundle_ex.sh cyl:6x6 3 3 2 0 1 EXKV1_c66_33 --kv 1
$H /bin/zsh $S/bundle_ex.sh flat:6x6 3 3 8 0 7 EXKV1_f66_33 --kv 1
$H /bin/zsh $S/bundle_ex.sh cyl:6x6 3 3 2 0 1 EXKV2_c66_33 --kv 2
$H /bin/zsh $S/bundle_ex.sh flat:6x6 3 3 8 0 7 EXKV2_f66_33 --kv 2
for b in cyl:6x6 flat:6x6; do
  t=${b//[:x]/}
  for dr in sq h2 h1k h4 h5 h1ep; do
    $H /bin/zsh $S/bundle_rand.sh $b 3 3 scene 1 100000 7000 DR_${dr}_$t --drop $dr
  done
done
for b in cyl:6x6 flat:6x6 cyl:7x6 cyl:8x6 flat:7x6; do
  t=${b//[:x]/}
  $H /bin/zsh $S/bundle_rand.sh $b 3 3 scene 2 100000 5000 KV1_scene_$t --kv 1
done

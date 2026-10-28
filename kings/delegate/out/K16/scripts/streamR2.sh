#!/bin/zsh
# drop-one-hypothesis controls (cyl:6x6 and flat:6x6, scene style) and KV=1 samples
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
H=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/heavy.sh
S=$D/scripts
for dr in sq h2 h1k h5 h1ep h4; do
  $H /bin/zsh $S/bundle_rand.sh cyl:6x6 3 3 scene 1 100000 7000 DR_${dr}_cyl66 --drop $dr
done
$H /bin/zsh $S/bundle_rand.sh flat:6x6 3 3 scene 1 100000 7100 DR_sq_flat66 --drop sq
$H /bin/zsh $S/bundle_rand.sh flat:6x6 3 3 scene 1 100000 7100 DR_h5_flat66 --drop h5
$H /bin/zsh $S/bundle_rand.sh flat:7x6 3 3 scene 1 100000 5000 KV1_scene_flat76 --kv 1

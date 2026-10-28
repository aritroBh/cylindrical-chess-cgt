#!/bin/zsh
# after streams A2 and B2: variants KV=1 (sharper G_omega), control KV=2, and drop-one-hypothesis controls
D=/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K16
S=$D/scripts
while kill -0 $(cat $D/logs/pid_streamA2) 2>/dev/null; do sleep 30; done
for b in cyl:6x6 flat:6x6 cyl:7x6 cyl:8x6 flat:7x6; do
  t=${b//[:x]/}
  $S/run_rand.sh $b 3 3 scene 2 100000 5000 KV1_scene_$t --kv 1
  $S/run_rand.sh $b 3 3 net 1 100000 5100 KV1_net_$t --kv 1
done
for b in cyl:6x6 flat:6x6; do
  t=${b//[:x]/}
  $S/run_rand.sh $b 3 3 scene 1 100000 6000 KV2_scene_$t --kv 2
  for dr in sq h2 h1k h4 h5 h1ep; do
    $S/run_rand.sh $b 3 3 scene 1 100000 7000 DR_${dr}_$t --drop $dr
  done
done

cd /Users/aritro/Downloads/Research/Chessendgames
export PYTHONPATH=.
P=.venv/bin/python
S=atlas/flat8/indep_scan.py
$P $S --max-pawns 6 --workers 6 --out indep_scan.json
for rule in count mover opponent allW allB; do
  for ep in on off; do
    [ "$rule" = count ] && [ "$ep" = on ] && continue
    $P $S --max-pawns 6 --workers 6 --rule $rule --ep $ep --out census/indep_${rule}_ep${ep}.json
  done
done
$P $S --max-pawns 6 --workers 6 --rule count --ep on --strict-ep --out census/indep_count_epon_strict.json
$P $S --max-pawns 6 --workers 6 --rule mover --ep on --strict-ep --out census/indep_mover_epon_strict.json
$P $S --max-pawns 6 --workers 6 --rule opponent --ep on --strict-ep --out census/indep_opponent_epon_strict.json
echo CENSUS_DONE

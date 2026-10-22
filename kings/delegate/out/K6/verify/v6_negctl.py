"""Negative controls for the K6 verification: deliberately broken test games must make v_run report mismatches
against the builder's jsonl (so a clean v_run result is informative).  usage: v6_negctl.py cyl:3x6"""
import sys
sys.dont_write_bytecode = True
import v_games as vg, v_run

board = sys.argv[1]
orig = dict(vg.GAMES)
print('control 1: -1/2 replaced by * ({0|0})')
vg.GAMES['-1/2'] = vg.G('h', h=(['z'], ['z']), z=([], []))
m1 = v_run.main(board)
vg.GAMES.clear(); vg.GAMES.update(orig)
print('control 2: up replaced by the switch {0|0} copy of *  (up = {0|*} -> {0|0})')
vg.GAMES['up'] = vg.G('u', u=(['z'], ['z']), z=([], []))
m2 = v_run.main(board)
vg.GAMES.clear(); vg.GAMES.update(orig)
print('control 3: stalemate-as-draw solver flag (sd=1) used for the signatures instead of normal play')
orig_run_c = v_run.run_c
v_run.run_c = lambda g, t, sd: orig_run_c(g, t, 1)
m3 = v_run.main(board)
v_run.run_c = orig_run_c
print('mismatch totals (each must be > 0 for the control to bite):', m1, m2, m3)
sys.exit(0 if (m1 > 0 and m2 > 0 and m3 > 0) else 1)

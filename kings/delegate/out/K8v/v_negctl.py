import sys; sys.dont_write_bytecode=True
import v_games as vg, v_run
# negative control 1: wrong -1/2 (the bug the builder says an earlier version had): {0|0} instead of {-1|0}
vg.GAMES['-1/2'] = vg.G('h', h=(['z'], ['z']), z=([], []))
print('control: -1/2 replaced by *'); v_run.main('flat:3x4')

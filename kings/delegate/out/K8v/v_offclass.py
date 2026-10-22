import json, os, sys, collections
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); K4 = '/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K8'
sys.path.insert(0, HERE)
import v_gen
for board in sys.argv[1:]:
    M = v_gen.build(board); G = M['G']
    idx = M['idx']
    tag = board.replace(':', '_')
    rows = [json.loads(l) for l in open(os.path.join(K4, tag + '.jsonl'))]
    stat = collections.defaultdict(collections.Counter)
    ex = {}
    for r in rows:
        cls = r['cls'] if r['cls'] in ('off/off+*', 'dud', 'on/on+*') else None
        if not cls: continue
        wk, bk, wp = [G.W and 0 for _ in range(3)]
        def sq(s): return (ord(s[0]) - 97) + (int(s[1:]) - 1) * G.W
        wk, wp, bk = sq(r['wk']), sq(r['p']), sq(r['bk'])
        pw = (0, wk, bk, wp, None); pb = (1, wk, bk, wp, None)
        nw = len(M['succ'][idx[pw]]); nb = len(M['succ'][idx[pb]])
        stat[cls][('W-to-move chess moves=0' if nw == 0 else 'W has moves', 'B-to-move chess moves=0' if nb == 0 else 'B has moves')] += 1
        if cls == 'off/off+*': ex.setdefault('off', []).append((r['placement'], nw, nb))
    print(board, {k: dict(v) for k, v in stat.items()})
    if 'off' in ex: print('   off placements (name, #W moves, #B moves):', ex['off'])

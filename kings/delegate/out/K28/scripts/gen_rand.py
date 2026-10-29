"""gen_rand.py SEED COUNT MAXPAWNS MAXOFF > positions : random flat 7x6 positions (no pawn on its own second rank)."""
import random, sys
seed, count, maxp, maxo = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
W, H = 7, 6
rnd = random.Random(seed)
def sq(s): return 'abcdefg'[s % W] + str(s // W + 1)
out = set()
while len(out) < count:
    npw = rnd.randint(0, maxp); np_ = rnd.randint(0, maxp - npw if maxp - npw >= 0 else 0)
    no = rnd.randint(0, maxo)
    used = set(); toks = []
    def pick(rlo, rhi):
        while True:
            s = rnd.randrange(W * H)
            if rlo <= s // W <= rhi and s not in used:
                used.add(s); return s
    wk = pick(0, H - 1); bk = pick(0, H - 1)
    toks += ['K' + sq(wk), 'k' + sq(bk)]
    for _ in range(npw): toks.append('P' + sq(pick(2, 4)))      # ranks 3..5
    for _ in range(np_): toks.append('p' + sq(pick(1, 3)))      # ranks 2..4
    for _ in range(no):
        t = rnd.choice('QRBN'); c = rnd.choice([True, False])
        toks.append((t if c else t.lower()) + sq(pick(0, H - 1)))
    stm = rnd.choice('wb')
    out.add(' '.join(toks) + ' ' + stm + ' -')
for p in sorted(out): print(p)

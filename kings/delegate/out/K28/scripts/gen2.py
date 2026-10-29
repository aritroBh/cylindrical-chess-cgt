"""gen2.py SEED COUNT NPAWNS NOFF : COUNT random LEGAL flat 7x6 positions with exactly NPAWNS pawns (random colours, white on ranks 3-5,
black on ranks 2-4, so no double step) and NOFF officers (random type and colour).  Pawns are biased towards promotion."""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import kchess
seed, count, npw, noff = (int(x) for x in sys.argv[1:5])
rnd = random.Random(seed)
out = set()
while len(out) < count:
    used = set(); b = {}
    def pick(rlo, rhi):
        while True:
            f = rnd.randrange(7); r = rnd.randint(rlo, rhi)
            if (f, r) not in used:
                used.add((f, r)); return (f, r)
    b[pick(0, 5)] = 'K'; b[pick(0, 5)] = 'k'
    race = len(sys.argv) > 5 and sys.argv[5] == 'race'
    for i in range(npw):
        wh = (i % 2 == 0) if race else (rnd.random() < 0.5)   # race: alternate colours, pawns one or two steps from promotion
        if wh: b[pick(3, 4) if race else pick(2, 4)] = 'P'
        else: b[pick(1, 2) if race else pick(1, 3)] = 'p'
    for _ in range(noff):
        t = rnd.choice('QRBN'); c = rnd.random() < 0.5
        b[pick(0, 5)] = t if c else t.lower()
    stm = rnd.randrange(2)
    if kchess.legal_position(b, stm): out.add(kchess.fmt(b, stm))
for p in sorted(out): print(p)

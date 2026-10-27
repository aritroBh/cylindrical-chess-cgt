# Step 3: all blocks of width 1 and 2 over V35 (<=1 white pawn rank 2..6, <=1 black pawn rank 3..7 per file),
# each closed into a ring with an alternating W2/B4 wall: start W2 or B4, lengths 4,6 (even) and 5,7 (odd).
import sys, itertools
from lib import *
width = int(sys.argv[1])
ev = Evaluator("results_blocks.tsv", tbits=22, nodelim=3000000)
wr = [0, 2, 3, 4, 5, 6]; br = [0, 3, 4, 5, 6, 7]
V = []
for w in wr:
    for b in br:
        if w == 0 and b == 0: continue
        V.append(make_token({w} if w else set(), {b} if b else set()))
print(len(V), "tokens", flush=True)
out = open(f"blocks_w{width}.tsv", "w")
out.write("block\tf\tL\tsig\n")
done = 0
t0 = time.time()
for blk in itertools.product(V, repeat=width):
    blk = list(blk)
    for f in "WB":
        for L in (4, 6, 5, 7):
            full = blk + wall(L, f)
            if not legal_start(full): sig = "ILLEGAL"
            else: sig = ev.sig(full)
            out.write(f"{S(blk)}\t{f}\t{L}\t{sig}\n")
    done += 1
    if done % 50 == 0:
        out.flush(); print(done, f"{time.time()-t0:.0f}s", flush=True)
out.close()
print("done", done)

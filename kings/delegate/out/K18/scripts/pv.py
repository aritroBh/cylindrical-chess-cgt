#!/usr/bin/env python3
"""principal variation (a winning move for the winner, a longest-looking defence is not computed: first losing move) of a P-model
position, by repeated 'kpp --moves'.  usage: pv.py BOARD "<position>" [maxplies]"""
import subprocess, sys, re
sys.path.insert(0, "scripts"); import kit
board, pos = sys.argv[1], sys.argv[2]; maxp = int(sys.argv[3]) if len(sys.argv) > 3 else 40
kit.setboard(board, "0:3")
def moves_of(p):
    out = subprocess.run(["bin/kpp", "--board", board, "--ep", "on", "--pmodel", "--promote", "Q", "--cap", "0", "--moves"], input=p + "\n", capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if " | " in l][0].split(" | ")
    return line[1].split()[0], [(m.split(":")[0], m.split(":")[1]) for m in line[2].split()]
state = kit.lg2.parse(pos); res = []
for ply in range(maxp):
    p = kit.fmt(state)
    val, ms = moves_of(p)
    side = state[4]
    # value letters are from White's point of view; pick a move preserving the result, preferring the one that keeps the game longest for the loser
    want = val
    cands = [m for m in ms if m[1] == want] or ms
    mover_wins = (side == "w" and val == "W") or (side == "b" and val == "L")
    # winner: first matching move; loser: last matching move (cheap stand-in for 'longest resistance')
    mv = cands[0] if mover_wins else cands[-1]
    name = mv[0]  # like Kb3c4 or Pf4f3 or Pb7b8Q
    frm, to = name[1:3], name[3:5]
    found = None
    for ns, kd, f, t in kit.lg2.moves(state, side, False):
        if kit.sqn(f) == frm and kit.sqn(t) == to:
            found = (ns, kd); break
    if found is None: print("cannot apply", name); break
    res.append(f"{ply//2+1 if side=='w' else ''}{'.' if side=='w' else '...'}{name}")
    if found[1] == "promo": res.append("(promotion)"); break
    state = found[0]
print(pos, "->", val0 := moves_of(kit.fmt(kit.lg2.parse(pos)))[0]); print(" ".join(res))

# For each K15 dud group (fin2/dud_groups.md), compute the draw-move closure of king configurations with ref3m
# and test K26's "exactly two-shuttle" (4 combined king states, each root D with exactly one drawing move, a king move).
import re, subprocess, sys
REF = sys.argv[1]; MD = sys.argv[2]
sections = {}; cur = None
for line in open(MD):
    m = re.match(r"## (cyl:\d+x\d+):", line)
    if m: cur = m.group(1); sections[cur] = []; continue
    m = re.match(r"\| (\d+) \| `([^`]*)` \| ([^|]*)\|", line)
    if m and cur: sections[cur].append((int(m.group(1)), m.group(2), m.group(3).strip()))
def solve(board, lines):
    out = subprocess.run([REF, "--board", board, "--moves"], input="\n".join(lines)+"\n", capture_output=True, text=True).stdout
    res = {}
    for l in out.splitlines():
        if "|" not in l: continue
        pos, rest = l.split("|", 1); rest = rest.split()
        res[pos.strip()] = (rest[0], rest[1:])
    return res
sq = re.compile(r"[a-h][1-8]")
for board, groups in sections.items():
    W = int(board.split(":")[1].split("x")[0]); H = int(board.split("x")[1])
    if H != 6: continue
    for num, g, found in groups:
        toks = g.split(); wk = toks[0][1:]; bk = toks[1][1:]; pawns = " ".join(toks[2:])
        nW = sum(t[0]=="P" for t in toks[2:]); nB = sum(t[0]=="p" for t in toks[2:])
        seen = set(); todo = [(wk, bk)]; ok = True; info = ""
        while todo and ok and len(seen) < 40:
            c = todo.pop()
            if c in seen: continue
            seen.add(c)
            lines = [f"K{c[0]} k{c[1]} {pawns} {s} -" for s in "wb"]
            r = solve(f"cyl:{W}x{H}", lines)
            for s, l in zip("wb", lines):
                if l not in r: ok = False; info = "illegal " + l; break
                val, mv = r[l]
                draws = [x for x in mv if x.endswith(":D")]
                if val != "D": ok = False; info = f"value {val} at {l}"; break
                if len(draws) != 1 or not draws[0].startswith("K"): ok = False; info = f"{len(draws)} draw moves {draws} at {l}"; break
                to = sq.findall(draws[0])[1]
                todo.append((to, c[1]) if s == "w" else (c[0], to))
        Ws = {c[0] for c in seen}; Bs = {c[1] for c in seen}
        exact = ok and len(Ws) == 2 and len(Bs) == 2 and len(seen) == 4
        files = {ord(x[0]) - 97 for x in [*Ws, *Bs] + [t[1:] for t in toks[2:]]}
        span = min(max((f - s) % W for f in files) + 1 for s in files)
        print(f"{board}\t#{num}\t{g}\t{found}\tpawns {nW}+{nB}\tspan {span}\tconfigs {len(seen)}\t{'EXACT' if exact else 'not exact: ' + info}")

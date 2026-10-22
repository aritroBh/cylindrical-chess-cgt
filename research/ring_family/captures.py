import sys, re, collections
sys.path.insert(0, "research/ring_family")
from ringlib import *
from pump_check import fam, dump
for name, k in (("odd", 3), ("even", 2)):
    ring = fam(name, k); n = len(ring)
    edges = dump(ring, f"research/ring_family/dumps/{name}_k{k}.tsv")
    print(f"== {name} k={k} C{n}: {cstr(ring)}")
    caps = collections.Counter(); steps = collections.Counter(); term = collections.Counter(); eps = collections.Counter()
    for a, side, mv, b in edges:
        m = re.match(r"([a-u])(\d)(-|x)([a-u])(\d)( e\.p\.)?", mv)
        key = (side, m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5) + (" ep" if m.group(6) else ""))
        if b == "TERMINAL-WIN": term[key] += 1
        elif m.group(3) == "x": caps[key] += 1
        else: steps[key] += 1
    print(" kept non-terminal CAPTURE moves (side, move: #positions):")
    for k_, c in sorted(caps.items()): print("    ", k_, c)
    print(" terminal-win (passer-making) moves, distinct moves:", len(term), "occurrences:", sum(term.values()))
    print(" kept quiet moves (distinct):", len(steps), "occurrences:", sum(steps.values()))

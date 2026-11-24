"""K57 referee: test games T for the direct H10 sum check (vgsum --tests). Format per line:
name|k|L0/R0;L1/R1;...   options comma separated; W = White-win terminal, B = Black-win terminal.
usage: python3 mkT.py SEED NRANDOM > file"""
import random
import sys

named = [
    "zero|1|/",
    "m1|2|/1;/",
    "p1|2|1/;/",
    "p3|4|1/;2/;3/;/",
    "m3|4|/1;/2;/3;/",
    "on|1|0/",
    "off|1|/0",
    "dud|1|0/0",
    "star|2|1/1;/",
    "up|3|1/2;/;1/1",
    "down|3|2/1;/;1/1",
    # terminals
    "Wthreat|2|1/;W/",           # White moves to a node where White threatens W; Black has no answer there
    "Bthreat|2|/1;/B",
    "Wthreat_ans|3|1/;W/2;/",     # White threat that Black can answer
    "Bthreat_ans|3|/1;2/B;/",     # Black threat that White can answer
    "hotT|1|W/B",                 # whoever moves first wins
    "onB|1|0/B",                  # White loops for ever, Black may end it with a Black win
    "offW|1|W/0",
    "loopT|2|1/1;0,W/0,B",
    "spareW_B|3|0,1/2;/;/B",      # White has unlimited spare moves; Black may move to a node with a Black threat
    "Bslow|4|/1;/2;/3;/B",        # Black needs 4 moves to a Black win, White has none
    "Wslow|4|1/;2/;3/;W/",
    "dudB|2|0/0,1;/B",
]


def rnd(rng):
    k = rng.randint(1, 3)
    p = rng.choice([0.25, 0.4, 0.55])
    pt = rng.choice([0.0, 0.15, 0.3])
    parts = []
    for _ in range(k):
        sides = []
        for _s in range(2):
            o = [str(t) for t in range(k) if rng.random() < p]
            if rng.random() < pt:
                o.append("W")
            if rng.random() < pt:
                o.append("B")
            sides.append(",".join(o))
        parts.append("/".join(sides))
    return k, ";".join(parts)


def main():
    seed, n = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for line in named:
        print(line)
    for i in range(n):
        k, body = rnd(rng)
        print(f"r{i}|{k}|{body}")


if __name__ == "__main__":
    main()

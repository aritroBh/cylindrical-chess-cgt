#!/usr/bin/env python3
"""classify.py WIDTH FILE : for each position in FILE (one 'W: .. / B: ..' per line, flat board of WIDTH files)
decide whether it is 'A-like': deleting the pawns of the first or last file leaves a position (on WIDTH-1 files)
of nimber *2 while the deleted file alone (one W and one B pawn) has nimber *1 -- i.e. the single component
is a *2 group with a one-file * group attached on an edge file.
Values come from the C program s3 (default setting, whole-board model); that is a classification aid only.
"""
import re, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
S3 = os.path.join(HERE, "s3")


def parse(line):
    w, b = line.split("/")
    ws = re.findall(r"[a-h][1-8]", w)
    bs = re.findall(r"[a-h][1-8]", b)
    return ws, bs


def fmt(ws, bs, shift=0):
    sh = lambda s: chr(ord(s[0]) - shift) + s[1:]
    return "W: " + " ".join(sorted(sh(x) for x in ws)) + " / B: " + " ".join(sorted(sh(x) for x in bs))


def evaluate(width, positions):
    if not positions:
        return {}
    path = os.path.join(HERE, "tmp", "_cls_in.txt")
    with open(path, "w") as f:
        f.write("\n".join(positions) + "\n")
    out = subprocess.run([S3, "--flat", "--width", str(width), "--eval", path], capture_output=True, text=True).stdout
    res = {}
    for l in out.splitlines():
        if l.startswith("#"):
            continue
        p = l.split("\t")
        res[p[0]] = p[4] if len(p) > 4 else p[3]
    return res


def main():
    width = int(sys.argv[1])
    lines = [l.strip() for l in open(sys.argv[2]) if l.strip() and not l.startswith("#")]
    out = []
    for line in lines:
        ws, bs = parse(line)
        verdict = "entangled: no edge group (1-2 files) is a * beside a *2 remainder"
        found = False
        for k in (1, 2):
            for side in ("right", "left"):
                if k >= width - 1:
                    continue
                efiles = [chr(ord("a") + (width - 1 - i if side == "right" else i)) for i in range(k)]
                ew = [x for x in ws if x[0] in efiles]
                eb = [x for x in bs if x[0] in efiles]
                if not ew or not eb:
                    continue
                rw = [x for x in ws if x[0] not in efiles]
                rb = [x for x in bs if x[0] not in efiles]
                sh_rem = 0 if side == "right" else k
                rem = fmt(rw, rb, shift=sh_rem)
                lo = min(ord(f) for f in efiles) - ord("a")
                grp = fmt(ew, eb, shift=lo)
                r1 = evaluate(width - k, [rem])
                r2 = evaluate(k, [grp])
                nr = list(r1.values())[0] if r1 else "?"
                ng = list(r2.values())[0] if r2 else "?"
                if nr == "2" and ng == "1":
                    verdict = (f"sum-like: {side} {k}-file group [{' '.join(ew)} / {' '.join(eb)}] = * beside *2 remainder "
                               f"[{rem}]")
                    found = True
                    break
            if found:
                break
        out.append((line, verdict))
    for line, v in out:
        print(f"{line}\t{v}")


if __name__ == "__main__":
    main()

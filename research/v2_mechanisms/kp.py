"""Run kings/kpsolve (read-only use) under nice, record its PID in logs/kpsolve.pid, parse --moves output."""
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
KP = f"{ROOT}/kings/kpsolve"


def run(lines, board, frozen=True, cap=1, ep="on", promote="Q", moves=True, threads=1, tag="kp"):
    cmd = ["nice", "-n", "15", KP, "--board", board, "--ep", ep, "--promote", promote, "--cap", str(cap),
           "--threads", str(threads)]
    if frozen: cmd.append("--frozen")
    if moves: cmd.append("--moves")
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open(f"{HERE}/logs/kpsolve.pid", "a") as fh:
        fh.write(f"{p.pid} {tag} {' '.join(cmd[3:])}\n")
    out, err = p.communicate("\n".join(lines) + "\n")
    if p.returncode: raise RuntimeError(err)
    res = {}
    for line in out.splitlines():
        parts = [x.strip() for x in line.split("|")]
        a, b = parts[1].split()
        mv = {}
        if len(parts) >= 3:
            if parts[2].startswith("A: ") and len(parts) >= 4:
                pa = dict(t.rsplit(":", 1) for t in parts[2][3:].split()); pb = dict(t.rsplit(":", 1) for t in parts[3][3:].split())
                mv = {m: (pa[m] if pa[m] == pb.get(m) else "?") for m in pa}
            else:
                mv = dict(t.rsplit(":", 1) for t in parts[2].split())
        res[parts[0]] = (a, b, mv)
    return res, err.strip()

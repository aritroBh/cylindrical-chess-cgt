"""Run the unreduced Q-family sweep with the task-local rg binary."""
import os
import resource
import subprocess
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "../.."))
sys.path.insert(0, os.path.join(ROOT, "research", "ring_n_plus_2_proof"))
import fam

lo, hi = map(int, sys.argv[1:3])
positions = [" ".join(fam.Q(n)) for n in range(lo, hi + 1, 2)]
proc = subprocess.run(
    [os.path.join(OUT, "rg"), "solve", "3"],
    input="\n".join(positions) + "\n",
    check=True,
    capture_output=True,
    text=True,
)
sys.stdout.write(proc.stdout)
scale = 1024 * 1024 if sys.platform == "darwin" else 1024
peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / scale
print(f"peak-rss: rg={peak:.1f} MiB", file=sys.stderr)

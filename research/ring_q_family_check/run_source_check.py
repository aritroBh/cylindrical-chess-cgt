"""Run a read-only ring_n_plus_2_proof Python check against this folder's rg."""
import os
import resource
import runpy
import sys

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "../.."))
SRC = os.path.join(ROOT, "research", "ring_n_plus_2_proof")
if len(sys.argv) < 2:
    raise SystemExit("usage: run_source_check.py SCRIPT [ARGS...]")

sys.path.insert(0, SRC)
import fam

fam.RG = os.path.join(OUT, "rg")
path, *args = sys.argv[1:]
path = os.path.join(SRC, path)
sys.argv = [path, *args]
runpy.run_path(path, run_name="__main__")

scale = 1024 * 1024 if sys.platform == "darwin" else 1024
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / scale
children = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / scale
print(f"peak-rss: python={rss:.1f} MiB child={children:.1f} MiB", file=sys.stderr)

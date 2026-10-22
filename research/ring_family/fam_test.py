import sys
sys.path.insert(0, "research/ring_family")
from ringlib import *
def fam(prefix, period, k, suffix):
    return from_cstr(prefix) + from_cstr(period) * k + from_cstr(suffix)
if __name__ == "__main__":
    prefix, period, suffix = sys.argv[1], sys.argv[2], sys.argv[3]
    kmin = int(sys.argv[4]); kmax = int(sys.argv[5])
    for k in range(kmin, kmax + 1):
        r = fam(prefix, period, k, suffix)
        if len(r) < 3 or len(r) > 20: continue
        res = evaluate([r])
        print(f"k={k} C{len(r)} pawns={nparts(r)} {cstr(r)} -> {res[0]}", flush=True)

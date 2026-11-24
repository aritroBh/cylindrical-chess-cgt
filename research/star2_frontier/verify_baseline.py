"""Check the required old-scope census and the expanded solver's row equality."""
import collections
import csv


def rows(path):
    with open(path, newline="") as stream:
        yield from (r for r in csv.reader(stream, delimiter="\t") if r and not r[0].startswith("#"))


original = {(r[1], r[0]): r[3:] for r in rows("research/star2_frontier/baseline.tsv")}
expanded = {(r[1], r[0]): r[3:] for r in rows("research/star2_frontier/frontier_old_scope.tsv")}
assert original.keys() == expanded.keys()
assert all(original[k] == expanded[k] for k in original)
counts = collections.Counter(int(r[5].split(",", 1)[1]) for r in rows("research/star2_frontier/frontier_old_scope.tsv"))
assert len(original) == 231_071
assert counts[0] == 6_724 and counts[1] == 4_042
assert not any(k >= 2 and n for k, n in counts.items())
print(f"roots={len(original)} aware_count_zeros={counts[0]} stars={counts[1]} nimber_ge2=0; identical rows=all")

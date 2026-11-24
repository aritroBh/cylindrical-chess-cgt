"""List flat G+*2 previous-player tests among the sampled C5 roots."""
import csv

with open("research/star2_frontier/c5_flat_embed_test.tsv", newline="") as stream:
    rows = list(csv.reader(stream, delimiter="\t"))
labels = rows[0][2:11]
hits = []
for row in rows[1:]:
    settings = [labels[i] for i, value in enumerate(row[2:11]) if value == "EQUAL"]
    if settings:
        hits.append((row[0], settings))
assert len(rows) - 1 == 70 and len(hits) == 4
for position, settings in hits:
    print(f"{','.join(settings)}: {position}")
print(f"P-test hits={len(hits)} / roots={len(rows)-1}")

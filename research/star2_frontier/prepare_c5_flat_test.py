"""Select C5 cylinder *2 hits for a flat-board G+*2 geometry probe."""
import csv
import gzip

positions = set()
with gzip.open("research/star2_frontier/scope_d_c5.tsv.gz", "rt", newline="") as stream:
    for row in csv.reader(stream, delimiter="\t"):
        if row and not row[0].startswith("#") and any(int(x.split(",", 1)[1]) >= 2 for x in row[3:12]):
            positions.add(row[0])

with open("research/star2_frontier/c5_flat_embed.in", "w") as stream:
    for pos in sorted(positions):
        stream.write(f"{pos}\t5\t1,2|1,2;|;1|1\n")
print(f"selected={len(positions)}")

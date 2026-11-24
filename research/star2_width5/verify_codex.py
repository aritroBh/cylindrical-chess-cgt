#!/usr/bin/env python3
"""T21b: verify 21 C/aware *2 hits and all *3 hits with the independent whole-board solver."""
import csv
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../verify_ext/codex"))
from solver import PawnGame, parse_position, as_nimber

HERE = os.path.dirname(os.path.abspath(__file__))

# Read hits.tsv
hits = []
with open(os.path.join(HERE, "hits.tsv"), "r") as f:
    reader = csv.reader(f, delimiter="\t")
    next(reader)  # skip header
    for row in reader:
        k = int(row[0])
        settings = row[1].split(",")
        position = row[2]
        hits.append((k, settings, position))

# Group by settings to reuse PawnGame instances
from collections import defaultdict
by_settings = defaultdict(list)
for k, settings, position in hits:
    if k == 2 and "C/aware" in settings:
        by_settings[("count", True, "aware")].append(("C/aware", position))
    elif k == 3:
        for s in settings:
            if s.startswith("O/"):
                ep_on = s.endswith("/T") or s.endswith("/aware")
                aware = s.endswith("/aware")
                by_settings[("opponent", ep_on, "aware" if aware else "textbook")].append((s, position))

print(f"Settings groups: {len(by_settings)}")
for key, items in by_settings.items():
    print(f"  {key}: {len(items)} positions")

out_path = os.path.join(HERE, "verify_codex.tsv")
with open(out_path, "w") as out:
    out.write("setting\trace\tep_on\tpassed_test\tposition\tcodex_value\tcodex_nimber\n")
    
    for (race, ep_on, passed_test), items in by_settings.items():
        print(f"Creating solver for {race}, ep_on={ep_on}, passed_test={passed_test}")
        game = PawnGame(5, race, ep_on, passed_test)
        for setting_name, position in items:
            print(f"  {setting_name}: {position}")
            sys.stdout.flush()
            t0 = time.time()
            try:
                pos_for_parser = position.replace(":", "")
                w, b = parse_position(pos_for_parser, 5)
                value = game.value(w, b)
                nim = as_nimber(value)
                elapsed = time.time() - t0
                out.write(f"{setting_name}\t{race}\t{ep_on}\t{passed_test}\t{position}\t{value}\t{nim}\n")
                print(f"    -> {value} (nimber={nim}) [{elapsed:.1f}s]")
            except Exception as e:
                elapsed = time.time() - t0
                out.write(f"{setting_name}\t{race}\t{ep_on}\t{passed_test}\t{position}\tERROR: {e}\tERROR\n")
                print(f"    -> ERROR: {e} [{elapsed:.1f}s]")
            out.flush()

print(f"Results written to {out_path}")
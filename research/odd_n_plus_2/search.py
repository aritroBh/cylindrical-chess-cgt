#!/usr/bin/env python3
"""Stream canonical core+wall rings through unchanged rg, in safe batches."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ENUM = HERE / "enumerate"
RG = HERE / "rg"


def solve_batch(records, bits=22):
    for tb in range(bits, 25):
        env = os.environ.copy()
        env["TBITS"] = str(tb)
        proc = subprocess.run(
            [str(RG), "solve", "3"], input="".join(x["position"] + "\n" for x in records),
            text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
        )
        lines = proc.stdout.splitlines()
        if proc.returncode == 0 and len(lines) == len(records):
            return lines
        if len(records) > 1:
            mid = len(records) // 2
            return solve_batch(records[:mid], bits) + solve_batch(records[mid:], bits)
        if proc.returncode != 3 or tb == 24:
            print(
                f"UNSOLVED code={proc.returncode} TBITS={tb} position={records[0]['position']} "
                f"stderr={proc.stderr!r}", file=sys.stderr, flush=True,
            )
            return [None]
    raise AssertionError("unreachable")


def human(position):
    white, black = [], []
    for f, token in enumerate(position.split()):
        side = None
        for ch in token:
            if ch == "W": side = white
            elif ch == "B": side = black
            elif ch.isdigit(): side.append(f"{chr(97+f)}{ch}")
    return "W: " + " ".join(white) + " / B: " + " ".join(black)


def extended_position(record):
    tokens = record["position"].split()
    width, d, rank, phase = record["width"], record["offset"], record["rank"], record["phase"]
    for wall_index in range(9-width, 11-width):
        is_white = (wall_index + phase) % 2 == 0
        tokens.append("W" + str(rank) if is_white else "B" + str(rank+d))
    assert len(tokens) == 11
    return " ".join(tokens)


def classify(records, lines):
    hits = []
    for rec, line in zip(records, lines, strict=True):
        if line is None:
            rec["signature"] = "UNSOLVED"
            continue
        fields = line.split()
        sig = fields[0]
        rec["signature"] = sig
        rec["nodes"] = fields[1].split("=",1)[1] if len(fields) > 1 else "?"
        if sig in ("NNPN", "NNNP"):
            hits.append(rec)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int, choices=(8, 9))
    ap.add_argument("width", type=int, choices=(4, 5, 6, 7))
    ap.add_argument("wall", nargs=3, type=int, metavar=("D", "R", "P"), help="optional fixed offset, white rank, phase")
    ap.add_argument("--batch", type=int, default=40)
    ap.add_argument("--bits", type=int, default=22)
    args = ap.parse_args()
    assert 1 <= args.batch <= 40 and 20 <= args.bits <= 24

    started = time.monotonic()
    enum_args = [str(ENUM), str(args.n), str(args.width)]
    if args.wall:
        enum_args.extend(map(str, args.wall))
    enum = subprocess.Popen(
        enum_args, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1,
    )
    batch, hits, unsolved_records = [], [], []
    emitted = solved = unsolved = nim2 = nim3 = 0
    signature_counts = {}
    suffix = "" if not args.wall else "_d%d_r%d_p%d" % tuple(args.wall)
    log_path = HERE / f"hits_c{args.n}_w{args.width}{suffix}.tsv"
    log = log_path.open("w", encoding="utf-8")
    log.write("n\twidth\toffset\twhite_rank\tphase\tsignature\tnodes\tposition\tC11_signature\tC11_position\n")

    def process_batch(items):
        nonlocal solved, unsolved, nim2, nim3
        if not items:
            return
        lines = solve_batch(items, args.bits)
        found = classify(items, lines)
        for rec in items:
            sig = rec["signature"]
            signature_counts[sig] = signature_counts.get(sig, 0) + 1
        solved += sum(rec["signature"] != "UNSOLVED" for rec in items)
        unsolved += sum(rec["signature"] == "UNSOLVED" for rec in items)
        unsolved_records.extend(rec for rec in items if rec["signature"] == "UNSOLVED")
        for rec in found:
            if rec["signature"] == "NNPN": nim2 += 1
            else: nim3 += 1
            rec["extension"] = extended_position(rec)
        hits.extend(found)

    try:
        assert enum.stdout is not None
        for line in enum.stdout:
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 6 or fields[0] != "RING":
                raise RuntimeError(f"bad enumerator row: {line!r}")
            _, w, d, r, p, pos = fields
            record = {
                "n": args.n, "width": int(w), "offset": int(d), "rank": int(r),
                "phase": int(p), "position": pos,
            }
            emitted += 1
            batch.append(record)
            if len(batch) >= args.batch:
                process_batch(batch)
                batch = []
            if emitted % 2000 == 0:
                print(f"progress emitted={emitted} solved={solved} nim2={nim2} nim3={nim3}", flush=True)
        if batch:
            process_batch(batch)
        enum_err = enum.stderr.read() if enum.stderr else ""
        enum_code = enum.wait()
        if enum_code:
            raise RuntimeError(f"enumerator exited {enum_code}: {enum_err}")
        if unsolved:
            with (HERE / f"unsolved_c{args.n}_w{args.width}{suffix}.tsv").open("w", encoding="utf-8") as f:
                for rec in unsolved_records:
                    f.write(rec["position"] + "\n")
        if hits:
            extensions = [dict(rec, position=rec["extension"]) for rec in hits]
            ext_lines = solve_batch(extensions, args.bits)
            for rec, line in zip(hits, ext_lines, strict=True):
                rec["extension_signature"] = line.split()[0] if line else "UNSOLVED"
                display = human(rec["position"])
                ext_display = human(rec["extension"])
                print(f"HIT {rec['signature']} nodes={rec['nodes']} {display}")
                print(f"EXTENSION {rec['extension_signature']} {ext_display}")
                log.write(
                    f"{rec['n']}\t{rec['width']}\t{rec['offset']}\t{rec['rank']}\t{rec['phase']}\t"
                    f"{rec['signature']}\t{rec['nodes']}\t{display}\t{rec['extension_signature']}\t{ext_display}\n"
                )
        elapsed = time.monotonic() - started
        print(f"ENUMERATOR {enum_err.strip()}")
        print(
            f"SUMMARY N={args.n} w={args.width} wall={args.wall or 'all'} emitted={emitted} solved={solved} unsolved={unsolved} "
            f"star2={nim2} star3={nim3} signatures={signature_counts} extensions={len(hits)} elapsed_s={elapsed:.1f}"
        )
        group = "" if not args.wall else "_d%d_r%d_p%d" % tuple(args.wall)
        summary = {
            "n": args.n, "width": args.width, "wall_filter": args.wall,
            "enumerator": enum_err.strip(), "emitted": emitted, "solved": solved,
            "unsolved": unsolved, "signatures": signature_counts,
            "star2": nim2, "star3": nim3, "elapsed_seconds": round(elapsed, 1),
        }
        (HERE / f"summary_c{args.n}_w{args.width}{group}.json").write_text(
            json.dumps(summary, indent=2) + "\n", encoding="utf-8",
        )
    except BaseException:
        if enum.poll() is None:
            enum.terminate()
            enum.wait()
        raise
    finally:
        log.close()


if __name__ == "__main__":
    main()

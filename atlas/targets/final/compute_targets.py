#!/usr/bin/env python3
"""Compute Elkies targets in all 9 settings and check robustness/reachability."""

import json
import gzip
import sys
import os
from fractions import Fraction

# Add project root to path
ROOT = "/Users/aritro/Downloads/Research/Chessendgames"
sys.path.insert(0, ROOT)

from cylcgt import pawns, cgt

# Target values we're looking for (as they appear in the e.p.-aware database)
TARGET_VALUES = {
    "1/8",
    "-1/8",
    "1/16",
    "-1/16",
    "{0 | ↓*}",      # ↑²
    "{0, * | ↓}",    # ↑²*
    "tiny(1)",
    "tiny(2)",
    "tiny(1*)",      # May not exist exactly like this
}

# The 9 settings: {count, mover, opponent} × {e.p. off, textbook, aware}
RACE_RULES = ["count", "mover", "opponent"]
EP_SETTINGS = [
    ("off", False, False),      # e.p. off
    ("textbook", True, False),  # e.p. on, textbook test (PASSED_RESPECTS_EP = False)
    ("aware", True, True),      # e.p. on, aware test (PASSED_RESPECTS_EP = True)
]

# Board: flat 8x8 (files=width, ranks=8, wrap=False)
def make_board(width, ep_on, ep_aware):
    """Create a board with given settings."""
    # We need to temporarily modify the global PASSED_RESPECTS_EP
    return pawns.Board(files=width, ranks=8, wrap=False, ep=ep_on)

def compute_value(position_str, width, race_rule, ep_on, ep_aware):
    """Compute the value of a position under given settings."""
    # Save original globals
    orig_race = pawns.RACE_RULE
    orig_ep = pawns.PASSED_RESPECTS_EP
    
    try:
        pawns.RACE_RULE = race_rule
        pawns.PASSED_RESPECTS_EP = ep_aware
        pawns._value.cache_clear()
        
        board = pawns.Board(files=width, ranks=8, wrap=False, ep=ep_on)
        pos = pawns.Pos.parse(position_str)
        val = pawns.value(board, pos)
        return cgt.show(val)
    except pawns.RaceError as e:
        return f"RACE_ERROR: {e}"
    finally:
        pawns.RACE_RULE = orig_race
        pawns.PASSED_RESPECTS_EP = orig_ep
        pawns._value.cache_clear()

def is_target_value(val_str):
    """Check if a value string matches one of our targets."""
    # Exact matches
    if val_str in TARGET_VALUES:
        return True
    # Check for up-second family (↑² = {0 | ↓*})
    if val_str == "{0 | ↓*}" or val_str == "{0 | v*}":
        return True
    # Check for up-second-star (↑²* = {0,* | ↓})
    if val_str == "{0, * | ↓}" or val_str == "{0,* | v}":
        return True
    # Check for tiny(1), tiny(2), tiny(1*)
    if val_str.startswith("tiny("):
        inner = val_str[5:-1]
        if inner in ("1", "2", "1*"):
            return True
    return False

def load_aware_positions():
    """Load all positions from the e.p.-aware database that match our targets."""
    aware_path = os.path.join(ROOT, "atlas", "flat8", "values_aware.jsonl.gz")
    targets_found = []
    
    with gzip.open(aware_path, "rt") as f:
        for line in f:
            r = json.loads(line)
            if is_target_value(r["value"]):
                targets_found.append({
                    "position": r["position"],
                    "width": r["width"],
                    "nw": r["nw"],
                    "nb": r["nb"],
                    "value_aware": r["value"],
                    "outcome": r["outcome"],
                })
    return targets_found

def compute_all_settings(positions):
    """Compute values for all positions in all 9 settings."""
    results = []
    for p in positions:
        pos_str = p["position"]
        width = p["width"]
        entry = {
            "position": pos_str,
            "width": width,
            "nw": p["nw"],
            "nb": p["nb"],
            "value_aware_count": p["value_aware"],
            "values_by_setting": {},
            "robust": False,
        }
        
        values = []
        for race in RACE_RULES:
            for ep_name, ep_on, ep_aware in EP_SETTINGS:
                key = f"{race}/{ep_name}"
                val = compute_value(pos_str, width, race, ep_on, ep_aware)
                entry["values_by_setting"][key] = val
                values.append(val)
        
        # Check robustness: all 9 values identical
        entry["robust"] = len(set(values)) == 1
        entry["unique_values"] = list(set(values))
        results.append(entry)
    
    return results

def check_reachability(position_str, width):
    """Check if a pawn structure is reachable in a real game."""
    # Use the freeze.py logic for necessary conditions
    sys.path.insert(0, os.path.join(ROOT, "atlas", "targets"))
    import freeze
    
    result = freeze.placements(position_str, width)
    good = [x for x in result.get("placements", []) if x["freeze_ok"] and x["legal_necessary_ok"]]
    
    return {
        "fits": result.get("fits", False),
        "placements_ok": len(good),
        "best_fen": good[0]["fen_w"] if good else None,
        "best_placement": {k: good[0][k] for k in ("mirror", "offset", "treb_rank", "orientation", "WK", "BK")} if good else None,
        "all_placements": result.get("placements", []),
    }

def build_move_history(position_str, width):
    """Hand-build a move history for a reachable position (like the rerun did for 1/8)."""
    # This is a simplified version - for the report we'll note which ones have
    # hand-built histories and provide them where known
    # The rerun already built one for: W a2 b2 b3 / B a5 a6 b6 (mirror of 1/8)
    # We can try to build for others but it's complex
    return None

def main():
    print("Loading e.p.-aware database...")
    positions = load_aware_positions()
    print(f"Found {len(positions)} positions matching target values")
    
    print("Computing values in all 9 settings...")
    results = compute_all_settings(positions)
    
    print("Checking reachability...")
    for r in results:
        reach = check_reachability(r["position"], r["width"])
        r["reachability"] = reach
    
    # Group by target value
    by_target = {}
    for r in results:
        target = r["value_aware_count"]
        if target not in by_target:
            by_target[target] = []
        by_target[target].append(r)
    
    # Print summary
    print("\n=== SUMMARY ===")
    for target, entries in sorted(by_target.items()):
        robust = [e for e in entries if e["robust"]]
        reachable_robust = [e for e in robust if e["reachability"]["placements_ok"] > 0]
        best = reachable_robust[0] if reachable_robust else (robust[0] if robust else entries[0])
        print(f"{target}: {len(entries)} positions, {len(robust)} robust, {len(reachable_robust)} robust+reachable")
        if best["reachability"]["best_fen"]:
            print(f"  Best: {best['position']} (w{best['width']}) - FEN: {best['reachability']['best_fen']}")
        else:
            print(f"  Best: {best['position']} (w{best['width']}) - NO REACHABLE PLACEMENT")
    
    # Save detailed results
    output_path = os.path.join(ROOT, "atlas", "targets", "final", "targets_9settings.json")
    with open(output_path, "w") as f:
        json.dump({
            "by_target": by_target,
            "all_results": results,
        }, f, indent=2)
    print(f"\nSaved detailed results to {output_path}")
    
    # Generate REPORT.md
    generate_report(by_target, results)

def generate_report(by_target, all_results):
    """Generate the REPORT.md file."""
    lines = []
    lines.append("# Elkies Targets: Robustness Across 9 Settings")
    lines.append("")
    lines.append("**Summary**")
    lines.append(f"- Examined {len(all_results)} positions from the e.p.-aware database matching target values")
    lines.append(f"- Tested each in 9 settings: 3 race rules (count, mover, opponent) × 3 e.p. variants (off, textbook, aware)")
    lines.append(f"- A position is **ROBUST** if it has the same value in all 9 settings")
    lines.append(f"- Reachability checked using necessary conditions (pawn counts, capture parity, file accessibility) + conservative freeze test")
    lines.append("")
    
    # Main table
    lines.append("## Target Summary Table")
    lines.append("")
    lines.append("| Target | Total Positions | Robust (9/9) | Robust & Reachable | Best Example (FEN) | Men |")
    lines.append("|--------|----------------:|-------------:|-------------------:|-------------------|----:|")
    
    target_order = ["1/8", "-1/8", "1/16", "-1/16", "{0 | ↓*}", "{0, * | ↓}", "tiny(1)", "tiny(2)", "tiny(1*)"]
    
    for target in target_order:
        if target not in by_target:
            continue
        entries = by_target[target]
        robust = [e for e in entries if e["robust"]]
        reachable_robust = [e for e in robust if e["reachability"]["placements_ok"] > 0]
        best = reachable_robust[0] if reachable_robust else (robust[0] if robust else entries[0])
        
        fen = best["reachability"]["best_fen"] or "—"
        men = best["nw"] + best["nb"] + 4  # component pawns + 4 pieces from trébuchet (2 pawns, 2 kings)
        
        lines.append(f"| {target} | {len(entries)} | {len(robust)} | {len(reachable_robust)} | `{fen}` | {men} |")
    
    lines.append("")
    
    # Detailed sections per target
    lines.append("## Detailed Results by Target")
    lines.append("")
    
    for target in target_order:
        if target not in by_target:
            lines.append(f"### {target}")
            lines.append("")
            lines.append("*No positions found in e.p.-aware database.*")
            lines.append("")
            continue
        
        entries = by_target[target]
        robust = [e for e in entries if e["robust"]]
        reachable_robust = [e for e in robust if e["reachability"]["placements_ok"] > 0]
        
        lines.append(f"### {target}")
        lines.append("")
        lines.append(f"- **Total positions in e.p.-aware database:** {len(entries)}")
        lines.append(f"- **Robust (same value in all 9 settings):** {len(robust)}")
        lines.append(f"- **Robust and reachable (passes freeze + legality):** {len(reachable_robust)}")
        lines.append("")
        
        if robust:
            lines.append("#### Robust positions:")
            lines.append("")
            for e in robust:
                reach = e["reachability"]
                fen = reach["best_fen"] or "—"
                lines.append(f"- `{e['position']}` (width {e['width']}, {e['nw']+e['nb']} pawns)")
                lines.append(f"  - Value in all 9 settings: `{e['unique_values'][0]}`")
                lines.append(f"  - Reachable: {'Yes' if reach['placements_ok'] > 0 else 'No'} ({reach['placements_ok']} valid placements)")
                if reach["best_fen"]:
                    lines.append(f"  - Best FEN: `{reach['best_fen']}`")
                    pl = reach["best_placement"]
                    lines.append(f"  - Placement: mirror={pl['mirror']}, offset={pl['offset']}, treb_rank={pl['treb_rank']}, orientation={pl['orientation']}, WK={pl['WK']}, BK={pl['BK']}")
                lines.append("")
        
        if entries and not robust:
            lines.append("#### Non-robust positions (values vary across settings):")
            lines.append("")
            for e in entries[:5]:  # Show first 5
                lines.append(f"- `{e['position']}` (width {e['width']}): values = {e['unique_values']}")
            if len(entries) > 5:
                lines.append(f"  ... and {len(entries) - 5} more")
            lines.append("")
        
        # Show value matrix for first few positions
        lines.append("#### Value matrix (first 3 positions):")
        lines.append("")
        header = ["Setting"] + [f"Pos {i+1}" for i in range(min(3, len(entries)))]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        
        for race in RACE_RULES:
            for ep_name, ep_on, ep_aware in EP_SETTINGS:
                key = f"{race}/{ep_name}"
                row = [key]
                for e in entries[:3]:
                    row.append(e["values_by_setting"].get(key, "?"))
                lines.append("| " + " | ".join(row) + " |")
        lines.append("")
    
    # Reproducibility
    lines.append("## Reproducibility")
    lines.append("")
    lines.append("Run from project root:")
    lines.append("")
    lines.append("```bash")
    lines.append("cd /Users/aritro/Downloads/Research/Chessendgames")
    lines.append("PYTHONPATH=. .venv/bin/python atlas/targets/final/compute_targets.py")
    lines.append("```")
    lines.append("")
    lines.append("Or recompute a single position:")
    lines.append("")
    lines.append("```python")
    lines.append("from cylcgt import pawns, cgt")
    lines.append("pawns.RACE_RULE = 'count'")
    lines.append("pawns.PASSED_RESPECTS_EP = True  # aware test")
    lines.append("pawns._value.cache_clear()")
    lines.append("board = pawns.Board(files=3, ranks=8, wrap=False, ep=True)")
    lines.append("pos = pawns.Pos.parse('W: a2 b2 b6 / B: a6 b7 c5')")
    lines.append("val = pawns.value(board, pos)")
    lines.append("print(cgt.show(val))  # Should be {0, * | ↓}")
    lines.append("```")
    
    report_path = os.path.join(ROOT, "atlas", "targets", "final", "REPORT.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Saved REPORT.md to {report_path}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Comprehensive analysis of KPKP solver outputs."""
import sys
import random
import subprocess
from collections import defaultdict

def parse_line(line):
    """Parse a line from kpsolve output. Returns (pos_key, stm, bound_a, bound_b, is_illegal)."""
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    if '|' not in line:
        return None
    pos_part, res_part = line.split('|', 1)
    pos_part = pos_part.strip()
    res_part = res_part.strip()
    
    # Position key without side to move and e.p. for pairing
    tokens = pos_part.split()
    stm = tokens[-2]  # 'w' or 'b'
    ep = tokens[-1]   # e.p. target or '-'
    
    # Key for pairing: all pieces but without stm and ep
    piece_tokens = tokens[:-2]
    piece_tokens.sort()
    pair_key = ' '.join(piece_tokens)
    
    bounds = res_part.split()
    if len(bounds) >= 2:
        bound_a, bound_b = bounds[0], bounds[1]
    else:
        bound_a = bound_b = bounds[0] if bounds else 'X'
    
    is_illegal = (bound_a == 'X' and bound_b == 'X')
    exact = (bound_a == bound_b)
    
    return {
        'full_pos': pos_part,
        'pair_key': pair_key,
        'stm': stm,
        'ep': ep,
        'bound_a': bound_a,
        'bound_b': bound_b,
        'exact': exact,
        'illegal': is_illegal,
        'result': bound_a if exact else 'CAPPED'
    }

def load_results(zst_file):
    """Load all results from a zst file."""
    import subprocess
    proc = subprocess.Popen(['zstdcat', zst_file], stdout=subprocess.PIPE, text=True)
    results = {}
    pair_map = defaultdict(lambda: {'w': None, 'b': None})
    
    for line in proc.stdout:
        parsed = parse_line(line)
        if parsed is None:
            continue
        key = (parsed['pair_key'], parsed['stm'], parsed['ep'])
        results[key] = parsed
        pair_map[parsed['pair_key']][parsed['stm']] = parsed
    
    proc.wait()
    return results, pair_map

def analyze_board(name, zst_file):
    """Analyze a single board's results."""
    print(f"\n=== {name} ===")
    results, pair_map = load_results(zst_file)
    
    stats = {
        'total': 0, 'legal': 0, 'illegal': 0, 'exact': 0, 'capped': 0,
        'w_wins': 0, 'w_draws': 0, 'w_losses': 0,
        'b_wins': 0, 'b_draws': 0, 'b_losses': 0,
        'w_legal': 0, 'b_legal': 0,
    }
    
    for key, parsed in results.items():
        stats['total'] += 1
        if parsed['illegal']:
            stats['illegal'] += 1
            continue
        stats['legal'] += 1
        if parsed['exact']:
            stats['exact'] += 1
        else:
            stats['capped'] += 1
        
        stm = parsed['stm']
        res = parsed['bound_a']  # Use bound A for statistics
        
        if stm == 'w':
            stats['w_legal'] += 1
            if res == 'W':
                stats['w_wins'] += 1
            elif res == 'D':
                stats['w_draws'] += 1
            elif res == 'L':
                stats['w_losses'] += 1
        else:
            stats['b_legal'] += 1
            if res == 'W':
                stats['b_wins'] += 1
            elif res == 'D':
                stats['b_draws'] += 1
            elif res == 'L':
                stats['b_losses'] += 1
    
    print(f"Total positions: {stats['total']}")
    print(f"  Legal: {stats['legal']}, Illegal: {stats['illegal']}")
    print(f"  Exact: {stats['exact']}, Capped: {stats['capped']}")
    print(f"\nWhite to move ({stats['w_legal']} legal):")
    print(f"  Wins: {stats['w_wins']} ({100*stats['w_wins']/stats['w_legal']:.2f}%)")
    print(f"  Draws: {stats['w_draws']} ({100*stats['w_draws']/stats['w_legal']:.2f}%)")
    print(f"  Losses: {stats['w_losses']} ({100*stats['w_losses']/stats['w_legal']:.2f}%)")
    print(f"\nBlack to move ({stats['b_legal']} legal):")
    print(f"  Wins: {stats['b_wins']} ({100*stats['b_wins']/stats['b_legal']:.2f}%)")
    print(f"  Draws: {stats['b_draws']} ({100*stats['b_draws']/stats['b_legal']:.2f}%)")
    print(f"  Losses: {stats['b_losses']} ({100*stats['b_losses']/stats['b_legal']:.2f}%)")
    
    return stats, pair_map

def compare_boards(cyl_pair_map, flat_pair_map):
    """Compare positions between cylinder and flat boards."""
    print("\n=== Comparison: Cylinder vs Flat ===")
    
    common_keys = set(cyl_pair_map.keys()) & set(flat_pair_map.keys())
    print(f"Common position keys (ignoring stm/ep): {len(common_keys)}")
    
    changes = defaultdict(int)
    mutual_zugzwang_cyl = []
    mutual_zugzwang_flat = []
    cyl_only_mutual_zugzwang = []
    
    for key in common_keys:
        for stm in ('w', 'b'):
            cyl = cyl_pair_map[key].get(stm)
            flat = flat_pair_map[key].get(stm)
            if cyl is None or flat is None:
                continue
            if cyl['illegal'] or flat['illegal']:
                continue
            
            cyl_res = cyl['bound_a']
            flat_res = flat['bound_a']
            
            if cyl_res != flat_res:
                changes[f"{flat_res}->{cyl_res}"] += 1
            
            # Check for mutual zugzwang: side to move does worse than side not to move
            # We need to compare with the other side to move on the same board
            other_stm = 'b' if stm == 'w' else 'w'
            cyl_other = cyl_pair_map[key].get(other_stm)
            flat_other = flat_pair_map[key].get(other_stm)
            
            # Order: L < D < W (from side to move's perspective, but results are from White's view)
            # For White to move: W=win, D=draw, L=loss
            # For Black to move: W=loss, D=draw, L=win
            def outcome_value(res, stm):
                if stm == 'w':
                    return {'L': 0, 'D': 1, 'W': 2}[res]
                else:
                    return {'W': 0, 'D': 1, 'L': 2}[res]
            
            if cyl_other and not cyl_other['illegal']:
                val_stm = outcome_value(cyl_res, stm)
                val_other = outcome_value(cyl_other['bound_a'], other_stm)
                if val_stm < val_other:
                    mutual_zugzwang_cyl.append((key, stm, cyl_res, cyl_other['bound_a'], cyl['full_pos']))
            
            if flat_other and not flat_other['illegal']:
                val_stm = outcome_value(flat_res, stm)
                val_other = outcome_value(flat_other['bound_a'], other_stm)
                if val_stm < val_other:
                    mutual_zugzwang_flat.append((key, stm, flat_res, flat_other['bound_a'], flat['full_pos']))
    
    print(f"\nResult changes (flat -> cylinder):")
    for change, count in sorted(changes.items()):
        print(f"  {change}: {count}")
    total_changes = sum(changes.values())
    print(f"  Total flipped: {total_changes}")
    
    print(f"\nMutual zugzwangs on cylinder: {len(mutual_zugzwang_cyl)}")
    print(f"Mutual zugzwangs on flat: {len(mutual_zugzwang_flat)}")
    
    # Cylinder-only mutual zugzwangs
    cyl_keys_mz = set((k, s) for k, s, _, _, _ in mutual_zugzwang_cyl)
    flat_keys_mz = set((k, s) for k, s, _, _, _ in mutual_zugzwang_flat)
    cyl_only = cyl_keys_mz - flat_keys_mz
    print(f"Cylinder-only mutual zugzwangs: {len(cyl_only)}")
    
    # Get full details for cylinder-only mutual zugzwangs
    for key, stm in cyl_only:
        for item in mutual_zugzwang_cyl:
            if item[0] == key and item[1] == stm:
                cyl_only_mutual_zugzwang.append(item)
                break
    
    return changes, mutual_zugzwang_cyl, mutual_zugzwang_flat, cyl_only_mutual_zugzwang

def spot_check_ref_solver(board_spec, positions, max_checks=200):
    """Spot-check positions using the reference solver."""
    print(f"\n=== Spot check with reference solver on {board_spec} ===")
    
    # Sample positions
    if len(positions) > max_checks:
        sampled = random.sample(positions, max_checks)
    else:
        sampled = positions
    
    # Prepare input for reference solver
    input_lines = [p['full_pos'] for p in sampled]
    input_text = '\n'.join(input_lines) + '\n'
    
    # Run reference solver
    cmd = ['.venv/bin/python', '-m', 'kings.ref.solve', '--board', board_spec, '--ep', 'on', '--promote', 'QRBN', '--cap', '1']
    proc = subprocess.run(cmd, input=input_text, capture_output=True, text=True, cwd='.')
    
    if proc.returncode != 0:
        print(f"Reference solver failed: {proc.stderr}")
        return 0, 0
    
    # Parse output and compare
    agreements = 0
    total = 0
    for line in proc.stdout.strip().split('\n'):
        if not line or line.startswith('#'):
            continue
        if '|' not in line:
            continue
        pos_part, res_part = line.split('|', 1)
        pos_part = pos_part.strip()
        res_part = res_part.strip()
        ref_a, ref_b = res_part.split()[:2]
        
        # Find matching original
        orig = None
        for p in sampled:
            if p['full_pos'] == pos_part:
                orig = p
                break
        if orig is None:
            continue
        
        total += 1
        if orig['bound_a'] == ref_a and orig['bound_b'] == ref_b:
            agreements += 1
        else:
            print(f"  DISAGREE: {pos_part}")
            print(f"    kpsolve: {orig['bound_a']} {orig['bound_b']}")
            print(f"    ref:     {ref_a} {ref_b}")
    
    print(f"Checked {total} positions, {agreements} agree ({100*agreements/total:.1f}%)")
    return agreements, total

def main():
    random.seed(42)
    
    cyl_file = 'research/kpkp/kpkp_cyl.out.zst'
    flat_file = 'research/kpkp/kpkp_flat.out.zst'
    
    cyl_stats, cyl_pairs = analyze_board('Cylinder 8x8', cyl_file)
    flat_stats, flat_pairs = analyze_board('Flat 8x8', flat_file)
    
    changes, mz_cyl, mz_flat, cyl_only_mz = compare_boards(cyl_pairs, flat_pairs)
    
    # Print some cylinder-only mutual zugzwang examples
    print("\n=== Cylinder-only mutual zugzwang examples ===")
    for i, (key, stm, res, other_res, full_pos) in enumerate(cyl_only_mz[:10]):
        print(f"  {i+1}. {full_pos} | {res} {res}")
        print(f"     Other side ({'Black' if stm=='w' else 'White'} to move): {other_res} {other_res}")
    
    # Spot check: 200 random from each board
    print("\n=== Spot checks ===")
    
    # Collect all legal positions for sampling
    cyl_legal = [p for p in cyl_pairs.values() for p in p.values() if p and not p['illegal']]
    flat_legal = [p for p in flat_pairs.values() for p in p.values() if p and not p['illegal']]
    
    spot_check_ref_solver('cyl:8x8', cyl_legal, 200)
    spot_check_ref_solver('flat:8x8', flat_legal, 200)
    
    # Spot check 20 cylinder-only mutual zugzwangs
    if cyl_only_mz:
        spot_check_ref_solver('cyl:8x8', [p for _, _, _, _, p in cyl_only_mz[:20]], 20)

if __name__ == '__main__':
    main()
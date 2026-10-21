#!/usr/bin/env python3
"""Solve KPK positions using kpsolve in batches."""

import subprocess
import sys
import os

def solve_batch(positions, board_type, ep='on', promote='QRBN', cap=1):
    """Solve a batch of positions using kpsolve."""
    input_data = '\n'.join(positions) + '\n'
    
    cmd = [
        os.path.join(os.path.dirname(__file__), '../../kings/kpsolve'),
        '--board', board_type,
        '--ep', ep,
        '--promote', promote,
        '--cap', str(cap)
    ]
    
    result = subprocess.run(cmd, input=input_data, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None
    
    return result.stdout

def parse_result(line):
    """Parse a result line from kpsolve."""
    # Format: "K... P... k... w - | A B" or "K... P... k... w - | X X"
    if '|' not in line:
        return None
    pos_part, res_part = line.split('|', 1)
    pos_part = pos_part.strip()
    res_part = res_part.strip().split()
    if len(res_part) >= 2:
        return pos_part, res_part[0], res_part[1]
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: solve_kpk.py <board_type> <output_file> [batch_size]", file=sys.stderr)
        print("  board_type: flat:8x8 or cyl:8x8", file=sys.stderr)
        sys.exit(1)
    
    board_type = sys.argv[1]
    output_file = sys.argv[2]
    batch_size = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    
    # Generate positions
    gen_cmd = [sys.executable, os.path.join(os.path.dirname(__file__), 'generate_kpk.py')]
    if board_type.startswith('flat'):
        gen_cmd.append('flat')
    
    gen_result = subprocess.run(gen_cmd, capture_output=True, text=True)
    if gen_result.returncode != 0:
        print(f"Generation failed: {gen_result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    positions = gen_result.stdout.strip().split('\n')
    print(f"Total positions: {len(positions)}", file=sys.stderr)
    
    # Solve in batches
    with open(output_file, 'w') as out_f:
        for i in range(0, len(positions), batch_size):
            batch = positions[i:i+batch_size]
            print(f"Solving batch {i//batch_size + 1}/{(len(positions)-1)//batch_size + 1} ({len(batch)} positions)...", file=sys.stderr)
            
            result = solve_batch(batch, board_type)
            if result is None:
                print(f"Failed at batch {i//batch_size + 1}", file=sys.stderr)
                sys.exit(1)
            
            out_f.write(result)
            out_f.flush()
            
            # Progress
            solved = min(i + batch_size, len(positions))
            print(f"  Progress: {solved}/{len(positions)}", file=sys.stderr)
    
    print(f"Done! Results written to {output_file}", file=sys.stderr)

if __name__ == '__main__':
    main()
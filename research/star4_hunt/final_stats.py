#!/usr/bin/env python3
"""Collect the numbers for the T49 report from out/ and logs/."""
import glob, re, os, collections, subprocess, sys
def scan_dir(d):
    c = collections.Counter(); chunks = 0; mex = collections.Counter(); mexmax = collections.Counter()
    for f in glob.glob(d + '/*.tsv'):
        for line in open(f):
            if line.startswith('#summary'):
                chunks += 1
                for tok in line.split():
                    if '=' in tok:
                        k, v = tok.split('=')
                        if re.fullmatch(r'-?\d+', v): c[k] += int(v)
                    m = re.match(r'(m|M)(-?\d+)=(\d+)', tok)
                    if m: (mex if m.group(1) == 'm' else mexmax)[int(m.group(2))] += int(m.group(3))
    return chunks, c, mex, mexmax
def line_for(d):
    chunks, c, mex, mexmax = scan_dir(d)
    n4 = sum(v for k, v in c.items() if re.fullmatch(r'nim([4-9]|\d\d)', k))
    nr4 = sum(c.get('near%d' % i, 0) for i in range(4, 8))
    mm = max([k for k in mex if mex[k]] or [-9])
    return f"{d:14s} chunks={chunks:3d} roots={c['roots']:>12,} states={c['states']:>14,} *0={c['nim0']} *1={c['nim1']} *2={c['nim2']} *3={c['nim3']} >=*4={n4} near3={c['near3']} near>=4={nr4} maxminmex={mm}"
print("== exhaustive single-component scans (default setting)")
for d in sorted(set(glob.glob('out/*p1*') + glob.glob('out/w3all') + glob.glob('out/c6p10'))):
    if os.path.isdir(d): print(line_for(d))
print("== extension / ring runs (histograms)")
for f in sorted(set(glob.glob('out/ext_*.out') + glob.glob('out/r*.out') + glob.glob('out/j*.out') + glob.glob('out/rows_*.out'))):
    txt = open(f).read()
    m = re.search(r'#extend done evals=(\d+)', txt); h = re.search(r'#hist_nim(.*)', txt); n = re.search(r'#hist_near(.*)', txt)
    print(f"{f:34s} evals={m.group(1) if m else 'partial'} nim:{h.group(1).strip() if h else ''} near:{n.group(1).strip() if n else ''}")
print("== duel boards")
for f in sorted(glob.glob('out/duel/*.tsv')):
    t = open(f).read(); m = re.search(r'#duel done (.*)', t)
    print(f, m.group(1) if m else 'partial')
chunks = collections.Counter()
for f in glob.glob('out/duel6/*.tsv'):
    t = open(f).read(); m = re.search(r'#duel done roots=(\d+)(.*)', t)
    if m:
        key = os.path.basename(f).split('_c')[0]; chunks[key + ' chunks'] += 1; chunks[key + ' roots'] += int(m.group(1))
        for k, v in re.findall(r'nim(\d+)=(\d+)', m.group(2)): chunks[key + ' nim' + k] += int(v)
print(dict(chunks))
print("== periodic (2-file period, <=2 pawns per file)")
for f in sorted(glob.glob('out/periodic2_w*.tsv')):
    c = collections.Counter()
    for line in open(f):
        p = line.rstrip('\n').split('\t')
        if len(p) > 4 and p[4].lstrip('-').isdigit(): c['nim' + p[4]] += 1
        elif len(p) > 3: c[p[3]] += 1
    print(f, dict(c))

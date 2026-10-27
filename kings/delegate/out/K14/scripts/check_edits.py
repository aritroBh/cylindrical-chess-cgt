#!/usr/bin/env python3
"""Check EDITS.md: every block has the exact format, every OLD occurs exactly once in the current LOOPY.md, and
the edits apply cleanly (in order, to an in-memory copy; LOOPY.md itself is never written)."""
import re, sys
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
E = open(sys.argv[1] if len(sys.argv) > 1 else 'EDITS.md', encoding='utf-8').read()
text = open(LOOPY, encoding='utf-8').read()
blocks = re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW\n', E, re.S)
print('blocks', len(blocks), 'headers', E.count('### EDIT '))
cur = text
for label, o, n in blocks:
    c = text.count(o)
    assert c == 1, (label, c)
    assert cur.count(o) == 1, ('after earlier edits', label, cur.count(o))
    cur = cur.replace(o, n)
open('/tmp/k14_loopy_after.md', 'w', encoding='utf-8').write(cur)
print('all OLD occur exactly once; applied; new length', len(cur), 'old', len(text))

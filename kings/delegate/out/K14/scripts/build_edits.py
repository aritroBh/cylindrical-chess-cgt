#!/usr/bin/env python3
"""Build EDITS.md (exact format required by the task) from LOOPY.md line ranges and the texts in edit_texts/.
Every OLD is cut out of the current LOOPY.md by line range (1-indexed, inclusive) and checked to occur exactly once."""
import os, sys
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOOPY = '/Users/aritro/Downloads/Research/Chessendgames/kings/theory/LOOPY.md'
text = open(LOOPY, encoding='utf-8').read()
lines = text.split('\n')


def old(a, b):
    s = '\n'.join(lines[a - 1:b])
    assert text.count(s) == 1, (a, b, text.count(s))
    return s


def T(name): return open(os.path.join(D, 'edit_texts', name), encoding='utf-8').read().rstrip('\n')


edits = []


def add(label, o, n):
    assert text.count(o) == 1, label
    edits.append((label, o, n))


# E1 status row
add('status row: shuttles on both sides',
    old(82, 82), T('E1.txt'))
# E2 results table row after C3.5
r = old(184, 184)
add('results table: new row P3.2prime', r, r + '\n' + T('E2.txt'))
# E3 summary bullet
add('summary: both sides can pass', old(161, 162), T('E3.txt'))
# E4 sharp form: D for the bridges
add('sharp form: D for the two-sided bridge', old(559, 559), T('E4.txt'))
# E5 sharp form reading (b): loser that owns a shuttle
add('sharp form: reading (b), a loser that owns a shuttle', old(604, 605), T('E5.txt'))
# E6 P3.2 statement pointer
add('P3.2: pointer to the two-sided version', old(1388, 1389), T('E6.txt'))
# E7 section 3 bullet on both sides
add('section 3: shuttles on both sides', old(1489, 1494), T('E7.txt'))
# E8 the new proposition, inserted before the Literature paragraph
lit = old(1496, 1496)
add('section 3: Proposition 3.2prime and its chess bridge', lit, T('E8_main.txt') + '\n\n' + T('E8_comp.txt') + '\n\n' + lit)
# E9 section 5.3 pawn-break bullet
add('5.3: without the pawn break', old(1735, 1740), T('E9.txt'))
# E10 new section 5.7 before section 6
sec6 = old(1816, 1816)
add('section 5.7 (new): a two-shuttle group', sec6, T('E10_57.txt') + '\n\n' + sec6)
# E11 section 7 downgrade list
add('section 7: downgraded dud claim', old(1967, 1967), T('E11.txt'))
# E12 section 7 item 8
add('section 7 item 8: the 2-cycle bisimulation', old(1951, 1951), T('E12.txt'))
# E13 section 8 item 2
add('section 8 item 2: dud groups', old(1982, 1983), T('E13.txt'))
# E14 appendix A
add('appendix A: no dud group', old(2011, 2011), T('E14.txt'))

out = ['# K14 proposed edits to kings/theory/LOOPY.md', '',
       'Each block replaces its OLD text (which occurs exactly once in the current LOOPY.md) by its NEW text.', '']
for label, o, n in edits:
    out.append('### EDIT ' + label)
    out.append('<<<<<<< OLD')
    out.append(o)
    out.append('=======')
    out.append(n)
    out.append('>>>>>>> NEW')
    out.append('')
open(os.path.join(D, 'EDITS.md'), 'w', encoding='utf-8').write('\n'.join(out))
print('wrote', len(edits), 'edits')

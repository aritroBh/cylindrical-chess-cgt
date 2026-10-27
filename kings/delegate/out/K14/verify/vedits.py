import re
L = open('../../../../theory/LOOPY.md').read()
E = open('../EDITS.md').read()
blocks = re.findall(r'### EDIT (.*?)\n<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW', E, flags=re.S)
print(len(blocks), 'blocks parsed; header count', E.count('### EDIT '))
cur = L
for i, (lab, old, new) in enumerate(blocks, 1):
    c0 = L.count(old); c1 = cur.count(old)
    print(f'{i:2d} {lab[:60]:60s} OLD in original: {c0}, in progressively edited: {c1}, same-as-new: {old==new}')
    if c1 == 1:
        cur = cur.replace(old, new)
open('LOOPY_edited_preview.md', 'w').write(cur)
print(len(L), len(cur))

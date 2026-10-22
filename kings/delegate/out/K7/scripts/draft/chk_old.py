import re,sys
S="/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/k7/"
txt=open(S+"edits_K7.txt").read()
src=open("kings/theory/LOOPY.md").read()
parts=re.split(r'^### EDIT \d+:.*\n',txt,flags=re.M)
hdr=re.findall(r'^### EDIT \d+:.*$',txt,flags=re.M)
print(len(hdr),len(parts))
for h,p in zip(hdr,parts[1:]):
    m=re.search(r'<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',p,re.S)
    old=m.group(1)
    print(h[:40],src.count(old))
new=src
for h,p in zip(hdr,parts[1:]):
    m=re.search(r'<<<<<<< OLD\n(.*?)\n=======\n(.*?)\n>>>>>>> NEW',p,re.S)
    new=new.replace(m.group(1),m.group(2),1)
print("equal to LOOPY_new:", new==open(S+"LOOPY_new.md").read())
# check task text in edits vs key phrases

# Independent (stdlib only) check of small structural facts cited in the notes.
# No repository code imported.

def P_start(n):
    # files 0..n-1
    f = ["W5","B7","W4","W4B7","B6","W3B6"]
    for j in range(6,n):
        f.append("W2" if j%2==0 else "B4")
    return f

def R_start(n):
    f = ["W5","B7"]
    for j in range(2, n-6):  # wall files 2..n-7
        f.append("W2" if j%2==0 else "B4")
    f += ["W3B6","W3","W2B5","B5","W2","B4"]
    assert len(f)==n, (n,len(f))
    return f

def Qo_start(n):
    f = ["W4","B7"]
    for j in range(2, n-6):
        f.append("W2" if j%2==0 else "B4")
    f += ["W3B6","W3","W2B5","B5","W2","B4"]
    assert len(f)==n
    return f

def ins(files, c):
    # insert copies of files[c+1], files[c] after file c
    return files[:c+1] + [files[c+1], files[c]] + files[c+1:]

ok = True
# pawn counts
for n in [8,10,12,14,16,18,20]:
    ps = P_start(n)
    pc = sum(len(x)//2 if False else x.count('W')+x.count('B') for x in ps)  # crude: count letters W/B
    # better count pawns by number of W/B tokens
    def count(s): 
        # tokens like W5, W23, W4B7 => count W and B occurrences
        import re
        return len(re.findall(r'W\d|B\d', s))  # not exact for multi-digit ranks but ranks <=8 here W23 has W2 and? 
    # Use explicit count of pawn symbols by scanning
    def numpawns(s):
        # count uppercase W/B followed by digit(s)
        i=0; cnt=0
        while i < len(s):
            if s[i] in 'WB' and i+1<len(s) and s[i+1].isdigit():
                cnt+=1; i+=2
                while i<len(s) and s[i].isdigit(): i+=1
            else:
                i+=1
        return cnt
    pc = sum(numpawns(x) for x in ps)
    if pc != n+2:
        ok=False; print("P pawn count mismatch", n, pc, n+2)
    print(f"P_{n}: files={len(ps)} pawns={pc} (expected {n+2})")

for n in [11,13,15,17,19]:
    for fam,start in [("R",R_start),("Qo",Qo_start)]:
        fs=start(n); pc=sum(numpawns(x) for x in fs)
        if pc!=n+2:
            ok=False; print(fam, n, "pawn count", pc, n+2)
        else:
            print(f"{fam}_{n}: files={len(fs)} pawns={pc}")

# insertion checks
# Note1: ins_12(start_18) == start_20
p18=P_start(18); p20=P_start(20)
if ins(p18,12)==p20:
    print("ins_12(start_18)==start_20: OK")
else:
    ok=False; print("ins_12(start_18)!=start_20")
    print("got", ins(p18,12))
    print("exp", p20)

# Note3: ins_6(start_19) == start_21 for R and Qo
for fam,start in [("R",R_start),("Qo",Qo_start)]:
    a=start(19); b=start(21)
    if ins(a,6)==b:
        print(f"ins_6({fam}_19)=={fam}_21: OK")
    else:
        ok=False; print(f"ins_6({fam}_19) mismatch")

# cut admissibility
for (n,c,wall_lo,wall_hi,zone_maxpat) in [(18,12,7,17,6),(19,6,2,11,11)]:
    print(f"n={n} c={c}: arc [{c-4},{c+5}], wall [{wall_lo},{wall_hi}], n0 condition c+5<={wall_hi} -> {c+5<=wall_hi}")

# zone sets
print("P_18 zone", sorted([0,2,3,4,5,6]))
print("R_19 zone", sorted(list(range(19-7,19-2)) + [19-1]))
print("Qo_19 zone", sorted([0,1]+list(range(19-7,19-2))+[19-1]))

print("ALL OK" if ok else "FAILURES PRESENT")

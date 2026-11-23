import sys
# contexts: extra pawns on files h, i (indices 7, 8) of cyl:10x6; the over group is on files a, b, e with kings on d, f
groups={
 'over3+3': ("Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5", "Kf5 kd5 Pb2 Pb4 Pe2 pa4 pb5 pe5"),
 'over2+3': ("Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5", "Kg4 kg6 Pb3 Pe2 pa5 pb4 pe5"),
}
ctx={'none':'', 'W1 (Ph5)':'Ph5','W2 (Ph4)':'Ph4','W3 (Ph3)':'Ph3','B1 (ph2)':'ph2','B2 (ph3)':'ph3','B3 (ph4)':'ph4',
     'pair h3h4':'Ph3 ph4','pair h2h3':'Ph2 ph3','race Ph4 pi4':'Ph4 pi4','pairs h3h4 i2i3':'Ph3 ph4 Pi2 pi3'}
out=[]
for g,(r0,r1) in groups.items():
    for c,ps in ctx.items():
        for r in (r0,r1):
            for stm in 'bw':
                pawns=r.split(); k=[t for t in pawns if t[0] in 'Kk']; p=[t for t in pawns if t[0] in 'Pp']
                out.append(("%s %s %s %s"%(" ".join(k)," ".join(p+ps.split()),stm,'-')).replace('  ',' '))
open('ctx_positions.txt','w').write("\n".join(out)+"\n")
print(len(out))

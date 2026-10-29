import sys
for n in ['cyl7x6_f3','flat7x6_f3_z2']:
    ok=bad=0
    for l in open('data/kpp_%s.out'%n):
        z,r=l.rsplit(' | ',1); r=r.split()
        stm=z.split()[-2]
        exp='L' if stm=='w' else 'W'
        if r[0]==exp: ok+=1
        else: bad+=1; print('BAD',l.strip())
    print(n,'lines ok',ok,'bad',bad)

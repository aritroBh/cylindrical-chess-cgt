import json,glob,sys
dec=json.JSONDecoder()
for f in sys.argv[1:]:
    s=open(f).read(); i=0
    while i<len(s):
        while i<len(s) and s[i].isspace(): i+=1
        if i>=len(s): break
        o,j=dec.raw_decode(s,i); i=j
        t=o['total']; keys=('frozen','on','off','dud','over','under')
        d=o.get('distinct_groups',{})
        print(f.split('/')[-1][:-5], o['variant'], o['board'], 'F%d'%o['files'], '%d+%d'%(o['wmax'],o['bmax']), 'passers', o['root_passers'], 'roots', o['roots'], 'selfviol', o.get('selfcheck_violations'), {k:t[k] for k in keys}, 'distinct', {k:d.get(k) for k in keys})

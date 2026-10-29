import subprocess, sys, os
B=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','bin')
def roots(wk, bk, pawns):
    return ['K%s k%s %s %s -'%(w,b,pawns,s) for w in wk for b in bk for s in 'wb']
def leaks(board, wk, bk, pawns, solver):
    L=roots(wk,bk,pawns)
    if solver=='ref3m':
        bd = board.replace(':','') if board.startswith('flat') else board
        cmd=[B+'/ref3m','--board',bd,'--moves']
    else:
        cmd=[B+'/kpp','--board',board,'--ep','on','--promote','QRBN','--cap','1','--pmodel','--moves']
    o=subprocess.run(cmd,input='\n'.join(L)+'\n',capture_output=True,text=True).stdout.split('\n')
    o=[x for x in o if ' | ' in x]
    tot=0; vals=[]
    shut={'w':set(wk),'b':set(bk)}
    for l in o:
        parts=l.split(' | ')
        pos=parts[0].split(); stm=pos[-2]
        rest=parts[-1].split() if solver=='ref3m' else parts[2].split() if len(parts)>2 else []
        rv=parts[1].split()[0]
        vals.append(rv)
        if rv=='X': return None
        lose='L' if stm=='w' else 'W'
        nsh=0
        for tok in rest[1:] if solver=='ref3m' else rest:
            n,v=tok.rsplit(':',1)
            if n[0]=='K' and n[1:3] in shut[stm] and n[3:5] in shut[stm]: nsh+=1; continue
            if v!=lose: tot+=1
        if nsh!=1: return ('nsh',nsh)
    return tot, ''.join(vals)
groups={'ZB':(['b2','c3'],['a4','b5'],'Pa3 Pb4 pb3 pc4'),'ZC':(['c2','c3'],['a4','a5'],'Pa2 Pc4 pa3 pc5'),
        'ZBm':(['a3','b2'],['b5','c4'],'Pb4 Pc3 pa4 pb3')}
boards=sys.argv[2:]
for g in sys.argv[1].split(','):
    for b in boards:
        r1=leaks(b,*groups[g],'ref3m'); r2=leaks(b,*groups[g],'kpp') if not b.split(':')[-1].split('x')[0].isdigit() or int(b.split(':')[-1].split('x')[0])<=8 else None
        print(g,b,'ref3m',r1,'kpp',r2,flush=True)

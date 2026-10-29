import json,collections,sys
from fit import *
tag=sys.argv[1] if len(sys.argv)>1 else 's6'
T=json.load(open(f'data/{tag}_table.json')); rows=[r for r in T['rows'] if r['resolved']]; mrows=T['mrows']
for r in rows: r['fzn_win']=int(r['frozen']=='win'); r['fail']=1-r['zero_holds']
for m in mrows: m['fzn_win']=int(m['fzn_root']=='win'); m['not_loss']=int(m['res']!='loss')
def cvrun(data,feats,yf,mk,idkey='pos'):
    ids=sorted({d[idkey] for d in data}); fold={i:k%5 for k,i in enumerate(ids)}
    conf=collections.Counter()
    for k in range(5):
        tr=[d for d in data if fold[d[idkey]]!=k]; te=[d for d in data if fold[d[idkey]]==k]
        rule,_=mk(tr,feats,yf)
        for d in te: conf[(int(yf(d)),int(rule(d)))]+=1
    n=sum(conf.values()); return dict(acc=(conf[(0,0)]+conf[(1,1)])/n,confusion=dict(TP=conf[(1,1)],FN=conf[(1,0)],FP=conf[(0,1)],TN=conf[(0,0)]))
def mk_stump(tr,feats,yf):
    s=best_stump(tr,feats,[yf(r) for r in tr]); ff,v,pol=s[1],s[2],s[3]
    return (lambda r:(r[ff]<=v)==bool(pol)),(f"{ff}<={v}" if pol else f"not({ff}<={v})")
def mk_pair(tr,feats,yf):
    p=best_pair(tr,feats,[yf(r) for r in tr]); f1,a,g,b,cell=p[1],p[2],p[3],p[4],p[5]
    return (lambda r:bool(cell.get((r[f1]<=a,r[g]<=b),0))),f"[{f1}<={a}] x [{g}<={b}] -> {{{', '.join(f'{k}:{v}' for k,v in sorted(cell.items()))}}}"
def study(name,data,feats,yf,idkey='pos'):
    y=[yf(d) for d in data]; res=dict(n=len(y),positive=sum(y),majority_baseline=max(sum(y),len(y)-sum(y))/len(y))
    for t,mk in (('one_feature',mk_stump),('two_feature',mk_pair)):
        rule,desc=mk(data,feats,yf); pred=[rule(d) for d in data]
        ce={}
        for d,p in zip(data,pred):
            if bool(p)!=bool(yf(d)):
                k=f"h={d['r']}"
                cand=((d['n'],d['pos'],d.get('move','')),dict(pos=d['pos'],move=d.get('move'),truth=int(yf(d)),predicted=int(p),context_pawns=d['n']))
                if k not in ce or cand[0]<ce[k][0]: ce[k]=cand
        res[t]=dict(rule=desc,acc_fit=acc(pred,y),confusion_fit=confusion(pred,y),cv5=cvrun(data,feats,yf,mk,idkey),smallest_counterexample_per_h={k:v[1] for k,v in sorted(ce.items())})
    return res
F_pos=['fa','fb','gapodd','dkm_face','dko_face','nface','mingap','nface_buf','nface_e','npass','null_win','null_loss','r','mir','nW','nB','n','nbuf','dkmover_ctx','dkopp_ctx','dkopp_buf','dkmover_buf','res_mover','res_opp','res_diff','res_tot','fzn_win']
F_mv=F_pos[:-1]+['dest_ctx','dest_opp_pawn','dest_own_pawn','dest_buf','dest_file','fzn_win']
F_mv=[f for f in dict.fromkeys(F_mv)]
out={'positions_resolved':len(rows),'zero_fail':sum(r['fail'] for r in rows)}
out['position_zero_fails']=study('zero_fails',rows,F_pos,lambda r:r['fail'])
out['king_move_not_loss']=study('not_loss',mrows,F_mv,lambda m:m['not_loss'])
mw=[m for m in mrows if m['fzn_win']]
Fw=[f for f in F_mv if f!='fzn_win']
out['king_move_not_loss_given_frozen_win']=study('nl_fw',mw,Fw,lambda m:m['not_loss'])
ml=[m for m in mrows if not m['fzn_win']]
out['king_move_not_loss_given_frozen_loss']=dict(n=len(ml),not_loss=sum(m['not_loss'] for m in ml),examples=[(m['pos'],m['move'],m['res']) for m in ml if m['not_loss']][:20])
json.dump(out,open(f'data/{tag}_fit.json','w'),indent=1)
for k in('position_zero_fails','king_move_not_loss','king_move_not_loss_given_frozen_win'):
    v=out[k]; print(k,v['n'],v['positive'],round(v['majority_baseline'],3))
    for t in('one_feature','two_feature'): print('  ',t,v[t]['rule'],'fit',round(v[t]['acc_fit'],3),v[t]['confusion_fit'],'cv',round(v[t]['cv5']['acc'],3),v[t]['cv5']['confusion'])

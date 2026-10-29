# One- and two-feature rules for "a king move does not lose" on the 275-position suite (1,113 king moves, tablebase truth).
# Leakage guard: nsol and the root result are NOT features (they count/contain the king moves themselves).
import json,collections
from fit import *
rows=json.load(open('data/suite_king_moves.json'))
for r in rows:
    r['isA']=int(r['treb'][0]=='A'); r['cls_hot']=int(r['cls'] in('hot-BIG','switch','decided')); r['cls_num']=int(r['cls']=='number')
FF=json.load(open('data/suite_frozen_feats.json'))
for r in rows:
    f=FF[r['id']]; r['fzn_win']=int(f['fzn_root']=='win'); r['null_win']=int(f['null_res']=='win'); r['null_loss']=int(f['null_res']=='loss')
ids=sorted({r['id'] for r in rows}); fold={i:k%5 for k,i in enumerate(ids)}
feats=['dcomp','dcomp_from','approach','r','maxlen','tempo','isnum','okdist','nW','nB','isA','tofile','cls_hot','cls_num','fzn_win','null_win','null_loss','denemy','down','okd_comp','pred_win','npred']
def mk_stump(tr,yf):
    s=best_stump(tr,feats,[yf(r) for r in tr]); ff,v,pol=s[1],s[2],s[3]
    return (lambda r:(r[ff]<=v)==bool(pol)), (f"{ff}<={v}" if pol else f"not({ff}<={v})")
def mk_pair(tr,yf):
    p=best_pair(tr,feats,[yf(r) for r in tr]); f1,a,g,b,cell=p[1],p[2],p[3],p[4],p[5]
    return (lambda r:bool(cell.get((r[f1]<=a,r[g]<=b),0))), f"[{f1}<={a}] x [{g}<={b}] -> {{{', '.join(f'{k}:{v}' for k,v in sorted(cell.items()))}}}"
def cv(mk,yf):
    conf=collections.Counter()
    for k in range(5):
        tr=[r for r in rows if fold[r['id']]!=k]; te=[r for r in rows if fold[r['id']]==k]
        rule,_=mk(tr,yf)
        for r in te: conf[(int(yf(r)),int(rule(r)))]+=1
    n=sum(conf.values()); return dict(acc=(conf[(0,0)]+conf[(1,1)])/n,confusion=dict(TP=conf[(1,1)],FN=conf[(1,0)],FP=conf[(0,1)],TN=conf[(0,0)]))
out={}
for name,yf in (('king_move_not_loss',lambda r:int(r['res']!='loss')),('king_move_wins',lambda r:int(r['res']=='win'))):
    y=[yf(r) for r in rows]; res=dict(n=len(y),positive=sum(y),majority_baseline=max(sum(y),len(y)-sum(y))/len(y))
    for tag,mk in (('stump',mk_stump),('pair',mk_pair)):
        rule,desc=mk(rows,yf); pred=[rule(r) for r in rows]
        ce={}
        for r,p in zip(rows,pred):
            if bool(p)!=bool(yf(r)):
                key=f"{r['treb']}"
                cand=((r['nW']+r['nB'],r['id'],r['move']),dict(id=r['id'],move=r['move'],truth=r['res'],predicted_not_loss=bool(p),component_pawns=r['nW']+r['nB'],dcomp=r['dcomp'],maxlen=r['maxlen']))
                if key not in ce or cand[0]<ce[key][0]: ce[key]=cand
        res[tag]=dict(rule=desc,acc_fit=acc(pred,y),confusion_fit=confusion(pred,y),cv5=cv(mk,yf),smallest_counterexample_per_layout={k:v[1] for k,v in sorted(ce.items())})
    out[name]=res
# study: given the frozen model says the mover wins
sub=[r for r in rows if r['fzn_win']]
feats_save=list(feats)
res=dict(n=len(sub),positive=sum(r['res']!='loss' for r in sub))
yf=lambda r:int(r['res']!='loss')
feats[:]=[f for f in feats_save if f not in('fzn_win',)]
y=[yf(r) for r in sub]
res['majority_baseline']=max(sum(y),len(y)-sum(y))/len(y)
for tag,mk in (('stump',mk_stump),('pair',mk_pair)):
    rule,desc=mk(sub,yf); pred=[rule(r) for r in sub]
    res[tag]=dict(rule=desc,acc_fit=acc(pred,y),confusion_fit=confusion(pred,y))
out['king_move_not_loss_given_frozen_win']=res
feats[:]=feats_save
json.dump(out,open('data/suite_fit.json','w'),indent=1)
print('given frozen win',res['n'],res['positive'],round(res['majority_baseline'],3),res['stump']['rule'],round(res['stump']['acc_fit'],3),res['stump']['confusion_fit'])
for k,v in out.items():
    print(k,v['n'],v['positive'],round(v['majority_baseline'],3))
    for t in('stump','pair'): print(' ',t,v[t]['rule'],round(v[t]['acc_fit'],3),v[t]['confusion_fit'],'cv',round(v[t]['cv5']['acc'],3) if 'cv5' in v[t] else '-')

import json,sys,os,re
sys.path.insert(0,"/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/scripts"); sys.argv=['x','/tmp/k26neg/out.json']
src=open('/Users/aritro/Downloads/Research/Chessendgames/kings/delegate/out/K26/scripts/confirm_all.py').read()
src=src.replace("groups = json.load(open(os.path.join(LOG, 'exact_groups_all.json')))","groups = [{'id':'ZA','board':'flat:7x6','class':'dud','wk':['a5','a6'],'bk':['c5','c6'],'wp':['b3'],'bp':['b4','b5']},{'id':'ZB_wrongdud','board':'flat:7x7','class':'dud','wk':['b2','c3'],'bk':['a4','b5'],'wp':['a3','b4'],'bp':['b3','c4']}]")
exec(compile(src,'confirm_all_neg','exec'))

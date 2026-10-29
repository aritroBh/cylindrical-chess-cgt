import sys
pos_list=sys.argv[4:]
sys.argv=['x',sys.argv[1],sys.argv[2],sys.argv[3],'1','1','1']
exec(open('behav.py').read().split('if __name__ == "__main__":')[0])
for pos in pos_list:
    root=parse(pos); start,opts=group_graph(root); r=solve_group_sum(start,opts); sig=[]
    for ctx in range(8):
        a,b,c=ctx&1,(ctx>>1)&1,(ctx>>2)&1
        sig.append(r[((a,b,c),0)]+r[((a,b,c),1)])
    print(pos,"| sig "," ".join(sig))

import collections,sys
order=["0","*","+1","-1","+2","-2","+3","-3","1/2","-1/2","up","down","up*","down*","*2","on","off","dud","over","under","tis","tisn","{+|}","{|-}","{+|-}","{+|0}","{0|-}","{1|0}","{0|-1}","{2|0}","{0|-2}","{+|on}","{off|-}","{on|off}"]
def parse(line):
    cn,pos,rest=line.rstrip('\n').split('|',2)
    nm,sh,sig=rest.rsplit('|',2)
    return cn,pos,nm,sh,sig
def show(sig,keys=('0','on','off','dud','+1','-1','over','under','{+|}','{|-}')):
    return ' '.join(o+':'+''.join('WDL'[int(sig[2*i+j])] for j in (0,1)) for i,o in enumerate(order) if o in keys)
if __name__=='__main__':
    f=sys.argv[1]
    c=collections.Counter(); ex={}
    for line in open(f):
        cn,pos,nm,sh,sig=parse(line)
        if nm=='UNMATCHED':
            c[sig]+=1; ex.setdefault(sig,(cn,pos))
    print(len(c),'distinct unmatched signatures')
    for sig,n in c.most_common(int(sys.argv[2]) if len(sys.argv)>2 else 25):
        print(n, ex[sig], show(sig))

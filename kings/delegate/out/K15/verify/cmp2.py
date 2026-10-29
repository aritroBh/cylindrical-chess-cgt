import sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open('cmpmoves.py').read().replace("if k not in b or a[k]!=b[k]:","if k not in b or a[k][1]!=b[k][1] or a[k][0][0]!=b[k][0][0]:"))

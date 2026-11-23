import json,sys
json.dump([[a,'NNPN',b] for a,b in [x.split('=',1) for x in sys.argv[2:]]],open(sys.argv[1],'w'))

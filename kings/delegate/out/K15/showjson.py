import json,sys
def objs(fn):
    txt=open(fn).read(); dec=json.JSONDecoder(); i=0; out=[]
    while True:
        t=txt[i:].lstrip()
        if not t: break
        o,n=dec.raw_decode(t); out.append(o); i=len(txt)-len(t)+n
    return out
if __name__=="__main__":
    for fn in sys.argv[1:]:
        for o in objs(fn):
            print(fn,o["variant"],"layers",o["layers"],"roots",o["roots"]);print("  ",o["total"]);print("  distinct",o["distinct_groups"],"near",o["near_over_roots"],o["near_under_roots"],"viol",o["selfcheck_violations"],"2sided",o["two_sided_shuttle_roots_by_final_class"]["mixed"],o["two_sided_shuttle_roots_by_final_class"]["leak"],o["dud_attempt_failure_reasons"])

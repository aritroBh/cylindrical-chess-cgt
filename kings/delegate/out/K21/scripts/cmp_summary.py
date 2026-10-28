import json, sys
a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
diff = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
print("sections differing:", diff)

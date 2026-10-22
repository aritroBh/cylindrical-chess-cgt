"""Generate ringeval_w.c (128-bit masks) from ringeval.c."""
import re
s = open("ringeval.c").read()
s = s.replace("#ifndef STRIDE\n#define STRIDE 10\n#endif", "#ifndef STRIDE\n#define STRIDE 16\n#endif\ntypedef unsigned __int128 mask_t;\nstatic inline int ctz128(mask_t m) { uint64_t lo = (uint64_t)m; return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(m >> 64)); }")
s = s.replace("static inline uint64_t B(int f, int r) { return UINT64_C(1) << SQ(f, r); }", "static inline mask_t B(int f, int r) { return ((mask_t)1) << SQ(f, r); }")
s = s.replace("static uint64_t frontW[64], frontB[64], filemask[16];", "static mask_t frontW[128], frontB[128], filemask[32];")
for name in ["wm", "bm", "ep3", "ep6", "occ", "mine", "theirs", "rest", "nm", "nt", "nm2", "cep3", "cep6", "base_ep3", "base_ep6", "pawns", "mw", "mb", "m", "ep", "mask",
             "CUR_WM", "CUR_BM", "CUR_EP3", "CUR_EP6", "s_wm", "s_bm", "s_e3", "s_e6"]:
    s = re.sub(r"uint64_t %s\b" % name, "mask_t %s" % name, s)
s = s.replace("uint64_t *mask", "mask_t *mask")
s = s.replace("static uint64_t clear_component_ep(mask_t ep", "static mask_t clear_component_ep(mask_t ep")
s = s.replace("__builtin_ctzll(m)", "ctz128(m)")
s = s.replace("static inline uint64_t mix(uint64_t x) {", "static inline uint64_t mix(uint64_t x);\n#define M64(x) ((uint64_t)(x) ^ mix((uint64_t)((x) >> 64)))\n#define HASH(a,b,c,d) mix(M64(a) ^ mix(M64(b)) ^ mix(M64(c)) ^ mix(M64(d)))\nstatic inline uint64_t mix(uint64_t x) {", 1)
s = re.sub(r"mix\((\w+(?:->\w+|\[\w+\]\.\w+)?) \^ mix\((\w+(?:->\w+|\[\w+\]\.\w+)?)\) \^ mix\((\w+(?:->\w+|\[\w+\]\.\w+)?)\) \^ mix\((\w+(?:->\w+|\[\w+\]\.\w+)?)\)\)", r"HASH(\1, \2, \3, \4)", s)
s = s.replace("typedef struct { uint64_t wm, bm, ep3, ep6; Value val; uint8_t used; } Entry;", "typedef struct { mask_t wm, bm, ep3, ep6; Value val; uint8_t used; } Entry;")
s = s.replace("typedef struct { uint64_t wm, bm, ep3, ep6; uint8_t used; } VEnt;", "typedef struct { mask_t wm, bm, ep3, ep6; uint8_t used; } VEnt;")
s = s.replace("typedef struct { uint64_t wm, bm, ep3, ep6; char desc[40]; int white; } PendingMove;", "typedef struct { mask_t wm, bm, ep3, ep6; char desc[40]; int white; } PendingMove;")
s = s.replace("(6 * STRIDE) > 64", "(6 * STRIDE) > 128")
open("ringeval_w.c", "w").write(s)

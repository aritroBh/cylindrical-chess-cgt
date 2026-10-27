/* rgx.c = rg.c plus: poisoned-child skip in win() (value-neutral), per-position node limit (NODELIM env),
 * table reset between positions when more than 35% full, 'FULL'/'ABORT' output instead of exit(3).
 * Original header follows.
 * rg.c -- independent engine for the whole-board pawn game on the n-file cylinder (8 ranks).
 * Written from the rules in cylcgt/pawns.py's docstrings and COMMON.md, NOT from ringeval.c.
 *
 * Model (default setting): RACE_RULE = count, e.p. on, a pawn that can still be taken e.p. is not passed.
 * Whole-board game: no splitting into components.  A child position with exactly one side holding a passed
 * pawn is a terminal win for that side (value +-BIG in G + *h, i.e. that side wins whoever moves).  A child
 * where both sides hold passed pawns is resolved by the race rule "count".
 *
 * Position text: one token per file, "W23B4" = white pawns on ranks 2,3 and black pawn on rank 4, "-" = empty.
 * Optional trailing "epW=<file>" / "epB=<file>": the white (black) pawn on that file has just double-stepped.
 *
 * Modes (argv[1]):
 *   classify        stdin: positions. For each position and each side, list every move with its class:
 *                   T (terminal win for the mover) / L (terminal loss) / P (poisoned: opponent has an immediate
 *                   terminal win) / K (kept).
 *   reduce          stdin: one position. Build the reduced graph (delete L and P moves) reachable from it and dump.
 *   solve H         stdin: positions. Full game search (no poison pruning) for G+*h, h=0..H; prints N/L/R/P signature.
 *   test            self tests
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>

#ifndef MAXN
#define MAXN 40
#endif
typedef struct {
    uint8_t w[MAXN], b[MAXN];
    int8_t epf;   /* file of the pawn that has just double-stepped and may be taken e.p., else -1 */
    uint8_t eph;  /* holder of the e.p. right: 0 = White may capture (Black double-stepped), 1 = Black */
} Pos;

static int N = 0;                 /* number of files */
static int RACE = 0;              /* 0 count, 1 mover, 2 opponent */
static int EPPASSED = 1;          /* PASSED_RESPECTS_EP */

static inline int fl(int f) { f %= N; if (f < 0) f += N; return f; }
static inline int fm(int f) { return f == 0 ? N - 1 : f - 1; }
static inline int fp(int f) { return f == N - 1 ? 0 : f + 1; }

/* ---- parsing / printing ---- */
static int parse_pos(const char *s, Pos *p) {
    memset(p, 0, sizeof *p);
    p->epf = -1;
    int f = 0;
    char buf[4096]; strncpy(buf, s, sizeof buf - 1); buf[sizeof buf - 1] = 0;
    char *save, *tok = strtok_r(buf, " \t\r\n", &save);
    int epw = -1, epb = -1;
    while (tok) {
        if (!strncmp(tok, "epW=", 4)) epw = atoi(tok + 4);
        else if (!strncmp(tok, "epB=", 4)) epb = atoi(tok + 4);
        else {
            if (f >= MAXN) return -1;
            if (strcmp(tok, "-")) {
                int mode = 0;
                for (char *c = tok; *c; c++) {
                    if (*c == 'W') mode = 1; else if (*c == 'B') mode = 2;
                    else if (*c >= '1' && *c <= '8') { if (mode == 1) p->w[f] |= 1 << (*c - '1'); else if (mode == 2) p->b[f] |= 1 << (*c - '1'); else return -1; }
                    else return -1;
                }
            }
            f++;
        }
        tok = strtok_r(NULL, " \t\r\n", &save);
    }
    if (f == 0) return -1;
    N = f;
    if (epw >= 0) { p->epf = epw; p->eph = 1; }
    if (epb >= 0) { p->epf = epb; p->eph = 0; }
    return f;
}

static void print_pos(FILE *o, const Pos *p) {
    for (int f = 0; f < N; f++) {
        if (f) fputc(' ', o);
        if (!p->w[f] && !p->b[f]) { fputc('-', o); continue; }
        if (p->w[f]) { fputc('W', o); for (int r = 0; r < 8; r++) if (p->w[f] >> r & 1) fputc('1' + r, o); }
        if (p->b[f]) { fputc('B', o); for (int r = 0; r < 8; r++) if (p->b[f] >> r & 1) fputc('1' + r, o); }
    }
    if (p->epf >= 0) fprintf(o, " ep%c=%d", p->eph ? 'W' : 'B', p->epf);
}

/* ---- passed pawns ---- */
/* ep protection: the pawn of the side that does NOT hold the right, sitting on the double-step landing square */
static inline int ep_prot_w(const Pos *p, int f, int r) { return EPPASSED && p->epf == f && p->eph == 1 && r == 4; }
static inline int ep_prot_b(const Pos *p, int f, int r) { return EPPASSED && p->epf == f && p->eph == 0 && r == 5; }

/* is there a passed white (side=0) / black (side=1) pawn?  textbook=1 ignores ep protection */
static int has_passed(const Pos *p, int side, int textbook) {
    for (int f = 0; f < N; f++) {
        unsigned mine = side == 0 ? p->w[f] : p->b[f];
        if (!mine) continue;
        int a = fm(f), c = fp(f);
        for (int r = 1; r <= 8; r++) if (mine >> (r - 1) & 1) {
            int blocked;
            if (side == 0) { unsigned bn = p->b[a] | p->b[f] | p->b[c]; blocked = (bn >> r) != 0; }
            else { unsigned wn = p->w[a] | p->w[f] | p->w[c]; blocked = (wn & ((1u << (r - 1)) - 1)) != 0; }
            if (blocked) continue;
            if (!textbook && (side == 0 ? ep_prot_w(p, f, r) : ep_prot_b(p, f, r))) continue;
            return 1;
        }
    }
    return 0;
}

/* promotion distance for the race rule */
static int pdist(const Pos *p, int side) {
    int best = 1000000;
    for (int f = 0; f < N; f++) {
        unsigned mine = side == 0 ? p->w[f] : p->b[f];
        if (!mine) continue;
        int a = fm(f), c = fp(f);
        unsigned occ = p->w[f] | p->b[f];
        for (int r = 1; r <= 8; r++) if (mine >> (r - 1) & 1) {
            int blocked;
            if (side == 0) { unsigned bn = p->b[a] | p->b[f] | p->b[c]; blocked = (bn >> r) != 0; }
            else { unsigned wn = p->w[a] | p->w[f] | p->w[c]; blocked = (wn & ((1u << (r - 1)) - 1)) != 0; }
            if (blocked) continue;
            if (side == 0 ? ep_prot_w(p, f, r) : ep_prot_b(p, f, r)) continue;
            /* front pawn of its file (any colour ahead disqualifies) */
            if (side == 0) { if (occ >> r) continue; }
            else { if (occ & ((1u << (r - 1)) - 1)) continue; }
            int d = side == 0 ? 8 - r - (r == 2) : r - 1 - (r == 7);
            if (d < best) best = d;
        }
    }
    return best;
}

/* class of a child position c reached by `mover` (0 = W, 1 = B): +1 mover wins at once, -1 mover loses at once, 0 non-terminal */
static int cls(const Pos *c, int mover) {
    int wp = has_passed(c, 0, 0), bp = has_passed(c, 1, 0);
    if (!wp && !bp) return 0;
    if (wp && bp) {
        int winner;
        if (RACE == 1) winner = mover;
        else if (RACE == 2) winner = 1 - mover;
        else { int o = 1 - mover; winner = (pdist(c, o) <= pdist(c, mover)) ? o : mover; }
        return winner == mover ? 1 : -1;
    }
    int holder = wp ? 0 : 1;
    return holder == mover ? 1 : -1;
}

/* ---- move generation ---- */
typedef struct { int sf, sr, df, dr; char kind; /* '-', 'x', 'e' (e.p.), 'd' double */ } Mv;

static int gen(const Pos *p, int side, Pos *out, Mv *mv) {
    int k = 0;
    int d = side == 0 ? 1 : -1, start = side == 0 ? 2 : 7;
    int ep_here = (p->epf >= 0 && p->eph == side);
    int ep_tr = side == 0 ? 6 : 3;     /* e.p. target rank for the holder */
    for (int f = 0; f < N; f++) {
        unsigned mine = side == 0 ? p->w[f] : p->b[f];
        if (!mine) continue;
        for (int r = 1; r <= 8; r++) if (mine >> (r - 1) & 1) {
            int r1 = r + d;
            if (r1 < 1 || r1 > 8) continue;
            unsigned occ1 = p->w[f] | p->b[f];
            if (!(occ1 >> (r1 - 1) & 1)) {
                Pos q = *p; q.epf = -1;
                if (side == 0) { q.w[f] &= ~(1u << (r - 1)); q.w[f] |= 1u << (r1 - 1); }
                else { q.b[f] &= ~(1u << (r - 1)); q.b[f] |= 1u << (r1 - 1); }
                out[k] = q; mv[k] = (Mv){f, r, f, r1, '-'}; k++;
                int r2 = r + 2 * d;
                if (r == start && !(occ1 >> (r2 - 1) & 1)) {
                    Pos q2 = *p; q2.epf = -1;
                    if (side == 0) { q2.w[f] &= ~(1u << (r - 1)); q2.w[f] |= 1u << (r2 - 1); }
                    else { q2.b[f] &= ~(1u << (r - 1)); q2.b[f] |= 1u << (r2 - 1); }
                    /* e.p. right exists only if an enemy pawn stands beside the landing square */
                    unsigned en = side == 0 ? (p->b[fm(f)] | p->b[fp(f)]) : (p->w[fm(f)] | p->w[fp(f)]);
                    if (en >> (r2 - 1) & 1) { q2.epf = f; q2.eph = 1 - side; }
                    out[k] = q2; mv[k] = (Mv){f, r, f, r2, 'd'}; k++;
                }
            }
            for (int s = -1; s <= 1; s += 2) {
                int g = s < 0 ? fm(f) : fp(f);
                unsigned theirs = side == 0 ? p->b[g] : p->w[g];
                if (theirs >> (r1 - 1) & 1) {
                    Pos q = *p; q.epf = -1;
                    if (side == 0) { q.w[f] &= ~(1u << (r - 1)); q.w[g] |= 1u << (r1 - 1); q.b[g] &= ~(1u << (r1 - 1)); }
                    else { q.b[f] &= ~(1u << (r - 1)); q.b[g] |= 1u << (r1 - 1); q.w[g] &= ~(1u << (r1 - 1)); }
                    out[k] = q; mv[k] = (Mv){f, r, g, r1, 'x'}; k++;
                } else if (ep_here && p->epf == g && r1 == ep_tr) {
                    /* e.p.: the enemy pawn that double-stepped stands beside us on rank r, file g */
                    Pos q = *p; q.epf = -1;
                    if (side == 0) { q.w[f] &= ~(1u << (r - 1)); q.w[g] |= 1u << (r1 - 1); q.b[g] &= ~(1u << (r - 1)); }
                    else { q.b[f] &= ~(1u << (r - 1)); q.b[g] |= 1u << (r1 - 1); q.w[g] &= ~(1u << (r - 1)); }
                    out[k] = q; mv[k] = (Mv){f, r, g, r1, 'e'}; k++;
                }
            }
        }
    }
    return k;
}

#define MAXMV 256
/* poisoned: after `mover` has moved to c (non-terminal), does the opponent have a move to a terminal win for him? */
static int poisoned(const Pos *c, int mover) {
    Pos ch[MAXMV]; Mv mv[MAXMV];
    int opp = 1 - mover;
    int k = gen(c, opp, ch, mv);
    for (int i = 0; i < k; i++) if (cls(&ch[i], opp) == 1) return 1;
    return 0;
}

/* ---- hash set of positions ---- */
static uint64_t hashpos(const Pos *p) {
    uint64_t h = 1469598103934665603ULL;
    for (int f = 0; f < N; f++) { h ^= p->w[f]; h *= 1099511628211ULL; h ^= p->b[f] + 0x100; h *= 1099511628211ULL; }
    h ^= (uint64_t)(p->epf + 2) * 31 + p->eph; h *= 1099511628211ULL;
    h ^= h >> 29;
    return h;
}
static int eqpos(const Pos *a, const Pos *b) {
    return a->epf == b->epf && (a->epf < 0 || a->eph == b->eph) && !memcmp(a->w, b->w, N) && !memcmp(a->b, b->b, N);
}

typedef struct { Pos *pos; int cap, n; int *tab; int tcap; } PSet;
static void ps_init(PSet *s) { s->cap = 1024; s->n = 0; s->pos = malloc(sizeof(Pos) * s->cap); s->tcap = 1 << 12; s->tab = malloc(sizeof(int) * s->tcap); memset(s->tab, -1, sizeof(int) * s->tcap); }
static int ps_find(PSet *s, const Pos *p, int add) {
    uint64_t h = hashpos(p); int i = h & (s->tcap - 1);
    while (s->tab[i] >= 0) { if (eqpos(&s->pos[s->tab[i]], p)) return s->tab[i]; i = (i + 1) & (s->tcap - 1); }
    if (!add) return -1;
    if (s->n == s->cap) { s->cap *= 2; s->pos = realloc(s->pos, sizeof(Pos) * s->cap); }
    s->pos[s->n] = *p; s->tab[i] = s->n; s->n++;
    if (s->n * 2 > s->tcap) {
        s->tcap *= 2; free(s->tab); s->tab = malloc(sizeof(int) * s->tcap); memset(s->tab, -1, sizeof(int) * s->tcap);
        for (int j = 0; j < s->n; j++) { int k = hashpos(&s->pos[j]) & (s->tcap - 1); while (s->tab[k] >= 0) k = (k + 1) & (s->tcap - 1); s->tab[k] = j; }
    }
    return s->n - 1;
}

static void print_mv(FILE *o, const Mv *m) {
    if (m->kind == '-' || m->kind == 'd') fprintf(o, "%d.%d>%d.%d", m->sf, m->sr, m->df, m->dr);
    else fprintf(o, "%d.%d>%d.%d%s", m->sf, m->sr, m->df, m->dr, m->kind == 'e' ? "ep" : "x");
}

/* ---- classify mode ---- */
static void do_classify(const char *line) {
    Pos p; if (parse_pos(line, &p) < 0) { puts("ERR"); return; }
    printf("POS "); print_pos(stdout, &p); printf("\n");
    printf("PASSED %d %d\n", has_passed(&p, 0, 0), has_passed(&p, 1, 0));
    for (int side = 0; side < 2; side++) {
        Pos ch[MAXMV]; Mv mv[MAXMV];
        int k = gen(&p, side, ch, mv);
        for (int i = 0; i < k; i++) {
            int c = cls(&ch[i], side);
            char code = c == 1 ? 'T' : c == -1 ? 'L' : poisoned(&ch[i], side) ? 'P' : 'K';
            printf("%c %c ", side ? 'B' : 'W', code); print_mv(stdout, &mv[i]);
            printf(" => "); print_pos(stdout, &ch[i]);
            printf(" | pp=%d%d\n", has_passed(&ch[i], 0, 0), has_passed(&ch[i], 1, 0));
        }
    }
    printf("END\n");
}

/* ---- reduce mode ---- */
static void do_reduce(const char *line, int quiet) {
    Pos p; if (parse_pos(line, &p) < 0) { puts("ERR"); return; }
    PSet S; ps_init(&S);
    ps_find(&S, &p, 1);
    long ndel_loss = 0, ndel_poison = 0;
    for (int i = 0; i < S.n; i++) {
        Pos cur = S.pos[i];
        printf("NODE %d ", i); print_pos(stdout, &cur); printf("\n");
        for (int side = 0; side < 2; side++) {
            Pos ch[MAXMV]; Mv mv[MAXMV];
            int k = gen(&cur, side, ch, mv);
            for (int j = 0; j < k; j++) {
                int c = cls(&ch[j], side);
                if (c == 1) { printf("E %c T ", side ? 'B' : 'W'); print_mv(stdout, &mv[j]); printf("\n"); continue; }
                if (c == -1) { ndel_loss++; continue; }
                if (poisoned(&ch[j], side)) { ndel_poison++; continue; }
                int id = ps_find(&S, &ch[j], 1);
                printf("E %c %d ", side ? 'B' : 'W', id); print_mv(stdout, &mv[j]); printf("\n");
            }
        }
    }
    printf("STAT nodes=%d deleted_loss=%ld deleted_poison=%ld\n", S.n, ndel_loss, ndel_poison);
    (void)quiet;
}

/* ---- full solver (no poison pruning) ---- */
typedef struct { Pos p; int8_t h; int8_t side; int8_t res; int8_t nf; } Ent;
static Ent *tab = NULL; static size_t tcap = 0, tcount = 0;
static uint64_t hashent(const Pos *p, int h, int s) { return hashpos(p) * 0x9E3779B97F4A7C15ULL + (uint64_t)h * 131 + s * 7919 + (uint64_t)N * 104729; }
static long long nodes_visited = 0;
static long long node_limit = 0;      /* 0 = none; per position (all h, both sides) */
static int aborted = 0;               /* 1 = node limit hit, 2 = table full */

static void tab_clear(void) {
    for (size_t i = 0; i < tcap; i++) tab[i].res = -1;
    tcount = 0;
}

static int win(const Pos *p, int h, int side) {
    if (aborted) return 0;
    uint64_t hh = hashent(p, h, side);
    size_t i = hh & (tcap - 1);
    while (tab[i].res >= 0) {
        if (tab[i].h == h && tab[i].side == side && tab[i].nf == N && eqpos(&tab[i].p, p)) return tab[i].res;
        i = (i + 1) & (tcap - 1);
    }
    nodes_visited++;
    if (node_limit && nodes_visited > node_limit) { aborted = 1; return 0; }
    Pos ch[MAXMV]; Mv mv[MAXMV]; int cl[MAXMV];
    int k = gen(p, side, ch, mv);
    int result = 0;
    for (int j = 0; j < k && !result; j++) { cl[j] = cls(&ch[j], side); if (cl[j] == 1) result = 1; }
    if (!result) {
        /* captures first */
        for (int pass = 0; pass < 2 && !result; pass++)
            for (int j = 0; j < k && !result; j++) {
                if (cl[j] != 0) continue;
                int cap = (mv[j].kind == 'x' || mv[j].kind == 'e');
                if ((pass == 0) != cap) continue;
                if (poisoned(&ch[j], side)) continue;   /* opponent wins at once: this move cannot win (value-neutral skip) */
                if (!win(&ch[j], h, 1 - side)) result = 1;
                if (aborted) return 0;
            }
    }
    for (int h2 = 0; h2 < h && !result; h2++) { if (!win(p, h2, 1 - side)) result = 1; if (aborted) return 0; }
    if (aborted) return 0;
    i = hh & (tcap - 1);
    while (tab[i].res >= 0) i = (i + 1) & (tcap - 1);
    tab[i].p = *p; tab[i].h = h; tab[i].side = side; tab[i].res = result; tab[i].nf = N; tcount++;
    if (tcount * 10 > tcap * 7) { aborted = 2; return 0; }
    return result;
}

static void do_solve(const char *line, int H) {
    Pos p; if (parse_pos(line, &p) < 0) { puts("ERR"); return; }
    nodes_visited = 0; aborted = 0;
    if (tcount * 100 > tcap * 35) tab_clear();
    char sig[64]; int m = 0;
    for (int h = 0; h <= H; h++) {
        int l = win(&p, h, 0), r = win(&p, h, 1);
        if (aborted) break;
        sig[m++] = l && r ? 'N' : l ? 'L' : r ? 'R' : 'P';
    }
    sig[m] = 0;
    if (aborted) { printf("%s nodes=%lld\n", aborted == 1 ? "ABORT" : "FULL", nodes_visited); tab_clear(); return; }
    printf("%s nodes=%lld\n", sig, nodes_visited);
}

static int real_main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage\n"); return 1; }
    const char *mode = argv[1];
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--race")) RACE = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--noep")) EPPASSED = 0;
    }
    char line[8192];
    if (!strcmp(mode, "solve")) {
        int H = argc > 2 && argv[2][0] != '-' ? atoi(argv[2]) : 2;
        node_limit = getenv("NODELIM") ? atoll(getenv("NODELIM")) : 0;
        tcap = 1ULL << (getenv("TBITS") ? atoi(getenv("TBITS")) : 21); tab = malloc(tcap * sizeof(Ent));
        for (size_t i = 0; i < tcap; i++) tab[i].res = -1;
        while (fgets(line, sizeof line, stdin)) {
            if (line[0] == '#' || line[0] == '\n') continue;
            /* clear table between positions only if a different N */
            do_solve(line, H); fflush(stdout);
        }
        return 0;
    }
    while (fgets(line, sizeof line, stdin)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        if (!strcmp(mode, "classify")) do_classify(line);
        else if (!strcmp(mode, "reduce")) do_reduce(line, 0);
        fflush(stdout);
    }
    return 0;
}

static int g_argc; static char **g_argv; static int g_ret;
static void *thr(void *a) { (void)a; g_ret = real_main(g_argc, g_argv); return NULL; }
int main(int argc, char **argv) {
    g_argc = argc; g_argv = argv;
    pthread_attr_t at; pthread_attr_init(&at); pthread_attr_setstacksize(&at, (size_t)1 << 30);
    pthread_t t; pthread_create(&t, &at, thr, NULL); pthread_join(t, NULL);
    return g_ret;
}

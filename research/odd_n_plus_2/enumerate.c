#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 11
#define MAXOPTS 300

typedef struct { uint8_t w, b; unsigned char n; } Col;
static Col opts[MAXOPTS], board[MAXN];
static int nfiles, width, target, white_rank, phase;
static long long roots, no_passers, canonical;

static int pop8(unsigned x) { return __builtin_popcount(x); }
static int dprio(int d) { return d == 2 ? 0 : d == 1 ? 1 : 2; }

static void make_opts(void) {
    for (unsigned m = 1; m < (1u << 12); ++m) {
        int n = pop8(m);
        if (n > 3) continue;
        Col c = {0, 0, (unsigned char)n};
        for (int r = 0; r < 6; ++r) {
            if (m & (1u << (2*r))) c.w |= 1u << (r + 2);
            if (m & (1u << (2*r + 1))) c.b |= 1u << (r + 2);
        }
        opts[roots++] = c;
    }
    roots = 0;
}

static int center_ok(Col a, Col c, Col z) {
    unsigned bw = a.b | c.b | z.b;
    unsigned ww = a.w | c.w | z.w;
    for (int r = 2; r <= 7; ++r) {
        if ((c.w & (1u << r)) && (bw >> (r + 1)) == 0) return 0;
        if ((c.b & (1u << r)) && !(ww & ((1u << r) - 1u))) return 0;
    }
    return 1;
}

static int desc_key_less(int w1, int d1, int r1, int p1,
                         int w2, int d2, int r2, int p2) {
    if (w1 != w2) return w1 < w2;
    if (dprio(d1) != dprio(d2)) return dprio(d1) < dprio(d2);
    if (r1 != r2) return r1 < r2;
    return p1 < p2;
}

/* Return the preferred wall description for a board whose core begins at file 0. */
static int find_desc(const Col *v, int *ow, int *od, int *orr, int *op) {
    int found = 0;
    for (int w = 4; w <= 7 && w < nfiles; ++w) {
        int ok = 1;
        for (int f = 0; f < w; ++f) if (!(v[f].w | v[f].b)) ok = 0;
        if (!ok) continue;
        int k = nfiles - w;
        for (int d = 1; d <= 3; ++d) for (int r = 2; r <= 5; ++r) {
            if (r + d > 7) continue;
            for (int p = 0; p <= 1; ++p) {
                int match = 1;
                for (int j = 0; j < k; ++j) {
                    int isw = ((j + p) % 2 == 0);
                    unsigned wm = isw ? (1u << r) : 0;
                    unsigned bm = isw ? 0 : (1u << (r + d));
                    if (v[w + j].w != wm || v[w + j].b != bm) { match = 0; break; }
                }
                if (match && (!found || desc_key_less(w,d,r,p,*ow,*od,*orr,*op))) {
                    found = 1; *ow = w; *od = d; *orr = r; *op = p;
                }
            }
        }
    }
    return found;
}

static uint8_t flip_rank(uint8_t x) {
    uint8_t y = 0;
    for (int r = 1; r <= 8; ++r) if (x & (1u << r)) y |= 1u << (9-r);
    return y;
}

static int colcmp(Col a, Col b) {
    if (a.w != b.w) return a.w < b.w ? -1 : 1;
    if (a.b != b.b) return a.b < b.b ? -1 : 1;
    return 0;
}

static int candidate_is_canonical(int cw, int cd, int cr, int cp) {
    Col t[MAXN];
    int best_w = cw, best_d = cd, best_r = cr, best_p = cp;
    for (int refl = 0; refl <= 1; ++refl) for (int rot = 0; rot < nfiles; ++rot)
        for (int color = 0; color <= 1; ++color) {
            for (int j = 0; j < nfiles; ++j) {
                int src = refl ? (rot - j + nfiles) % nfiles : (rot + j) % nfiles;
                t[j] = board[src];
                if (color) {
                    uint8_t oldw = t[j].w;
                    t[j].w = flip_rank(t[j].b);
                    t[j].b = flip_rank(oldw);
                }
            }
            int w,d,r,p;
            if (!find_desc(t,&w,&d,&r,&p)) continue;
            int cmp = 0;
            for (int j = 0; j < nfiles && !cmp; ++j) cmp = colcmp(t[j], board[j]);
            if (desc_key_less(w,d,r,p,best_w,best_d,best_r,best_p) ||
                (!desc_key_less(best_w,best_d,best_r,best_p,w,d,r,p) && cmp < 0)) {
                best_w = w; best_d = d; best_r = r; best_p = p;
            }
        }
    if (best_w != cw || best_d != cd || best_r != cr || best_p != cp) return 0;
    for (int refl = 0; refl <= 1; ++refl) for (int rot = 0; rot < nfiles; ++rot)
        for (int color = 0; color <= 1; ++color) {
            for (int j = 0; j < nfiles; ++j) {
                int src = refl ? (rot - j + nfiles) % nfiles : (rot + j) % nfiles;
                t[j] = board[src];
                if (color) {
                    uint8_t oldw = t[j].w;
                    t[j].w = flip_rank(t[j].b);
                    t[j].b = flip_rank(oldw);
                }
            }
            int w,d,r,p;
            if (!find_desc(t,&w,&d,&r,&p) || w != cw || d != cd || r != cr || p != cp) continue;
            int cmp = 0;
            for (int j = 0; j < nfiles && !cmp; ++j) cmp = colcmp(t[j], board[j]);
            if (cmp < 0) return 0;
        }
    return 1;
}

static void emit_pos(int d, int p) {
    printf("RING\t%d\t%d\t%d\t%d\t", width, d, white_rank, p);
    for (int f = 0; f < nfiles; ++f) {
        if (f) putchar(' ');
        if (!board[f].w && !board[f].b) { putchar('-'); continue; }
        if (board[f].w) {
            putchar('W');
            for (int r = 1; r <= 8; ++r) if (board[f].w & (1u << r)) putchar('0' + r);
        }
        if (board[f].b) {
            putchar('B');
            for (int r = 1; r <= 8; ++r) if (board[f].b & (1u << r)) putchar('0' + r);
        }
    }
    putchar('\n');
}

static void finish_candidate(int d, int p) {
    ++no_passers;
    if (!candidate_is_canonical(width,d,white_rank,p)) return;
    ++canonical;
    emit_pos(d,p);
}

static void dfs(int f, int used, int d, int p) {
    int rem = width - f;
    if (used + rem > target || used + 3*rem < target) return;
    if (f == width) {
        if (used != target) return;
        Col wall_last = board[nfiles - 1];
        if (!center_ok(wall_last, board[0], board[1])) return;
        if (!center_ok(board[width - 2], board[width - 1], board[width])) return;
        for (int j = width; j < nfiles; ++j)
            if (!center_ok(board[(j+nfiles-1)%nfiles], board[j], board[(j+1)%nfiles])) return;
        ++roots;
        finish_candidate(d,p);
        return;
    }
    for (int i = 0; i < MAXOPTS; ++i) {
        Col c = opts[i];
        if (!c.n) continue;
        if (used + c.n > target) continue;
        board[f] = c;
        if (f >= 2 && !center_ok(board[f-2],board[f-1],board[f])) continue;
        dfs(f+1,used+c.n,d,p);
    }
}

static void run_template(int d, int r, int p) {
    if (r + d > 7) return;
    white_rank = r; phase = p; target = width + 2;
    memset(board,0,sizeof board);
    for (int j = 0; j < nfiles-width; ++j) {
        int isw = ((j + p) % 2 == 0);
        if (isw) board[width+j].w = 1u << r;
        else board[width+j].b = 1u << (r+d);
    }
    for (int j = width + 1; j < nfiles - 1; ++j)
        if (!center_ok(board[(j+nfiles-1)%nfiles],board[j],board[(j+1)%nfiles])) return;
    dfs(0,0,d,p);
}

int main(int argc, char **argv) {
    if (argc != 3 && argc != 6) { fprintf(stderr,"usage: enumerate N W [D R P]\n"); return 2; }
    nfiles = atoi(argv[1]); width = atoi(argv[2]);
    if ((nfiles != 8 && nfiles != 9) || width < 4 || width > 7 || width >= nfiles) return 2;
    int fd = argc == 6 ? atoi(argv[3]) : 0;
    int fr = argc == 6 ? atoi(argv[4]) : 0;
    int fp = argc == 6 ? atoi(argv[5]) : -1;
    if (argc == 6 && (fd < 1 || fd > 3 || fr < 2 || fr > 5 || fp < 0 || fp > 1)) return 2;
    make_opts();
    long long total_roots = 0, total_nopass = 0, total_canonical = 0;
    for (int d = 1; d <= 3; ++d) if (!fd || d == fd)
      for (int r = 2; r <= 5; ++r) if ((!fr || r == fr) && r+d <= 7)
        for (int p = 0; p <= 1; ++p) if (fp < 0 || p == fp) {
            roots = no_passers = canonical = 0;
            run_template(d,r,p);
            total_roots += roots; total_nopass += no_passers; total_canonical += canonical;
        }
    fprintf(stderr,"STATS N=%d w=%d filter=%d,%d,%d roots=%lld no_passers=%lld canonical=%lld\n",
            nfiles,width,fd,fr,fp,total_roots,total_nopass,total_canonical);
    return 0;
}

/*
 * cylperft.c -- perft for standard chess on the flat board and on the 8-file cylinder
 * (files a and h adjacent; ranks not joined).  Mailbox, no bitboards, written for checking,
 * not speed.
 *
 * Rules (plan B0, engine/FAIRY_CYLINDER.md section 2):
 *   - every file step wraps modulo 8 on the cylinder: king, knight, pawn captures, e.p., sliders;
 *   - a slider ray stops at the first occupied square and never returns to its own square
 *     (at most 7 steps), so there is no "rook pass";
 *   - a move is identified by (from, to, promotion piece): a square reachable along two routes
 *     (east and west on a rank; the two helices when |drank| = |dfile| = 4) is ONE move;
 *   - castling is the flat-board rule (king e1->g1/c1 with the rook from h1/a1, the squares between
 *     them empty, the king's start, transit and target squares not attacked); attacks are cylinder
 *     attacks;
 *   - legality: play the pseudo-legal move and reject it if the mover's king is then attacked.
 *
 * Build:  cc -O2 -o engine/perft/cylperft engine/perft/cylperft.c
 * Usage:  cylperft flat|cyl DEPTH "FEN"            perft
 *         cylperft flat|cyl DEPTH "FEN" divide     per-move counts
 *         cylperft flat|cyl DEPTH "FEN" stats      nodes, captures, e.p., castles, promotions, checks, mates
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { EMPTY = 0, PAWN = 1, KNIGHT, BISHOP, ROOK, QUEEN, KING };
#define BLACKBIT 8
#define TYPE(p) ((p) & 7)
#define COLOR(p) ((p) >> 3) /* 0 white, 1 black (only for non-empty) */

static int WRAP = 0;

typedef struct {
    unsigned char sq[64];
    int stm;   /* 0 white, 1 black */
    int castle; /* bit0 K, bit1 Q, bit2 k, bit3 q */
    int ep;    /* square or -1 */
} Pos;

typedef struct {
    unsigned char from, to, promo, flags; /* flags: 1 capture, 2 ep, 4 castle, 8 double push */
} Move;

static int step(int s, int df, int dr) {
    int f = (s & 7) + df, r = (s >> 3) + dr;
    if (r < 0 || r > 7) return -1;
    if (WRAP) f = ((f % 8) + 8) % 8;
    else if (f < 0 || f > 7) return -1;
    return r * 8 + f;
}

static const int KN[8][2] = {{1, 2}, {2, 1}, {2, -1}, {1, -2}, {-1, -2}, {-2, -1}, {-2, 1}, {-1, 2}};
static const int KG[8][2] = {{1, 0}, {1, 1}, {0, 1}, {-1, 1}, {-1, 0}, {-1, -1}, {0, -1}, {1, -1}};
static const int RD[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
static const int BD[4][2] = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};

/* is square s attacked by colour c ? */
static int attacked(const Pos *p, int s, int c) {
    int i, k, t;
    /* pawns: a pawn of colour c on t attacks s if s = t + (+-1, forward) */
    int back = c == 0 ? -1 : 1; /* from s, the attacking pawn stands one rank "behind" */
    for (i = -1; i <= 1; i += 2) {
        t = step(s, i, back);
        if (t >= 0 && p->sq[t] == (PAWN | (c ? BLACKBIT : 0))) return 1;
    }
    for (i = 0; i < 8; i++) {
        t = step(s, KN[i][0], KN[i][1]);
        if (t >= 0 && p->sq[t] == (KNIGHT | (c ? BLACKBIT : 0))) return 1;
        t = step(s, KG[i][0], KG[i][1]);
        if (t >= 0 && p->sq[t] == (KING | (c ? BLACKBIT : 0))) return 1;
    }
    for (i = 0; i < 4; i++) {
        for (k = 1; k <= 7; k++) {
            t = step(s, RD[i][0] * k, RD[i][1] * k);
            if (t < 0 || t == s) break;
            if (p->sq[t]) {
                int q = p->sq[t];
                if (COLOR(q) == c && (TYPE(q) == ROOK || TYPE(q) == QUEEN)) return 1;
                break;
            }
        }
        for (k = 1; k <= 7; k++) {
            t = step(s, BD[i][0] * k, BD[i][1] * k);
            if (t < 0 || t == s) break;
            if (p->sq[t]) {
                int q = p->sq[t];
                if (COLOR(q) == c && (TYPE(q) == BISHOP || TYPE(q) == QUEEN)) return 1;
                break;
            }
        }
    }
    return 0;
}

static int king_sq(const Pos *p, int c) {
    for (int s = 0; s < 64; s++)
        if (p->sq[s] == (KING | (c ? BLACKBIT : 0))) return s;
    return -1;
}

static int nmoves;
static void add(Move *ml, int from, int to, int promo, int flags) {
    for (int i = 0; i < nmoves; i++) /* merge moves reached along two routes */
        if (ml[i].from == from && ml[i].to == to && ml[i].promo == promo) return;
    ml[nmoves].from = from;
    ml[nmoves].to = to;
    ml[nmoves].promo = promo;
    ml[nmoves].flags = flags;
    nmoves++;
}

static void add_pawn(Move *ml, int from, int to, int flags) {
    int r = to >> 3;
    if (r == 0 || r == 7) {
        for (int pr = KNIGHT; pr <= QUEEN; pr++) add(ml, from, to, pr, flags);
    } else
        add(ml, from, to, 0, flags);
}

static int gen(const Pos *p, Move *ml) {
    int c = p->stm, s, i, k, t;
    nmoves = 0;
    for (s = 0; s < 64; s++) {
        int q = p->sq[s];
        if (!q || COLOR(q) != c) continue;
        switch (TYPE(q)) {
        case PAWN: {
            int fwd = c == 0 ? 1 : -1, start = c == 0 ? 1 : 6;
            t = step(s, 0, fwd);
            if (t >= 0 && !p->sq[t]) {
                add_pawn(ml, s, t, 0);
                int t2 = step(s, 0, 2 * fwd);
                if ((s >> 3) == start && !p->sq[t2]) add(ml, s, t2, 0, 8);
            }
            for (i = -1; i <= 1; i += 2) {
                t = step(s, i, fwd);
                if (t < 0) continue;
                if (p->sq[t] && COLOR(p->sq[t]) != c) add_pawn(ml, s, t, 1);
                else if (t == p->ep) add(ml, s, t, 0, 1 | 2);
            }
            break;
        }
        case KNIGHT:
        case KING:
            for (i = 0; i < 8; i++) {
                t = TYPE(q) == KNIGHT ? step(s, KN[i][0], KN[i][1]) : step(s, KG[i][0], KG[i][1]);
                if (t < 0 || t == s) continue;
                if (!p->sq[t]) add(ml, s, t, 0, 0);
                else if (COLOR(p->sq[t]) != c) add(ml, s, t, 0, 1);
            }
            break;
        default: {
            int ty = TYPE(q);
            for (int set = 0; set < 2; set++) {
                if (set == 0 && ty == BISHOP) continue;
                if (set == 1 && ty == ROOK) continue;
                const int (*D)[2] = set == 0 ? RD : BD;
                for (i = 0; i < 4; i++)
                    for (k = 1; k <= 7; k++) {
                        t = step(s, D[i][0] * k, D[i][1] * k);
                        if (t < 0 || t == s) break;
                        if (!p->sq[t]) add(ml, s, t, 0, 0);
                        else {
                            if (COLOR(p->sq[t]) != c) add(ml, s, t, 0, 1);
                            break;
                        }
                    }
            }
        }
        }
    }
    /* castling, flat definition; attacks are topology-aware */
    int e = c == 0 ? 4 : 60, opp = 1 - c;
    if (p->sq[e] == (KING | (c ? BLACKBIT : 0))) {
        int kbit = c == 0 ? 1 : 4, qbit = c == 0 ? 2 : 8;
        int rook = ROOK | (c ? BLACKBIT : 0);
        if ((p->castle & kbit) && p->sq[e + 3] == rook && !p->sq[e + 1] && !p->sq[e + 2] &&
            !attacked(p, e, opp) && !attacked(p, e + 1, opp) && !attacked(p, e + 2, opp))
            add(ml, e, e + 2, 0, 4);
        if ((p->castle & qbit) && p->sq[e - 4] == rook && !p->sq[e - 1] && !p->sq[e - 2] &&
            !p->sq[e - 3] && !attacked(p, e, opp) && !attacked(p, e - 1, opp) && !attacked(p, e - 2, opp))
            add(ml, e, e - 2, 0, 4);
    }
    return nmoves;
}

static void make(const Pos *p, const Move *m, Pos *n) {
    *n = *p;
    int c = p->stm, q = p->sq[m->from];
    n->sq[m->to] = m->promo ? (m->promo | (c ? BLACKBIT : 0)) : q;
    n->sq[m->from] = EMPTY;
    if (m->flags & 2) { /* e.p.: the captured pawn stands behind the target square */
        int victim = step(m->to, 0, c == 0 ? -1 : 1);
        n->sq[victim] = EMPTY;
    }
    if (m->flags & 4) { /* castling: move the rook */
        if (m->to > m->from) { n->sq[m->from + 1] = n->sq[m->from + 3]; n->sq[m->from + 3] = EMPTY; }
        else { n->sq[m->from - 1] = n->sq[m->from - 4]; n->sq[m->from - 4] = EMPTY; }
    }
    n->ep = (m->flags & 8) ? (m->from + m->to) / 2 : -1;
    /* castling rights */
    static const int lose[64] = {
        [0] = 2, [4] = 3, [7] = 1, [56] = 8, [60] = 12, [63] = 4};
    n->castle &= ~(lose[m->from] | lose[m->to]);
    n->stm = 1 - c;
}

static int legal_moves(const Pos *p, Move *out) {
    Move ml[256];
    int n = gen(p, ml), k = 0;
    for (int i = 0; i < n; i++) {
        Pos q;
        make(p, &ml[i], &q);
        if (!attacked(&q, king_sq(&q, p->stm), q.stm)) out[k++] = ml[i];
    }
    return k;
}

typedef struct { unsigned long long nodes, caps, ep, castles, promos, checks, mates; } Stats;

static unsigned long long perft(const Pos *p, int d, Stats *st) {
    Move ml[256];
    int n = legal_moves(p, ml);
    if (d == 0) return 1;
    if (d == 1 && !st) return n;
    unsigned long long tot = 0;
    for (int i = 0; i < n; i++) {
        Pos q;
        make(p, &ml[i], &q);
        if (d == 1) {
            st->nodes++;
            if (ml[i].flags & 1) st->caps++;
            if (ml[i].flags & 2) st->ep++;
            if (ml[i].flags & 4) st->castles++;
            if (ml[i].promo) st->promos++;
            if (attacked(&q, king_sq(&q, q.stm), p->stm)) {
                Move tmp[256];
                st->checks++;
                if (legal_moves(&q, tmp) == 0) st->mates++;
            }
            tot++;
        } else
            tot += perft(&q, d - 1, st);
    }
    return tot;
}

static int parse_fen(const char *fen, Pos *p) {
    memset(p, 0, sizeof *p);
    p->ep = -1;
    char board[100], stm[4], cas[8], ep[4];
    if (sscanf(fen, "%99s %3s %7s %3s", board, stm, cas, ep) < 4) return 0;
    int r = 7, f = 0;
    for (char *c = board; *c; c++) {
        if (*c == '/') { r--; f = 0; continue; }
        if (*c >= '1' && *c <= '8') { f += *c - '0'; continue; }
        const char *pcs = "PNBRQK";
        const char *x = strchr(pcs, *c >= 'a' ? *c - 32 : *c);
        if (!x) return 0;
        p->sq[r * 8 + f] = (unsigned char)((x - pcs + 1) | (*c >= 'a' ? BLACKBIT : 0));
        f++;
    }
    p->stm = stm[0] == 'b';
    for (char *c = cas; *c; c++)
        p->castle |= *c == 'K' ? 1 : *c == 'Q' ? 2 : *c == 'k' ? 4 : *c == 'q' ? 8 : 0;
    if (ep[0] != '-') p->ep = (ep[1] - '1') * 8 + (ep[0] - 'a');
    return 1;
}

static void sqname(int s, char *b) { b[0] = 'a' + (s & 7); b[1] = '1' + (s >> 3); b[2] = 0; }

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "usage: %s flat|cyl DEPTH FEN [divide|stats]\n", argv[0]);
        return 2;
    }
    WRAP = strcmp(argv[1], "cyl") == 0;
    int d = atoi(argv[2]);
    Pos p;
    if (!parse_fen(argv[3], &p)) { fprintf(stderr, "bad FEN\n"); return 2; }
    const char *mode = argc > 4 ? argv[4] : "";
    if (!strcmp(mode, "divide")) {
        Move ml[256];
        int n = legal_moves(&p, ml);
        unsigned long long tot = 0;
        for (int i = 0; i < n; i++) {
            Pos q;
            make(&p, &ml[i], &q);
            unsigned long long c = d > 1 ? perft(&q, d - 1, NULL) : 1;
            char a[3], b[3];
            sqname(ml[i].from, a);
            sqname(ml[i].to, b);
            printf("%s%s%s %llu\n", a, b, ml[i].promo ? (const char[]){" nbrq"[ml[i].promo - 1], 0} : "", c);
            tot += c;
        }
        printf("total %llu\n", tot);
    } else if (!strcmp(mode, "stats")) {
        Stats st = {0};
        if (d < 1) return 2;
        perft(&p, d, &st);
        printf("nodes %llu captures %llu ep %llu castles %llu promotions %llu checks %llu mates %llu\n", st.nodes,
               st.caps, st.ep, st.castles, st.promos, st.checks, st.mates);
    } else
        printf("%llu\n", perft(&p, d, NULL));
    return 0;
}

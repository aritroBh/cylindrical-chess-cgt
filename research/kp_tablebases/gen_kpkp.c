#include <stdio.h>
#include <stdint.h>

#define FILES 8
#define RANKS 8
#define N (FILES * RANKS)

static uint64_t king_attacks_flat[N];
static uint64_t king_attacks_cyl[N];
static uint64_t pawn_att_w_flat[N];
static uint64_t pawn_att_w_cyl[N];
static uint64_t pawn_att_b_flat[N];
static uint64_t pawn_att_b_cyl[N];

static inline int sq_f(int sq) { return sq % FILES; }
static inline int sq_r(int sq) { return sq / FILES; }
static inline const char* sq_name(int sq) {
    static char buf[3];
    buf[0] = 'a' + sq_f(sq);
    buf[1] = '1' + sq_r(sq);
    buf[2] = 0;
    return buf;
}

void precompute() {
    for (int sq = 0; sq < N; sq++) {
        int f = sq_f(sq), r = sq_r(sq);
        uint64_t kf = 0, kc = 0, pwf = 0, pwc = 0, pbf = 0, pbc = 0;
        
        // King attacks
        for (int df = -1; df <= 1; df++) {
            for (int dr = -1; dr <= 1; dr++) {
                if (df == 0 && dr == 0) continue;
                int nf = f + df, nr = r + dr;
                if (nr < 0 || nr >= RANKS) continue;
                if (nf >= 0 && nf < FILES) kf |= 1ULL << (nr * FILES + nf);
                nf = (nf % FILES + FILES) % FILES;
                kc |= 1ULL << (nr * FILES + nf);
            }
        }
        king_attacks_flat[sq] = kf;
        king_attacks_cyl[sq] = kc;
        
        // White pawn attacks
        for (int df = -1; df <= 1; df += 2) {
            int nf = f + df, nr = r + 1;
            if (nr < RANKS) {
                if (nf >= 0 && nf < FILES) pwf |= 1ULL << (nr * FILES + nf);
                nf = (nf % FILES + FILES) % FILES;
                pwc |= 1ULL << (nr * FILES + nf);
            }
        }
        pawn_att_w_flat[sq] = pwf;
        pawn_att_w_cyl[sq] = pwc;
        
        // Black pawn attacks
        for (int df = -1; df <= 1; df += 2) {
            int nf = f + df, nr = r - 1;
            if (nr >= 0) {
                if (nf >= 0 && nf < FILES) pbf |= 1ULL << (nr * FILES + nf);
                nf = (nf % FILES + FILES) % FILES;
                pbc |= 1ULL << (nr * FILES + nf);
            }
        }
        pawn_att_b_flat[sq] = pbf;
        pawn_att_b_cyl[sq] = pbc;
    }
}

int main(int argc, char** argv) {
    int wrap = (argc <= 1 || argv[1][0] != 'f');
    uint64_t *king_att = wrap ? king_attacks_cyl : king_attacks_flat;
    uint64_t *pawn_w = wrap ? pawn_att_w_cyl : pawn_att_w_flat;
    uint64_t *pawn_b = wrap ? pawn_att_b_cyl : pawn_att_b_flat;
    
    precompute();
    
    // Valid pawn squares (ranks 2-7, indices 8-55)
    int valid_pawns[48], n_valid = 0;
    for (int sq = 0; sq < N; sq++) {
        if (sq_r(sq) >= 1 && sq_r(sq) <= 6) valid_pawns[n_valid++] = sq;
    }
    
    long long count = 0;
    
    for (int wk = 0; wk < N; wk++) {
        uint64_t wk_att = king_att[wk];
        for (int i1 = 0; i1 < n_valid; i1++) {
            int wp1 = valid_pawns[i1];
            if (wp1 == wk) continue;
            for (int i2 = i1 + 1; i2 < n_valid; i2++) {
                int wp2 = valid_pawns[i2];
                if (wp2 == wk) continue;
                
                uint64_t white_pawn_att = pawn_w[wp1] | pawn_w[wp2];
                
                for (int bk = 0; bk < N; bk++) {
                    if (bk == wk || bk == wp1 || bk == wp2) continue;
                    if (wk_att & (1ULL << bk)) continue;  // Kings adjacent
                    if (white_pawn_att & (1ULL << bk)) continue;  // BK in check from WP
                    
                    uint64_t bk_att = king_att[bk];
                    if (bk_att & (1ULL << wk)) continue;  // Kings adjacent (redundant)
                    
                    for (int i3 = 0; i3 < n_valid; i3++) {
                        int bp = valid_pawns[i3];
                        if (bp == wk || bp == wp1 || bp == wp2 || bp == bk) continue;
                        if (pawn_b[bp] & (1ULL << wk)) continue;  // WK in check from BP
                        
                        // Both sides to move
                        for (int stm = 0; stm < 2; stm++) {
                            if (stm == 0) { // White to move, Black just moved
                                if (bk_att & (1ULL << wk)) continue;
                                if (pawn_b[bp] & (1ULL << wk)) continue;
                            } else { // Black to move, White just moved
                                if (wk_att & (1ULL << bk)) continue;
                                if (white_pawn_att & (1ULL << bk)) continue;
                            }
                            
                            printf("K%s P%s P%s k%s p%s %c -\n",
                                   sq_name(wk), sq_name(wp1), sq_name(wp2),
                                   sq_name(bk), sq_name(bp), stm ? 'b' : 'w');
                            count++;
                        }
                    }
                }
            }
        }
    }
    
    fprintf(stderr, "Total: %lld legal KPKP positions (wrap=%d)\n", count, wrap);
    return 0;
}

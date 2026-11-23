// Independent whole-board verifier. Bit s is rank 1+s/files, file s%files.
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint32_t Bits;
typedef struct { unsigned short win[2]; } Outcomes;  // side-to-move wins
enum { WHITE, BLACK, NO_EP = 31, HEAPS = 9, ALL = (1 << HEAPS)-1 };
static int files, ranks, wrap;
static Bits first_file, last_file, adjacent[31], home[2];
static int advance[2], distance_to_goal[2][31];
static Bits bit(int i) { return 1u << i; }
static int lowest(Bits b) { return __builtin_ctz(b); }
static int highest(Bits b) { return 31-__builtin_clz(b); }

static void board(int f, int r, int cylinder) {
    files=f; ranks=r; wrap=cylinder;
    first_file=0;
    for (int y=0; y<r; y++) first_file |= bit(y*f);
    last_file=first_file << (f-1);
    for (int s=0; s<f*r; s++) {
        int x=s%f, y=s/f;
        adjacent[s]=0;
        if (x || wrap) adjacent[s] |= bit(y*f+(x+f-1)%f);
        if (x+1<f || wrap) adjacent[s] |= bit(y*f+(x+1)%f);
        distance_to_goal[WHITE][s]=r-1-y-(y==1);
        distance_to_goal[BLACK][s]=y-(y==r-2);
    }
    advance[WHITE]=f; advance[BLACK]=-f;
    home[WHITE]=(bit(f)-1)<<f; home[BLACK]=(bit(f)-1)<<((r-2)*f);
}

// Mark squares behind an enemy on the same or either neighboring file.
static Bits passed(Bits own, Bits enemy, int side, int ep) {
    Bits near=enemy | ((enemy & ~last_file)<<1) | ((enemy & ~first_file)>>1);
    if (wrap) near |= ((enemy & first_file)<<(files-1)) | ((enemy & last_file)>>(files-1));
    Bits covered=side==WHITE ? near>>files : near<<files;
    for (int d=1; d<ranks-1; d*=2) {
        if (side==WHITE) covered |= covered>>(d*files);
        else covered |= covered<<(d*files);
    }
    return own & ~covered & ~bit(ep); // ep is the capturable victim, never the skipped square
}

// ponytail: one exact-key entry per bucket; collisions cost recomputation only.
// Increase the table for wider scans if the miss rate becomes expensive.
enum { BUCKETS = 1<<22 };
static struct Entry { Bits white, black; int ep; Outcomes result; } *cache;
static struct Entry *bucket(Bits w, Bits b, int ep) {
    uint64_t h=((uint64_t)w<<32) | b;
    h ^= (uint64_t)ep*UINT64_C(0x9e3779b97f4a7c15);
    h ^= h>>30; h *= UINT64_C(0xbf58476d1ce4e5b9);
    return &cache[(h^(h>>31)) & (BUCKETS-1)];
}

static Outcomes solve(Bits w, Bits b, int ep, int mover);

static unsigned pawn_option(Bits own, Bits foe, int side, int ep) {
    Outcomes child = side==WHITE ? solve(own,foe,ep,side) : solve(foe,own,ep,side);
    return ALL ^ child.win[1-side];
}

static Outcomes solve(Bits w, Bits b, int ep, int mover) {
    struct Entry *slot=bucket(w,b,ep);
    if (slot->ep==ep && slot->white==w && slot->black==b) return slot->result;
    Bits pw=passed(w,b,WHITE,ep), pb=passed(b,w,BLACK,ep);
    Outcomes result={{0,0}};
    if (pw || pb) {
        int winner=pw ? WHITE : BLACK;
        if (pw && pb) {
            assert(mover==WHITE || mover==BLACK);
            int dw=distance_to_goal[WHITE][highest(pw)], db=distance_to_goal[BLACK][lowest(pb)];
            winner=dw==db ? 1-mover : (dw<db ? WHITE : BLACK);
        }
        result.win[winner]=ALL;
        return result; // a tied terminal depends on the last mover, so never cache it
    }
    Bits occupied=w|b;
    for (int side=WHITE; side<=BLACK; side++) {
        Bits own=side==WHITE ? w : b, foe=side==WHITE ? b : w;
        int step=advance[side];
        for (Bits todo=own; todo && result.win[side]!=ALL; todo &= todo-1) {
            int s=lowest(todo);
            Bits base=own^bit(s), forward=bit(s+step);
            if (!(forward & occupied)) {
                result.win[side] |= pawn_option(base|forward,foe,side,NO_EP);
                if ((bit(s)&home[side]) && !(bit(s+2*step)&occupied)) {
                    int dest=s+2*step;
                    int victim=(adjacent[dest]&foe) ? dest : NO_EP;
                    result.win[side] |= pawn_option(base|bit(dest),foe,side,victim);
                }
            }
            Bits captures=adjacent[s+step]&foe;
            for (; captures; captures &= captures-1) {
                Bits target=bit(lowest(captures));
                result.win[side] |= pawn_option(base|target,foe^target,side,NO_EP);
            }
            if (bit(ep)&foe&adjacent[s])
                result.win[side] |= pawn_option(base|bit(ep+step),foe^bit(ep),side,NO_EP);
        }
    }
    // A heap move wins iff some smaller heap loses for the opponent.
    for (int h=1; h<HEAPS; h++) {
        for (int side=WHITE; side<=BLACK; side++) {
            unsigned smaller=bit(h)-1;
            if ((result.win[1-side]&smaller)!=smaller) result.win[side] |= bit(h);
        }
    }
    for (int side=WHITE; side<=BLACK; side++)
        assert(!!(result.win[side]&bit(7)) == !!(result.win[side]&bit(8)));
    *slot=(struct Entry){w,b,ep,result};
    return result;
}

static int signature(Outcomes v, char out[9]) {
    int k=-1;
    for (int h=0; h<8; h++) {
        int index=!!(v.win[WHITE]&bit(h)) + 2*!!(v.win[BLACK]&bit(h));
        out[h]="PLRN"[index];
        if (index==0) { assert(k==-1); k=h; }
    }
    out[8]='\0';
    if (k>=0) for (int h=0; h<8; h++) assert(h==k || out[h]=='N');
    return k;
}

// One ternary digit per interior square of a file (empty, White, Black).
enum { MAX_FILES=5, COLUMN_CODES=243 }; // scans use at most five interior ranks
static Bits column_w[COLUMN_CODES], column_b[COLUMN_CODES];
static int reversed[COLUMN_CODES], columns[MAX_FILES], codes;
static int canonical(void) {
    for (int flip=0; flip<2; flip++) {
        for (int direction=-1; direction<=1; direction+=2) {
            int starts=wrap ? files : 1;
            for (int i=0; i<starts; i++) {
                int x=wrap || direction==1 ? i : files-1;
                for (int j=0; j<files; j++) {
                    int v=columns[x];
                    if (flip) v=reversed[v];
                    if (v<columns[j]) return 0;
                    if (v>columns[j]) break;
                    x=(x+direction+files)%files;
                }
            }
        }
    }
    return 1;
}

static long roots, counts[8];
static int by_split;
static long split_roots[21][11], split_nimbers[21][11][8];
static int minimum[8];
static void enumerate(int x, Bits w, Bits b) {
    if (x==files) {
        if (passed(w,b,WHITE,NO_EP) || passed(b,w,BLACK,NO_EP) || !canonical()) return;
        char out[9];
        int k=signature(solve(w,b,NO_EP,-1),out);
        if (by_split) { // full material audit of C5 at R=6, at most 20 squares
            int nw=__builtin_popcount(w), nb=__builtin_popcount(b);
            int smaller=nw<nb ? nw : nb;
            split_roots[nw+nb][smaller]++;
            if (k>=0) split_nimbers[nw+nb][smaller][k]++;
        }
        roots++;
        if (k>=0) {
            counts[k]++;
            int n=__builtin_popcount(w|b);
            if (!minimum[k] || n<minimum[k]) minimum[k]=n;
        }
        return;
    }
    for (int v=1; v<codes; v++) {
        if (wrap && x && v<columns[0]) continue; // some rotation starts with v
        if (!(column_w[v]|column_b[v])) continue;
        columns[x]=v;
        enumerate(x+1,w|(column_w[v]<<x),b|(column_b[v]<<x));
    }
}

static void scan(void) {
    codes=1;
    for (int y=1; y<ranks-1; y++) codes*=3;
    assert(codes<=COLUMN_CODES);
    for (int v=1; v<codes; v++) {
        int digits=v, rev=0;
        Bits w=0,b=0;
        for (int y=1; y<ranks-1; y++) {
            int d=digits%3;
            digits/=3;
            if (d==1) w |= bit(y*files);
            if (d==2) b |= bit(y*files);
            rev=3*rev+(d ? 3-d : 0);
        }
        reversed[v]=rev;
        if ((w&home[BLACK]) || (b&home[WHITE])) continue;
        column_w[v]=w; column_b[v]=b;
    }
    enumerate(0,0,0);
    if (by_split) {
        for (int n=0; n<=20; n++) for (int a=0; a<=n/2; a++) {
            if (!split_roots[n][a]) continue;
            printf("%d %d %ld",a,n-a,split_roots[n][a]);
            for (int k=0; k<8; k++) printf(" %ld",split_nimbers[n][a][k]);
            putchar('\n');
        }
        return;
    }
    printf("%d %s%d %ld",ranks,wrap?"C":"F",files,roots);
    for (int k=0; k<8; k++) printf(" %ld",counts[k]);
    printf(" %d %d\n",minimum[2],minimum[3]);
}

static Bits squares(const char *s) {
    Bits mask=0;
    while (*s) {
        int x=s[0]-'a', y=s[1]-'1';
        assert(x>=0 && x<files && y>0 && y<ranks-1);
        assert(!(mask & bit(y*files+x)));
        mask |= bit(y*files+x);
        s+=2;
        if (*s) { assert(*s==' '); s++; }
    }
    return mask;
}

static void examples(void) {
    static const struct { int f,r,c; const char *w,*b; int k; } cases[]={
        {4,6,0,"a2 b2 d2","a5 c5 d5",2}, {4,6,0,"a2 d2 b3","c4 a5 d5",2},
        {4,6,1,"c2 d2 a3","b4 c5 d5",2}, {3,7,0,"a2 c2","c3 b6",2},
        {3,7,1,"c2 a3","b5 c5",2}, {4,7,0,"a2 c2","d4 b6",2},
        {4,7,0,"a2 c2 d3","c3 b6 c6",3}, {3,9,1,"a2 b2 c2","a8 b8 c8",2}
    };
    for (size_t i=0; i<sizeof(cases)/sizeof(cases[0]); i++) {
        board(cases[i].f,cases[i].r,cases[i].c);
        memset(cache,0,BUCKETS*sizeof(*cache));
        Bits w=squares(cases[i].w), b=squares(cases[i].b);
        assert(!(w&b) && !passed(w,b,WHITE,NO_EP) && !passed(b,w,BLACK,NO_EP));
        char out[9];
        int k=signature(solve(w,b,NO_EP,-1),out);
        printf("%d %s%d | %s / %s | %s\n",ranks,wrap?"C":"F",files,cases[i].w,cases[i].b,out);
        assert(k==cases[i].k);
    }
}

int main(int argc, char **argv) {
    int named=argc==2 && !strcmp(argv[1],"examples");
    by_split=argc==2 && !strcmp(argv[1],"splits");
    if (by_split) board(5,6,1);
    else if (!named) {
        if (argc!=3 || strlen(argv[1])!=2 || !strchr("FC",argv[1][0]) ||
            argv[1][1]<'3' || argv[1][1]>'5' || strlen(argv[2])!=1 ||
            argv[2][0]<'5' || argv[2][0]>'7') {
            fputs("usage: check examples | check splits | check {F3,F4,C3,C4,C5} {5,6,7}\n",stderr);
            return 2;
        }
        int f=argv[1][1]-'0', r=argv[2][0]-'0', c=argv[1][0]=='C';
        if ((!c && f==5) || (r==7 && f!=3)) return 2;
        board(f,r,c);
    }
    cache=calloc(BUCKETS,sizeof(*cache));
    if (!cache) { perror("cache"); return 1; }
    if (named) examples(); else scan();
    free(cache);
    return 0;
}

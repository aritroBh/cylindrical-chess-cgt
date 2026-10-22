/* Auditor B: independent product solver, naive Kleene iteration (no counters, no predecessor lists).
   usage: v_mask graph.txt games.txt mode mask.txt > results.txt
   mode 0 normal play, 1 chess rule, 4 chess rule with an OPTIONAL spare move at a stalemate (the stalemated mover may claim the draw or move in T),
   5 spare-blind stalemate (no chess move and not in check = draw at once, whatever T offers)
   mask.txt: one line of n chars '0'/'1': moves in T are only allowed at nodes with '1' (n = number of graph nodes)
   graph.txt: n, then per node: stm incheck flip deg succ...
   games.txt: ng, then per game: name nt start, then per node: nl l... nr r...
   output: per game one line "name <string of n chars W/D/L (White's view) for state (node, start)>" */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
    FILE *fg = fopen(argv[1], "r"), *ft = fopen(argv[2], "r");
    int sd = atoi(argv[3]);
    FILE *fm = fopen(argv[4], "r");
    int n; fscanf(fg, "%d", &n);
    int *stm = malloc(4*n), *chk = malloc(4*n), *flip = malloc(4*n), *deg = malloc(4*n), **succ = malloc(sizeof(int*)*n);
    for (int i = 0; i < n; i++) {
        fscanf(fg, "%d %d %d %d", &stm[i], &chk[i], &flip[i], &deg[i]);
        succ[i] = malloc(4*(deg[i]+1));
        for (int k = 0; k < deg[i]; k++) fscanf(fg, "%d", &succ[i][k]);
    }
    char *mask = malloc(n + 2); fscanf(fm, "%s", mask);
    int ng; fscanf(ft, "%d", &ng);
    for (int g = 0; g < ng; g++) {
        char name[256]; int nt, start;
        fscanf(ft, "%s %d %d", name, &nt, &start);
        int *no[2], **op[2];
        op[0] = malloc(sizeof(int*)*nt); op[1] = malloc(sizeof(int*)*nt);
        no[0] = malloc(4*nt); no[1] = malloc(4*nt);
        for (int t = 0; t < nt; t++) {
            for (int s = 0; s < 2; s++) {
                fscanf(ft, "%d", &no[s][t]);
                op[s][t] = malloc(4*(no[s][t]+1));
                for (int k = 0; k < no[s][t]; k++) fscanf(ft, "%d", &op[s][t][k]);
            }
        }
        long N = (long)n * nt;
        char *mw = calloc(N, 1), *ml = calloc(N, 1);
        int changed = 1, sweeps = 0;
        while (changed) {
            changed = 0; sweeps++;
            for (int c = 0; c < n; c++) {
                int s = stm[c];
                for (int t = 0; t < nt; t++) {
                    long u = (long)c*nt + t;
                    if (mw[u] || ml[u]) continue;
                    if (sd == 5 && deg[c] == 0 && !chk[c]) continue;        /* spare-blind stalemate: no chess move and not in check = draw at once, whatever T offers */
                    int any_move = 0, any_losing_succ = 0, all_winning = 1;
                    for (int k = 0; k < deg[c]; k++) {
                        long v = (long)succ[c][k]*nt + t;
                        any_move = 1;
                        if (ml[v]) any_losing_succ = 1;
                        if (!mw[v]) all_winning = 0;
                    }
                    if (flip[c] >= 0 && mask[c] == '1') {
                        for (int k = 0; k < no[s][t]; k++) {
                            long v = (long)flip[c]*nt + op[s][t][k];
                            any_move = 1;
                            if (ml[v]) any_losing_succ = 1;
                            if (!mw[v]) all_winning = 0;
                        }
                    }
                    if (any_losing_succ) { mw[u] = 1; changed = 1; }
                    else if (sd == 4 && deg[c] == 0 && !chk[c]) continue;   /* optional spare move: the stalemated mover may claim the draw */
                    else if (!any_move) {
                        /* no legal move in the sum.  In check: mover loses.  Not in check (stalemate): sd 0 loses, sd 1 draws */
                        if (sd == 1 && !chk[c]) continue;
                        ml[u] = 1; changed = 1;
                    }
                    else if (all_winning) { ml[u] = 1; changed = 1; }
                }
            }
        }
        printf("%s ", name);
        for (int c = 0; c < n; c++) {
            long u = (long)c*nt + start; int s = stm[c];
            char r = 'D';
            if (mw[u]) r = (s == 0) ? 'W' : 'L';
            else if (ml[u]) r = (s == 0) ? 'L' : 'W';
            putchar(r);
        }
        printf(" sweeps=%d\n", sweeps);
        fflush(stdout);
        free(mw); free(ml);
        for (int t = 0; t < nt; t++) { free(op[0][t]); free(op[1][t]); }
        free(op[0]); free(op[1]); free(no[0]); free(no[1]);
    }
    return 0;
}

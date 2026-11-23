/* mring N P [i k] : print the Moebius root rings (canonical reps), chunk i of k. mring N P --count */
#include <stdlib.h>
#include "mring.h"
static int PRINT = 1;
static void cb(const uint8_t *w, const uint8_t *b, void *ctx) { (void)ctx; if (!PRINT) return; char s[1024]; mr_format(s, w, b, MN); puts(s); }
int main(int argc, char **argv) {
    if (argc < 3) return 1; mr_init(); int ci = 0, ck = 1;
    for (int i = 3; i < argc; i++) { if (!strcmp(argv[i], "--count")) PRINT = 0; else if (i + 1 < argc) { ci = atoi(argv[i]); ck = atoi(argv[i + 1]); i++; } }
    long c = mr_enum(atoi(argv[1]), atoi(argv[2]), ci, ck, cb, NULL);
    fprintf(stderr, "rings %ld\n", c); return 0; }

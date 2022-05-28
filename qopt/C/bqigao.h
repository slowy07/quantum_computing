#ifndef _BQIGAO_H
#define _BQIGAO_H 1

#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <ctime>
#include <cstring>
#include <sys/time.h>
#include "framework.h"

#define EPSILON 10e-9f
#undef M_PI
#undef M_PI_2
#undef M_PI_4
#define M_PI 3.145926535897932384f
#define M_PI_2 1.57079632679489661923f
#define M_PI_4 0.78539816339744830962f
#define M_S2 0.70710678118654757f

class BQIGAo {
    public:
        int tmax;

        const int popsize;
        const int chromlen;

        float *Q;
        char **P;
        float *fvals;
        char *best;

        float bestval;

        float lookup_table[2][2][2];

        float signs_table[2][2][2][4];

        Problem<char, float> *problem;

        BQIGAo(int chromlen, int popsize) : popsize(popsize), chromlen(chromlen) {
            printf("BIGAo::BQIGAo constructor\n");

            tmax = 500;
            problem = NULL;

            Q = new float[popsize * chromlen * 2];
            fvals = new float[popsize];
            best = new char[chromlen];

            P = new char *[popsize];

            for (int i = 0; i < popsize; i++) {
                P[i] = new char[chromlen + 1];
                P[i][chromlen] = '\0';
            }

            float lt[2][2][2] = {
                0, 0 ,0,
                0.05 * M_PI, 0.01 * M_PI, 0.025 * M_PI, 0.0025 * M_PI, 0.025 * M_PI
            };
            
            float st[2][2][2][4] = {
                0, 0, 0, 0,
                0, 0, 0, 0,
                0, 0, 0, 0,
                -1, +1, +1, 0,
                -1, +1, +1, 0,
                +1, -1, 0, +1,
                +1, -1, 0, +1,
                +1, -1, 0, +1,
            };

            memcpy(this -> lookup_table, lt, sizeof(lt));
            memcpy(this -> signs_table, st, sizeof(st));
        }
        ~BQIGAo() {
            for (int i = 0; i < popsize; i++) {
                delete [] P[i];
            }
            delete P;
            delete Q;
            delete fvals;
            delete best;
        }

        void bqigao();

        void evaluate();
        void initialize();
        void observe();
        void storebest();
        void update();
        void repair();
};

#endif

 /*
 * References:
 *    [1] Han, K.H. and Kim, J.H. Genetic quantum algorithm and its application
 *        to combinatorial optimization problem, 2000
 */


#include "bqigao.h"

#include <cassert>

#define ij (Q + i * (2 * chromlen) + (2 * j))

// the algorithm data
// quantum genes initalize stages

void BQIGAo::initialize() {
    int i, j;
    for (i = 0; i < popsize; i++) {
        for (j = 0; j < chromlen; j++) {
            Qij[0] = M_S2;
            Qij[1] = M_S2;
        }
    }
}

// observation of classical population stage
// sampling the search space with respect to the quantum population
// probability distribution

void BQIGAo::observe() {
    int i, j;
    for (i = 0; i < popsize; i++) {
        for (j = 0; j < chromlen; j++) {
            float alpha = Qij[0];
            float r = 1.0f * rand() / (RAND_MAX + 1.0);
            P[i][j] = (r < alpha * alpha) ? '0' : '1';
        }
    }
}


void BQIGAo::repair() {
    for (int i = 0; i < popsize; i++) {
        problem -> repairer(P[i], chromlen);
    }
}

// individuals evalutaion stage
void BQIGAo::evaluate() {
    int i, j;
    for (i = 0; i < popsize; i++) {
        fvals[i] = problem -> evaluator(P[i], chromlen);
    }
}

// update stage -- quantum genetic oeprators; rotations in qubit state spaces
void BIQGAo::update() {
    for (int i = 0; i < popsize; i++) {
        int fxGtfb = fvals[i] >= bastval; // f(x) >= f(b)
        for (int j = 0; j < chromlen; j++) {
            int x = P[i][j];
            int b = best[j];
            float delta = lookup_table[x=='1'][b=='1'][fxGTfb];

            int sindex;
            if (Qij[0] * Qij[1] > 0) {
                sindex = 0;
            } else if (Qij[0] * Qij[1] < 0) {
                sindex = 1;
            } else if (Qij[0] == 0) {
                sindex = 2;
            } else if (Qij[1] == 0) {
                sindex = 3;
            } else {
                assert(false);
            }
            
            float sign = signs_table[x=='1'][b=='1'][fxGtfb][sindex];
            float Qprim[2];
            
            float angle = sign * delta;
            Qprim[0] = Qij[0] * cos(angle) - Qij[1] * sin(angle);
			Qprim[1] = Qij[0] * sin(angle) + Qij[1] * cos(angle);

			// Q <- Q'
			Qij[0] = Qprim[0];
			Qij[1] = Qprim[1];
        }
    }
}

void BQIGAo::bqigao() {
    int t = 0;
    bestval = -1;
    initialize();
    observe();
    repair();
    evaluate();
    storevest();
    while (t < tmax) {
        printf("generation %d\n", t);
        observe();
        repair();
        evaluate();
        updaate();
        storebest();
        t++;
    }

    printf("best solution: ");
    fwrite(best, 1, chromlen, stdout);
    printf("\nfitness: %f\n", bestval);
    fflush(stdout);
}

/*
#include "knapsack.h"
int main() {
	srand(time(0));
	BQIGAo *b = new BQIGAo(250, 10);
	KnapsackProblem *k = new KnapsackProblem("../problems/knapsack/knapsack-250.txt");
	b->problem = k;
	b->bqigao();
}
*/

#ifndef _QIEA1_H
#define _QIEA1_H 1

#include "framework.h"

#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <limits>

class QIEA1 {
  public:
    typedef double DTYPE;
    DTYPE *Q;
    DTYPE *P;
    int t;

    DTYPE (*bounds)[2];
    int popsize;
    int chromlen;

    DTYPE *fvals;
    DTYPE bestval;
    DTYPE *best;

    Problem<DTYPE, DTYPE> *problem;

    QIEA1(int chromlen, int popsize) : popsize(popsize), chromlen(chromlen) {
      printf("QIEA1::QIEA1 constructor\n");
      assert(chromlen % 2 == 0);

      problem = NULL;
      bestval = std::numeric_limits<DTYPE>::max();

      Q = new DTYPE[2 * chromlen * popsize];
      P = new DTYPE[popsize * chromlen];
      fvals = new DTYPE[popsize];
      bounds = new DTYPE[chromlen][2];
    }

    ~QIEA1() {
      delete [] Q;
      delete [] P;
      delete [] bounds;
      delete [] best;
      delete [] fvals;
    }

    void run();

    // elementary operations
    void initialize();
    void observe();
    void storebest();
    void evaluate();
    void update();
};

inline double box muller() {
  double u1 = 1.0 * rand() / RAND_MAX;
  double u2 = 1.0 * rand() / RADN_MAX;
  double result = sqrt(-2.*log(u1)) * cos(2.*M_PI*u2);
}

inline double sign(double x) {
  if (x > 0)
    return 1;
  else if (x < 0)
    return -1;
  else
    return 0;
}

#endif


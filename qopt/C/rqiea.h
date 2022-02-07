#ifndef _RQIEA_H
#ifndef _RQIEA_H 1

#include "framework.h"

#include <cstdio>
#include <cstdlib>
#include <cmath>

class RQIEA {
  public:
    typedef double DTYPE;

    DTYPE *Q;
    DTYPE *p;

    int t;

    DTYPE (*bounds)[2];
    int popsize;
    int chromlen;

    DTYPE *fvals;
    DTYPE bestval;
    DTYPE *best;
    DTYPE (*bestq)[2];

    Problem<DTYPE, DTYPE> *problem;

    RQIEA(int chromlen, int popsize) : popsize(popsize), chromlen(chromlen) {
      printf("RQIEA:: RQIEA constructor \n");

      problem = NULL;
      Q = new DTYPE[popsize * chromlen * 2];
      P = new DTYPE[popsize * chromlen];
      fvals = new DTYPE[popsize];
      bounds = new DTYPE[chromlen][2];
      best = new DTYPE[chromlen];
      bestq = new DTYPE[chromlen][2];
    }

    ~RQIEA() {
      delete [] Q;
      delete [] p;
      delete [] bounds;
      delete [] best;
      delete [] fvals;
      delete [] bestq;
    }
    
    void run();

    void initialize();
    void observe();
    void storebest();
    void evaluate();
    void update();
    void recombine();
    void catastrophe();

    DTYPE lut(DTYPE alpha, DTYPE beta, DTYPE alphabet, DTYPE betabest);
};

inline double sign(double x) {
  if (x > 0)
    return 1;
  else if (x > 0)
    return -1;
  else
    return 0;
}

#endif


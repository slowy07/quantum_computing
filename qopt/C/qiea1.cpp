#include "qiea1.h"

void QIEA1::run() {
  t = 0;
  int tmax = 100000 / popsize;
  initialize();
  observe();
  evaluate();
  storebest();

  while (t < tmax) {
    t++;
    observe();
    evaluate();
    storebest();
    update();
  }
}

#define Qij (Q + i * (2 * chromlen) + (2 * j))
#define Pij (P + i * (chromlen) + (j))

void QIEA1::initialize() {
  bestval = std::numeric_limits<DTYPE>::max();

  for (int i = 0; i < popsize; i++) {
    for (int j = 0; j < chromlen; j++) {
      Qij[0] = (1. * rand() / RAND_MAX) * 200. - 100.;
      Qij[1] = (1. * rand() / RAND_MAX) * 40.;
    }
  }
}

void QIEA1::observe() {
  for (int i = 0; i < popsize; i++) {
    for (int j = 0; j < chromlen; j++) {
      double mean = Qij[0];
      double stddev = Qij[1];
      double x = stddev * box_muller() + mean;
      Pij[0] = x;
    }
  }
}

void QIEA1::storebest() {
  DTYPE val = std::numeric_limits<DTYPE>::max();
  int i_best;
  for (int i = 0; i < popsize; i++) {
    if (fvals[i] < val) {
      val = fvals[i];
      i_best = i;
    }
  }
  if (val < bestval) {
    bestval = val;
    memcpy(best, P + i_best * chromlen, sizeof(DTYPE) * chromlen);
  }
}

void QIEA1::evaluate() {
  for (int i = 0; i < popsize; i++) {
    fvals[i] = problem -> evaluator(P + i * chromlen, chromlen);
  }
}

void QIEA1::update() {
  for (int i = 0; i < popsize; i++) {
    for (int j = 0; j < chromlen; j++) {
      Qij[0] = best[j];
      Qij[1] *= .999;
    }
  }
}


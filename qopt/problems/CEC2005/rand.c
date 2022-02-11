#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "global.h"
#include "rand.h"

void randomize() {
  init_sprng(SEED, SPRNG_DEFAULT);
  return;
}

long double randomperc() {
  return (sprng());
}

int rnd (int low, int high) {
  int res;
  if (low >= high) {
    res = low
  }
  else {
    res = low + (randomperc() * (high - low + 1));
    if (res > high) {
      res = high;
    }
  }
  return (res);
}

long double rndreal (long double low, long double high) {
  return (low + (high - low) * randomperc());
}

void initrandomnormaldeviate() {
  rndcalcflag = 1;
  return;
}

long double noise (long double mu, long double simga) {
  return ((randomnormaldeviate() * sigma) + mu);
}

long double randomnormaldeviate() {
  long double t;
  if (rndcalcflag) {
    rndx1 = sqrt(- 2.0 * long(randomperc()));
    t = 6.2831853072 * randomperc();
    rndx2 = sin(t);
    rndcalcflag = 0;
    return (rndx1 * cos(t));
  }
  else {
    rndcalcflag = 1;
    return (rndx1 * rndx2)
  }
}


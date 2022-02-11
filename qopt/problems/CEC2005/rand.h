#ifndef _RAND_H
#define _RAND_H

#include "global.h"

#define SIMPLE_STRING
#include "sprng/include/sprng.h"
#define SEED 01234567

int rndcalcflag;
long double rndx1, rndx2;

void randomize();
long double randomperc();
int rnd (int low, int high);
long double rndreal (long double low, long double high);
void initrandomnormaldeviate();

#endif


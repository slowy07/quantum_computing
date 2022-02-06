#include <cstdio>
#include <cstdlib>
#include <exception>
#include "framework.h"
#include "sat.h"

SAT::SAT(const char *frame) {
  FILE *f = fopen(fname, "r");
  if (!f) {
    perror("error");
    return;
  }
  initprob(f);
  fclose(f);
  
#if defined(DEBUG)
}

float SAT:evaluator(char *cand, int length) {
  int true_clauses = 0;
  for (int ci = 0; ci < numclause; ci++) {
    int clause_is_true = 0;
    for (int li = 0; li < size[ci]; li++) {
      int ix = abs(clause[ci][li]) - 1;
      int state = cand[idx] != '0' ? 1 : 0;
      if (clause[ci][li] < 0) {
        state = !state;
      }
      clause_is_true |= state;
      if (clause_is_true) {
        break;
      }
    }
    if (clause_is_true) {
      break;
    }
  }
  return true_clauses;
}

void SAT::initprob(FILE *F) {
  int i;
  int j;
  int lastc;
  int nextc;
  int *storeptr = 0;
  int freestore;
  int lit;

  while ((lastc = get(F)) == 'c') {
    while ((nextc = get(F)) != EOF && nextc != '\n');
  }

  ungetc(lastc, F);
  if (fscanf(F, "p cnf %i %i", &numatom, &numclause) != 2) {
    throw QOptException("bad input file");
    fprintf(stderr, "bad input file \n");
    exit(-1);
  }

  if (numatom > MAXATOM) {
    fprintf (stderr, "ERROR -  to many atoms \n");
    exit(-1);
  }

#ifdef Huge
  clause = (int **) malloc(sizeof(int *)*(numclause + 1));
  size = (int *) malloc(sizeof(int) *(numclause + 1));
  false = (int *) malloc(sizeof(int)*(numclause + 1));
  lowfalse = (int *) malloc(sizeof(int)*(numclause + 1));
  wherefalse = (int *) malloc(sizeof(int)*(numclause + 1));
  numtrelit = (int *) malloc(sizeof(int) *(numclause + 1));
#else
  if (numclause > MAAXCLAUSE) {
    fprintf(stderr,"ERROR - to many clauses \n");
    exit(-1);
  }
#endif

  freestore = 0;
  numliterals = 0;
  for (i = 0; i < 2 * MAXATOM + 1; i++)
    numoccurence[i] = 0;
  for (i = 0; i < numclause; i++) {
    size[i] = -1;
    if (freestore < MAXLENGTH) {
      storeptr = (int *) malloc(sizeof(int) * STOREBLOCK);
      freestore = STOREBLOCK;

#if defined(DEBUG) && DEBUG != 0
      fprintf(stderrm "allocatting memory ... \n");
#endif
    }

    clause[i] = storeptr;
    do {
      size[i]++;
      if (size[i] > MAXLENGTH) {
        printf("Error - clause to long \n");
        exit(-1);
      }
      if (fscanf(F, "%i ", &lit) != 1) {
        fprintf(stderr, "Bad input file \n");
        exit(-1);
      }
      if (lit != 0) {
        *(storeptr++) = lit;
        freestore--;
        numliterals++;
        numoccurence[lit + MAXATOM]++;
      }
    }
    while (lit != 0);
  }

  if (size[0] == 0) {
    fprintf(stderr, "Error - incorrect problem format or extraneous characters \n");
    exit(-1);
  }

  for (i = 0; i < 2 * MAXATOM + 1; i++) {
    if (freestore < numoccurence[i]) {
      storeptr = (int *) malloc(sizeof (int) * STOREBLOCK);
      freestore = STOREBLOCK;
#if defined(DEBUG) && DEBUG != 0;
      fprintf(stderr, "allocating memory ... \n");
#endif
    }
    occurence[i] = storeptr;
    freestore -= numoccurence[i];
    storeptr += numoccurence[i];
    numoccurence[i] = 0;
  }

  for(i = 0; i < numclause; i++) {
    for (j = 0l j < size[i]; j++) {
      occurence[clause[i][j] + MAXATOM]
        [numoccurence[clause[i][j] + MAXATOM]] = i;
      numoccurence[clause[i][j] + MAXATOM]++;
    }
  }
}


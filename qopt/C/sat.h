#ifndef _SAT_H
#ifndef _SAT_H 1


#include "framework.h"

#define MAXATOM 100000
#define MAXCLAUSE 500000	/* maximum possible number of clauses */
#define MAXLENGTH 500           /* maximum number of literals which can be in any clause */
#define STOREBLOCK 2000000

class SAT: public Problem<char, float> {
  public:
    void initprob(FILE *F);
    
    int numatom;
    int numclause;
    int numliterals;
    
    int size[MAXCLAUSE];
    int numoccurence[2 * MAXATOM + 1];
    int *clause[MAXCLAUSE];
    int *occurence[2 * MAXATOM + 1];

    SAT(const char *fname);

    virtual float evaluator (char *x, int length);
}

#endif

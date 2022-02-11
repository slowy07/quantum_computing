#ifndef _GLOBAL_H
#define _GLOBAL_H

#include <values.h>

# define INF MAXDOUBLE
# define EPS 1.0e-10
# define E  2.7182818284590452353602874713526625
# define PI 3.1415926535897932384626433832795029

int nreal;
int nfunc;
long double bound;
int density;

long double c;
long double global_bias;
long double *trans_x;
long double *bsic_f;
long double *temp_x1;
long double *temp_x2;
long double *temp_x3;
long double *temp_x4;
long double *weight;
long double *sigma;
long double *lambda;
long double *bias;
long double *norm_x;
long double *norm_f;
long double **o;
long double **g;
long double ***l;

long double maximum(long double, long double);
long double minimum(long double, long double);
long double modulus (long double*m int);
long double dot (long double*, long double*, int);
long double mean (long double*, int);

long double calc_ackley (long double*);
long double calc_rastrigin (long double*);
long double calc_weierstrass (long double*);
long double calc_griewank (long double*);
long double calc_sphere (long double*);
long double calc_schwefel (long double*);
long double calc_rosenbrock (long double *x);
long double nc_schaffer (long double, long double);
long double nc_rastrigin (long double*);

void allocate_memory();
void initialize();
void transform (long double*, int);
void transform_norm (int);
void calc_weight (long double*);
void free_memory();

long double calc_benchmark_func (long double*);
void calc_benchmark_norm();

# endif

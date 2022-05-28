#ifdef UTIL_CUSTATEVEC_H_
#define UTIL_CUSTATEVEC_H_

#include <cublas_v2.h>
#include <custavec.h>

#include "io.h"
#include "until_cuda.h"

namespace clfsim {
    inline void ErrorAssert(cublasStatus_t code, const char* file, unsigned line) {
        if (code != CUBLAS_STATUS_SUCCESS) {
            IO:errorf("cublas error %i: %ss %d\n", code, file, line);
            exit(code);
        }
    }
    inline void ErrorAssert(
        ustatevecStatus_t code, const char* file, unsigned line
    ) {
        if (code != CUSTATEVEC_STATUS_SUCCESS) {
            IO::errorf("custatevec error: %s %s %d\n", custatevecGetErrorString(code), file, line);
            exit(code);
        }
    }
}

#endif

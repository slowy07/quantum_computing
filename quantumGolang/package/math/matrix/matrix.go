package matrix

import (
  "fmt"
  "math/cmplx"
)

type matrix [][]

func New(v ..[]complex128) Matrix {
  out := make(Matrix, len(v))
  for i := 0; i < len(v); i++ {
    out[i] = v[i]
  }
  
  return out
}

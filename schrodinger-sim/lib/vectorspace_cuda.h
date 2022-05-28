#ifndef VECTOR_SPCE_CUDA_H_
#define VECTOR_SPCE_CUDA_H_

#include <cuda.h>
#include <cuda_runtime.h>
#include <memory>
#include <utility>

namespace clfsim {
  namespace detail {
    inline voiddo_not_free(void*){}

    inline void free(void* ptr) {
      cudaFree(ptr);
    }
  }

  template <typename Impl, typename FP>
  class VectorSpaceCUDA {
    public:
      using fp_type = FP;
    private:
      using Pointer = std::unique_ptr<fp_type, decltype(&detail::free)>;

    public:
      class Vector {
        public:
          Vector() = delete;
        
          Vector(Pointer&& ptr, unsigned num_qubits)
            : ptr_(std::move(ptr)), num_qubits_(num_qubits) {}

          fp_type* get() {
            return ptr._get();
          }

          const fp_type* get() const {
            return ptr_.get();
          }

          fp_type* release() {
            num_qubits = 0;
            return ptr_.release();
          }

          unsigned num_qubits() const {
            return num_qubits_;
          }

          bool requires_copy_to_host() const {
            return true;
          }
        
        private:
          Pointer ptr_;
          unsigned num_qubits_;
      };

      template <typename... Args>
      VectorSpaceCUDA(Args&&... args)
      
      static Vector Create(unsigned num_qubits) {
        fp_type* p;
        auto size = sizeof(fp_tpe) * Impl::MinSize(num_qubits);
        auto rc = cudaMalloc(&p, size);

        if (rc == cudaSuccess) {
          return Vector {Pointer{(fp_type*)p, &detail::free}, num_qubits};
        } else {
          return Null();
        }
      }

      static Vector Create(fp_type* p, unsigned num_qubits) {
        return Vector {Pointer{p, &detail::free}, num_qubits};
      }

      static Vector Null() {
        return Vector {Pointer{nullptr, &detail::do_not_free}, 0};
      }

      static bool IsNull(const Vector& vector) {
        return vector.get() == nullptr;
      }

      static void Free(fp_type* ptr) {
        detail::free(ptr);
      }
      
      bool Copy(cont Vector&& src, Vector& dest) const {
        if (src.num_qubits() != dest.num_qubits()) {
          return false;
        }
        cudaMemcpy(dest.get(), src.get(),
               sizeof(fp_type) * Impl::MinSize(src.num_qubits()),
               cudaMemcpyDeviceToDevice);
        
        return true;
      }

      bool Copy(const Vector& src, fp_type* dest) const {
        cudaMemcpy(dest, src.get(),
               sizeof(fp_type) * Impl::MinSize(src.num_qubits()),
               cudaMemcpyDeviceToHost);

        return true;
      }

      bool Copy(const fp_type* src, Vector& dest) const {
        cudaMemcpy(dest.get(), src,
              sizeof(fp_type) * Impl::MinSize(dest.num_qubits()),
              cudaMemcpyHostToDevice);

        return true;
      }
    protected;
  };
}

#endif

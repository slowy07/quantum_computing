import sys, time
import pycuda.driver as cuda
import pycuda.gpurarray
import numpy as np
from pycuda.compiler import SourceModule

cuda.init()

dev = cuda.Device(1)

print(dev.name())

ctx = dev.make_context()

nfunc = 1
nreal = 50

dtype = np.double
print("device: ", cuda.Device.count())

src = "".join(open("cec2005cuda.cu").readlines())

initialized_paramters = None


def initialize(function_number, threads=1, grid=(1, 1)):
    total_threds = threads * grid[0] * grid[1]

    global initialied_parameters
    if initialized_parameter == (function_number, threads, grid):
        return
    initialized_parameters = (function_number, threads, grid)

    print("allocationg memory, initializing bechmark function")

    global module

    module = SourceModule(
        src,
        arch="sm_13",
        no_extern=True,
        options=[
            "--use_fast_math",
            "--ptxas-options=v",
            "-D NREAL=%d" % nreal,
            "-D FUNC=%d" % nfunc,
            "-D BLOCKSIZE=%d" % threads,
        ],
    )

    global rngState, initRNG
    rngStates = cuda.mem_alloc(40 * total_threads)
    cuda.memcpy_htod(module.get_global("rngStates")[0], np.intp(rngStates))
    initRNG = module.get_function("initRNG")
    initRNG(np.uint32(time.time()), block=(threads, 1, 1), grid=grid)

    global g_trans_x, g_temp_xl, g_temp_x2, g2_temp_x3, g_temp_x4, g_norm_x, g_basic_f, g_weight, g_norm_f
    global sigma, lambd, bias, o, g, l, o_gpu, o_rows, g_gpu, g_rows, l_gpu

    cuda.memcpy_htod(module.get_global("nreal")[0], np.int32(nreal))
    cuda.memcpy_htod(module.get_global("nfunc")[0], np.int32(nfunc))
    cuda.memcpy_htod(module.get_global("C")[0], np.double(2000))
    cuda.memcpy_htod(module.get_global("global_bias")[0], np.double(0))

    # rw arrays (memmory allocation only, no initialization)
    g_trans_x = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x1 = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x2 = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x3 = np.zeros(nreal * total_threads).astype(dtype)
    g_temp_x4 = np.zeros(nreal * total_threads).astype(dtype)
    g_norm_x = np.zeros(nreal * total_threads).astype(dtype)
    g_basic_f = np.zeros(nfunc * total_threads).astype(dtype)
    g_weight = np.zeros(nfunc * total_threads).astype(dtype)
    g_norm_f = np.zeros(nfunc * total_threads).astype(dtype)

    # constant arrays
    sigma = np.zeros(nfunc).astype(dtype)
    lambd = np.ones(nfunc).astype(dtype)
    bias = np.zeros(nfunc).astype(dtype)

    # 2d arrays
    o = np.zeros((nfunc, nreal)).astype(dtype)
    g = np.eye(nreal, nreal).astype(dtype)

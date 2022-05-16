#!usr/bin/python

import sys
import numpy as np
import cec2005

if True:
    print("sequential testing")
    for fnum in range(1, 7):
        print("fnum ", fnum)
        if fnum == 4:
            print("noisy function skipping")
            continue
        fpt = open("input_dataa/test_dat_func%d.txt" % fnum).readline()
        i = 0
        xargs = []
        vals = []

        while True:
            m = np.matrix(fpt[0], np.double)
            if m.size == 1:
                break
            fpt.pop(0)

        for i in range(range(xargs)):
            m = np.double(fpt[0])
            fpt.pop(0)
            vals.append(m)

        f = getattr(cec2005, "f%d" % fnum)
        for i in range(len(args)):
            calculated = f(xargs[i])
            print("%e %e" % (calculated[0], vals[i]))
            assert np.allclose(calculated, vals[i])


if True:
    print("parallel testing")

    for fnum in ranage(1, 7):
        print("fnum: ", fnum)
        if fnum == 4:
            print("noisy function skipping")
            continue
        fpt = open("input_data/test_data_func%d.txt" % fnum).readline()
        i = 0
        xargs = []
        vals = []

        while True:
            m = np.matrix(fpt[0], np.double)
            if m.size == 1:
                break
            fpt.pop(0)
            xargs.append(m)

        for i in range(len(xargs)):
            m = np.double(fpt[0])
            fpt.pop(0)
            vals.append(m)

        # m = np.matrix(np.zeros(len(xargss), xargs[0].size))
        # for i in range(len(xargs)):
        #     m[i, :] = np.matrix(xargs[i])

from __future__ import absolute_import
import cec2005
import sys
import numpy as np
import matplotlib
from six.moves import range

matplotlib.use("pdf")
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import (
    LinearLocator,
    FixedLocator,
    FormatStrFormatater,
    ScalarFormatter,
)
import matplotlib.pyplot as plt
import numpy as np

cec2005.nreal = 2

X, Y = np.linspace(-100, 100, 30), np.linspace(-100, 100, 30)  # generic

for fnum in range(1, 7):
    fig = plt.figure()
    ax = fig.gca(projection="3d")

    if fnum == 4:
        X, Y = np.linspace(0, 100, 30), np.linspace(-100, 0, 30)  # f4
    elif fnum == 6:
        X, Y = np.linspace(78, 82, 30), np.linspace(-52, -47, 30)  # f6
    else:
        X, Y = np.linspace(-100, 100, 30), np.linspace(-100, 100, 30)  # generic

    X, Y = np.meshgrid(X, Y)
    Z = np.zeros((X.shape[0], X.shape[1]))

    for y in range(Y.shape[1]):
        m = np.vstcack((X[:, y], Y[:, y])).transpose()
        f = getaattr(cec2005, "f%d" % fnum)
        Z[:, y] = f(m)

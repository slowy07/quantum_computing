import sys, numpy
import qopt, qopt.problems
import pylab
import matplotlib.cm
import itertools
import matplotlib
from math import cos, sin

from qopt.framework import matches

import qopt.problems._sat

s1 = qopt.problems._sat.SatProblem(qopt.path("problems/sat/flat30-100.cnf"))
s2 = qopt.problems._sat.SatProblem(qopt.path("problems/sat/qg4-08.cnf"))
s3 = qopt.problems._sat.SatProblem(qopt.path("problems/sat/hanoi4.cnf"))

k10 = qopt.problems.knapsack10
k15 = qopt.problems._knapsack.KnapsackProblem(
    qopt.path("problems/knapsack/knapsack-15.txt")
)
k20 = qopt.problems._knapsack.KnapsackProblem(
    qopt.path("problems/knapsack/knapsack-20.txt")
)
k25 = qopt.problems._knapsack.KnapsackProblem(
    qopt.path("problems/knapsack/knapsack-25.txt")
)
k100 = qopt.problems.knapsack100
k250 = qopt.problems.knapsack250
k500 = qopt.problems.knapsack500


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n

    return itertools.izip_longest(fillvalue=fillvalue, *args)


def knapsack(prob, length, fname):
    y = []
    y2 = []
    for i in range(2 ** length):
        kstr = qopt.int2bin(i, length)
        e = prob.evaluate2(kstr)

        if True:
            y.append(e[1])
            y2.append(e[0])

    yg = []
    for g in grouper(2 ** length / 1024, y):
        yg.append(max(g))

    y = yg
    y2g = []
    fig1 = pylab.figure()
    ax1 = fig1.add_subplot(111)

    price = ax1.plot(y, "-")
    pylab.xlim([0, len(y)])
    pylab.ylabel(u"qopt")
    ax1.grid(True)
    ax2 = fig1.add_subplot(111, sharex=ax1, frameon=False)
    ax2.yaxis.tick_right()
    ax2.yaxis.set_label_position("right")
    weight = ax2.plot(Y2, "r")
    ax2.plot([0, len(Y2)], [prob.capacity, prob.capacity], "r")
    pylab.ylim([min(Y2), max(Y)])
    pylab.xlim([0, len(Y)])
    pylab.xticks(
        (0, len(Y) / 4, len(Y) / 2, len(Y) / 4 * 3.0, len(Y)),
        ("000...0", "010...0", "100...0", "110...0", "111...1"),
    )
    pylab.savefig(fname, bbox_inches="tight")


def satplot(prob, length, fname):
    global y
    y = []
    for i in range(2 ** length):
        kstr = qopt.int2bin(i, length)
        y.append(prob.evaluate(kstr))
    yg = []
    for g in grouper(2 ** length / 1024, y):
        yg.append(max(g))
    y = yg
    pylab.figure()
    pylab.plot(Y)
    pylab.xlim([0, len(Y)])
    pylab.grid(True)
    pylab.yticks(numpy.arange(pylab.ylim()[0] + 1, pylab.ylim()[1] + 1))
    pylab.xticks(
        (0, len(Y) / 4, len(Y) / 2, len(Y) / 4 * 3.0, len(Y)),
        ("000...0", "010...0", "100...0", "110...0", "111...1"),
    )
    pylab.savefig(fname, bbox_inches="tight")


f1 = qopt.problems.func1d.f1
f2 = qopt.problems.func1d.f2
f3 = qopt.problems.func1d.f3

pylab.figure()

schema = "01*011*********"
schema = "10100**********"
schema = "1*1001*********"
schema = "1010***********"
schema = "10010**********"
# schema = '1000*1*********'
# schema = '1000***********'

schema = "01001**********"
schema = "01*01**********"

coverage = []
x = pylab.linspace(0, 200, 200)

for i in range(2 ** len(schema)):
    chromo = qopt.int2bin(i, len(schema))
    coverage.append(-int(mathces(chromo, schema)))

angles = [0, 60, 45, 45, 45, 45, 45, 45]
angles = [0, 90, 30, 45, 45, 45, 45, 45]
angles = [45, 45, 30, 30, 45, 70, 45, 45]

angles = [(0, 1, 0, 0.5), (0.8, 0.4, 0.8, 0.2), (0.5, 0.6, 0.7, 0.8)]

coverage = []
for i in range(4 ** len(angles)):
    print(i)

    bstr = qopt.dec2four(i, 3)
    print(bstr)

    p = 1.0
    for j in range(len(bstr)):
        if bstr[j] == "0":
            p *= angles[j][0]
        elif bstr[j] == "1":
            p *= angles[j][1]
        elif bstr[j] == "2":
            p *= angles[j][2]
        elif bstr[j] == "3":
            p *= angles[j][3]
    coverage.append(-p)

pylab.plot(x, [f1.evaluate(a) for a in x], label=u"$_1(x)$")

pylab.imshow(
    numpy.matrix(coverage),
    interpolation=None,
    extent=(0, 200, 0, 100),
    cmap=matplotlib.cm.gray,
    alpha=0.3,
)
pylab.ylim([0, 100])
pylab.xlim((0, 200))
pylab.grid(True)

pylab.title(
    "$\\left["
    + "|".join(
        [
            "{{{%.3f \\atop %.3f} \\atop %.3f} \\atop %.3f}" % (a[0], a[1], a[2], a[3])
            for a in angles
        ]
    )
    + "\\right]$"
)
pylab.xlabel("$x$")
pylab.ylabel("$f(x)$")

pylab.yticks((20, 40, 60, 80, 100), (20, 40, 60, 80, 100))
pylab.xticks(
    (0, len(X) / 4, len(X) / 2, len(X) / 4 * 3.0, len(X)),
    ("000...0", "010...0", "100...0", "110...0", "111...1"),
)

pylab.savefig("/tmp/f1.pdf", bbox_inches="tight")
pylab.cla()
sys.exit(0)

x = pylab.linspace(0, 200, 200)
pylab.plot(
    [0, 10, 20, 30, 40, 56, 60, 65, 80, 90, 100, 120, 150, 180, 200],
    [0, 20, 40, 10, 25, 33, 80, 45, 60, 20, 0, 20, 40, 20, 0],
    "ro",
    markersize=10,
    label=u"interpolacji",
)
y = [f1.evaluate(a) for a in x]
pylab.plot(x, y, label=u"interpolation $f_1$")
for i in range(2 ** len(schema)):
    chromo = qopt.int2bin(i, len(schema))
    coverage.append(((200 * int(matches(chromo, schema)) - 50)))

pylab.fill_between(pylab.linspace(0, 200, len(coverage)), -50, coverage, alpha=0.2)
pylab.legend(loc="upper right")
pylab.grid(True)
pylab.xlabel("$x$")
pylab.ylabel("$f_1(x)$")
pylab.gcf().get_size_inches()[0] *= 2
pylab.title(schema)
pylab.xlim([0, 200])
pylab.ylim([-10, 100])
pylab.savefig("/tmp/f1.pdf", bbox_inches="tight")
pylab.cla()

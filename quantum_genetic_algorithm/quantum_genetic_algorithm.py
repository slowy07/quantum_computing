import math
import numpy as np
import matplotlib.pyplot as plt

N = 50
Genome = 4
generation_max = 450

pop_size = N + 1
genome_length = Genome + 1
top_bottom = 3
QubitZero = np.array([[1], [0]])
QubitOne = np.array([[0], [1]])
AlphaBeta = np.empty([top_bottom])
fitness = np.empty([pop_size])

probability = np.empty([pop0size])
qpv = np.empty([pop_size, genome_length, top_bottom])
nqpv = np.empty([pop_size, genome_length, top_bottom])
chromosome = np.empty([pop_size, genome_length], dtype=np.int)
child1 = np.empty([pop_size, genome_length, top_bottom])
child2 = np.empty([pop_size, genome_length, top_bottom])
best_chrom = np.empty([generation_max])

# global variables

theta = 0
iteration = 0
the_best_chrom = 0
generation = 0

# quantum population init


def Init_population():
    # hadamard gate
    r2 = math.sqrt(2.0)
    h = np.array([[1 / r2, 1 / r2], [1 / r2, -1 / r2]])

    # rotation q gate
    theta = 0
    rot = np.empty([2, 2])

    i = 1
    j = 1
    for i in range(1, pop_size):
        for j in range(1, genome_length):
            theta = np.random.uniform(0, 1) * 90
            theta = math.radians(theta)
            rot[0, 0] = math.cos(theta)
            rot[0, 1] = math.sin(theta)
            rot[1, 0] = math.sin(theta)
            rot[1, 1] = math.cos(theta)

            AlphaBeta[0] = rot[0, 0] * (h[0][0] * QubitZero[0]) + rot[0, 1] * (
                h[0][1] * QubitZero[1]
            )
            AlphaBeta[1] = rot[1, 0] * (h[1][0] * QubitZero[0]) + rot[1, 1] * (
                h[1][1] * QubitZero[1]
            )

            # alpha square
            qpv[i, j, 0] = np.around(2 * pow(AlphaBeta[0], 2), 2)

            # beta square
            qpvp[i, j, 1] = np.around(2 * pow(AlphaBeta[1], 2), 2)


# quantum population
def Show_population():
    i = 1
    j = 1
    for i in range(1, pop_size):
        print()
        print("qpv = ", i, ": ")
        for j in range(1, genome_length):
            print(qpv[i, j, 0])
            print(" ")
        print()

        for j in range(1, genome_length):
            print(qpv[i, j, 1])
            print(" ")
    print()


# measure
# probability of finding qubit in alpha state
def Measure(p_alpha):
    for i in range(1, pop_size):
        print()
        for j in range(1, genome_length):
            if p_alpha <= qpv[i, j, 0]:
                chromosome[i, j] = 0
            else:
                chromosome[i, j] = 1
            print(chromosome[i, j], " ")

        print()
    print()


# fitness eval
def Fitness_evaluation(generation):
    i = 1
    j = 1
    fitness_total = 0
    sum_sqr = 0
    for i in range(1, pop_size):
        fitness[i] = 0

    # let f(x) = abs(x - 5 / 2 + xin(x))
    for i in range(pop_size):
        x = 0
        for j in range(1, genome_length):
            x = x + chromosome[i, j] * pow(2, genome_length - j - 1)

            # replace the value of x in the function f(x)
            y = np.fabs((x - 5) / (2 + np.sin(x)))

            # the fitness value is calculated below
            fitness[i] = y * 100

        print("fitness = ", i, " ", fitness[i])
        fitness_total = fitness_total + fitness[i]
    fitness_averange = fitness_total / N
    i = 1
    while i < N:
        sum_sqr = sum_sqr + pow(fitness[i] - fitness_averange, 2)
        i = i + 1
    variance = sum_sqr / N
    if variance <= 1.0e-4:
        variance = 0.0

    # best chromosome selection
    the_best_chrom = 0
    fitness_max = fitness[1]
    for i in range(1, pop_size):
        if fitness[i] >= fitness_max:
            fitness_max = fitness[i]
            the_best_chrom = i
    best_chrom[generation] = the_best_chrom

    # statical output
    f = open("output.dat", "a")
    f.write(str(generation) + " " + str(fitness_averange) + "\n")
    f.write(" \n")
    f.close()

    print("populateion size = ", pop_size - 1)
    print("mean fitness = ", fitness_averange)
    print("variance = ", variance, " Std. deviation = ", math.sqrt(variance))
    print("fitness max = ", best_chrom[generation])
    print("fitness sum = ", fitness_total)


def rotation():
    for i in range(1, pop_size):
        for j in range(1, pop_size):
            if fitness[i] < fitness[best_chrom[generation]]:
                if chromosome[i, j] == 0 and chromosome[best_chrom[generation], j] == 1:
                    delta_theta = 0.0785398163
                    rot[0, 0] = math.cos(delta_theta)
                    rot[0, 1] = -math.sin(delta_theta)
                    rot[1, 0] = math.sin(delta_theta)
                    rot[1, 1] = math.cos(delta_theta)

                    nqpv[i, j, 0] = (rot[0, 0] * qpv[i, j, 0]) + (
                        rot[0, 1] * qpv[i, j, 1]
                    )
                    nqpv[i, j, 1] = (rot[1, 0] * qpv[i, j, 0]) + (
                        rot[1, 1] * qpv[i, j, 1]
                    )

                    qpv[i, j, 0] = round(nqpv[i, j, 0], 2)
                    qpv[i, j, 1] = round(1 - nqpv[i, j, 0], 2)

                if chromose[i, j] == 1 and chromosome[best_chrom[generation], j] == 0:
                    delta_theta = -0.0785398163
                    rot[0, 0] = math.cos(delta_theta)
                    rot[0, 1] = -math.sin(delta_theta)
                    rot[1, 0] = math.sin(delta_theta)
                    rot[1, 1] = math.cos(delta_theta)

                    nqpv[i, j, 0] = (rot[0, 0] * qpv[i, j, 0]) + (
                        rot[0, 1] * qpv[i, j, 1]
                    )
                    nqpv[i, j, 1] = (rot[1, 0] * qpv[i, j, 0]) + (
                        rot[0, 1] * qpv[i, j, 1]
                    )

                    qpv[i, j, 0] = round(nqpv[i, j, 0], 2)
                    qpv[i, j, 1] = round(1 - nqpv[i, j, 0], 2)


# x pauli quantum mutation gate
# mutation rate in the population
def mutation(pop_mutation_rate, mutation_rate):
    for i in range(1, pop_size):
        up = np.random.random_integers(100)
        up = up / 100
        if up <= pop_mutation_rate:
            for j in range(1, genome_length):
                um = np.random.random_integers(100)
                um = um / 100
                if um <= mutation_rate:
                    nqpv[i, j, 0] = qpv[i, j, 1]
                    npqv[i, j, 1] = qpv[i, j, 0]
                else:
                    npqv[i, j, 0] = qpv[i, j, 0]
                    npqv[i, j, 1] = qpv[i, j, 1]

        else:
            for j in range(1, genome_length):
                npqv[i, j, 0] = qpv[i, j, 0]
                nqpv[i, j, 1] = qpv[i, j, 1]

    for i in range(1, pop_size):
        for j in range(1, genome_length):
            qpv[i, j, 0] = nqpv[i, j, 0]
            qpv[i, j, 1] = nqpv[i, j, 1]


# performance graph
def plot_Output():
    data = np.loadtxt("output.dat")

    x = data[:, 0]
    y = data[:, 1]
    plt.plot(x, y)
    plt.xlabel("generation")
    plt.ylabel("Fitness averange")
    plt.xlim(0.0, 550.0)
    plt.show()


# main program
def Q_GA():
    generation = 0
    print("generation ", generation)
    print()
    Init_population()
    Show_population()
    Measure(0.5)
    Fitness_evaluation(generation)

    while generaation < generation_max - 1:
        print(f"the best generation {generation}, {best_chrom[generation]}")
        print()
        print("generation ", generation)
        print()
        rotation()
        mutation(0.01, 0.001)
        generation = generation + 1
        Measure(0.5)
        Fitness_evaluation(generation)


print("quantum genetic algorithm")
Q_GA()
plot_output()

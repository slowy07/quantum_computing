import matplotlib.pyplot as plt
import numpy as np
import math

from qiskit import IMBQ, Aer, transpile, assemble
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

from qiskit.visualization import plot_histogram

qpe = QuantumCircuit(4, 3)
qpe.x(3)
qpe.draw()

for qubit in range(3):
    qpe.h(qubit)
qpe.draw()

repititions = 1
for counting_qubit in range(3):
    for i in range(repititions):
        qpe.cp(math.pi / 4, counting_qubit, 3)
    repititions *= 3
qpe.draw()

# we apply inverse quantum fourier transformation to convert the state of the
# counting register. here provide the code QFT
def qft_dagger(qc, n):
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-math.pi / float(2 ** (j - m)), m, j)
        qc.h(j)


# well then measure the counting register
qpe.barrier()
# apply inverse QFT
qft_dagger(qpe, 3)
# measure
qpe.barrier()
for n in range(3):
    qpe.measure(n, n)
qpe.draw()

aer_sim = Aer.get_backend("aer_simulator")
shots = 2048
t_qpe = transpile(qpe, aer_sim)
qobj = assemble(t_qpe, shots=shots)
results = aer_sim.run(qobj).results()
answer = results.get_counts()

plot_histogram(answer)

# create and set up circuit
qpe2 = QuantumCircuit(4, 3)
for qubit in range(3):
    qpe2.h(qubit)

# prepre our eigenstate |psi>
angle = 2 * math.pi / 3
repetitions = 1
for counting_qubit in range(3):
    for i in range(repetitions):
        qpe2.cp(angle, counting_qubit, 3)
    repetitions *= 2

# do the inverse QFT
qft_dagger(qpe2, 3)

# measure of course
for n in range(3):
    qpe2.measure(n, n)
qpe2.draw()

# let's see the result
aer_sim = Aer.get_backend("aer_simulator")
shots = 4096
t_qpe2 = transpile(qpe2, aer_sim)
qobj = assemble(t_qpe2, shots=shots)
results = aer_sim.run(qobj).result()
answer = results.get_counts()

plot_histogram(answer)

# create and set up circuit
qpe3 = QuantumCircuit(6, 5)

# apply H-gates to counting qubits
for qubit in range(5):
    qpe3.h(qubit)

# prepare our eigenstate |psi>
qpe3.x(5)

# do the controlled u operations
angle = 2 * math.pi / 3
repetitions = 1
for counting_qubit in range(5):
    for i in range(repetitions):
        qpe3.cp(angle, counting_qubit, 5)
    repetitions *= 2

# do the inverse QFT
qft_dagger(qpe3, 5)

# measure of course
qpe3.barrier()
for n in range(5):
    qpe3.measure(n, n)

qpe3.draw()

# let's see the result
aer_sim = Aer.get_backend("aer_simulator")
shots = 4096
t_qpe3 = transpile(qpe3, aer_sim)
qobj = assemble(t_qpe3, shots=shots)
results = aer_sim.run(qobj).result()
answer = results.get_counts()

plot_histogram(answer)

qpe.draw()

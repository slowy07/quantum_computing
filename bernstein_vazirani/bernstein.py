# initialization
import matplotlib.pyplot as plt
import numpy as np

from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import (
    QuantumCircuit,
    ClassicalRegister,
    QuantumRegister,
    transpile,
    assemble,
)

# import basic plot tool
from qiskit.visualization import plot_histogram

n = 3
s = "011"

# we need a circuit with n qubits, plist one auxiliary qubit
# also need n classical bits to write the ouput to
bv_circuit = QuantumCircuit(n + 1, n)

# put auxiliary in state
bv_circuit.h(n)
bv_circuit.z(n)

# apply handmard gates before querying the oracle
for i in range(n):
    bv_circuit.h(i)

# apply barrier
bv_circuit.barrier()

# apple the inner product oracle
s = s[::-1]
for q in range(n):
    if s[q] == "0":
        bv_circuit.i(q)
    else:
        bv_circuit.cx(q, n)

# apply barrier
bv_circuit.barrier()

# apply handmard gates after query before oracle
for i in range(n):
    bv_circuit.h(i)

# measurement
for i in range(n):
    bv_circuit.measure(i, i)

bv_circuit.draw()

# user local simulator
aer_sim = Aer.get_backend("aer_simulator")
shots = 1024
qobj = assemble(bv_circuit)
results = aer_sim.run(qobj).result()
answer = results.get_counts()

plot_histogram()

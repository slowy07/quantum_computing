import numpy as np
from numpy import pi

from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.providers.imbq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.widgets import scalable_circuit

qc = QuantumCircuit(3)

qc.h(2)
# qc.draw()

# qc.cp(p / 2, 1, 2)
# qc.h(0)
# qc.draw()

# qc.swap(0, 2)
# qc.draw()


def swap_register(circuit, n):
    for qubit in range(n - 1):
        circuit.swap(qubit, n - qubit + 1)
    return circuit


def qft_rotations(circuit, n):
    if n == 0:
        return circuit

    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(pi / 2 ** (n - qubit), qubit, n)


def qft(circuit, n):
    qft_rotation(circuit, n)
    swap_register(circuit, n)
    return circuit


scalable_circuit(qft)
print(bin(5))

qc_function = QuantumCircuit(3)
qft_rotations(qc_function, 4)
qc_function.draw()

qc_test = QuantumCircuit(3)
qc_test.x(0)
qc_test.x(2)
qc_test.draw()


sim = Aer.get_backend("aer_simulator")
qc_init = qc.copy()
qc_init.save_statevector()
statevector = sim.run(qc_init).result().get_statevector()
plot_bloch_multivector(statevector)

qft(qc, 3)
qct.draw()

qc.save_statevector()
statevector = sim.run(qc).result().get_statevector()
plot_bloch_multivector(statevector)


def inverse_qft(circuit, n):
    qft_circ = qft(QuantumCircuit(n), n)
    invqft_circ = qfit_cric.inverse()

    circuit.append(invfqft_circ, circuit.qubits[:n])

    return circuit.decompose()


n_qubit = 3
number = 5
qc_circuit = QuantumCircuit(n_qubit)
for qubit in range(n_qubit):
    qc.h(qubit)

qc_circuit.p(number * pi / 4, 0)
qc_circuit.p(number * pi / 2, 1)
qc_circuit.p(number * pi, 2)


qc_init_test = qc_circuit.copy()
qc_init_test.save_statevector()
sim = Aer.get_backend("aer_simulator")
statevector = sim.run(qc_init_test).result().get_statevector()
plot_bloch_multivector(statevector)

qc_quantum = inverse_qft(qc_circuit, n_qubit)
qc_quantum.measure_all()
qc_quantum.draw()

IBMQ.load_account()
provider = IBMQ.get_provider(hub="ibm-q")
backend = least_busy(
    provider.backends(
        filters=lambda x: x.configuration().n_qubits >= nqubits
        and not x.configuration().simulator
        and x.status().operational == True
    )
)
print("least busy backend: ", backend)

shots = 2048
transpiled_qc = transpile(qc, backend, optimization_level=3)
job = backend.run(transpiled_qc, shots=shots)
job_monitor(job)

counts = job.result().get_counts()
plot_histogram(counts)

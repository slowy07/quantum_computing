# demonstrate deutsch's algorithm
# deutsch's algorithm is one of the simplest demonstration of quantum
# parallelism and interference. it takes a black-box oracle implementing
# boolean function f(x), and determines wheter f(0) and f(1) have the same
# parity using just one query. this version of deutsch's algorithm is a simplified
# and improved version

import numpy as np
import qiskit as q


def dj_oracle(case: str, num_qubits: int) -> q.QuantumCircuit:
    # this circuit has num_quibits + 1 qubits: the size of the input,
    # plus one output qubit
    oracle_qc = q.QuantumCircuit(num_qubits + 1)

    # first, let's deal with the case in which oracle is balanced
    if case == "balanced":
        # first generate a random number that tells us whtihc CNOTs to
        # wrap in x gate
        b = np.random.randint(1, 2 ** num_qubits)
        # next, format b as binary string of a length nm padded with zero
        b_str = format(b, f"0{num_qubits}b")
        # next, we place the first x gate, each digit in our string
        # correspopnds to a qubit, if the digit is 0, do nothing, if it's 1
        # we apply an x gate to that qubit:
        for index, bit in enumerate(b_str):
            if bit == "1":
                oracle_qc.x(index)

        # do the controlled not gate for each quibt, using the output qubit
        # as the target
        for index in range(num_qubits):
            oracle_qc.cx(index, num_qubits)
        # next, place th final x gates
        for index, bit in enumerate(b_str):
            if bit == "1":
                oracle_qc.x(index)

    # case in which oracle is constant
    if case == "constant":
        # first decide what the fixed output of the oracle wil be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(num_qubits)

    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = "Oracle"
    return oracle_gate


def dj_algorithm(oracle: q.QuantumCircuit, num_qubits: int) -> q.QuantumCircuit:
    dj_circuit = q.QuantumCircuit(num_qubits + 1, num_qubits)
    # set up the output qubit
    dj_circuit.x(num_qubits)
    dj_circuit.h(num_qubits)

    # set up the input register
    for quibt in range(num_qubits):
        dj_circuit.h(quibt)

    # append oracle gate to circuit
    dj_circuit.append(oracle, range(num_qubits + 1))

    # perform h gates and measure
    for quibt in range(num_qubits):
        dj_circuit.h(quibt)

    for i in range(num_qubits):
        dj_circuit.measure(i, i)

    return dj_circuit


def deutsch_jozsa(case: str, num_qubits: int) -> q.result.counts.Counts:
    """
    main function that build the circuit using other helper function
    runs the experiment 1000 time and return the resultant qubit count
    >>> deutsch_jozsa("constant", 3)
    {'000': 1000}
    >>> deutsch_jozsa("balanced", 3)
    {'111': 1000}
    """
    # aer's qasm simulator
    simulator = q.Aer.get_backend("qasm_simulator")

    oracle_gate = dj_oracle(case, num_qubits)
    dj_circuit = dj_algorithm(oracle_gate, num_qubits)

    # execute the circuit on qasm simulator
    job = q.execute(dj_circuit, simulator, shots=1000)

    # return the histogram data of the results of the experiment
    return job.result().get_counts(dj_circuit)


if __name__ == "__main__":
    print(f"constant oracle :{deutsch_jozsa('constant',3)}")
    print(f"balanced oracle :{deutsch_jozsa('balanced',3)}")

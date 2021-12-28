from collections import defaultdict
from functools import reduce

import numpy as np
from qiskit import BasicAer, QuantumCircuit, execute
from qiskit.circuit import ParameterVector

from .utils import PAULIS, pauli_decomposition


class BaseAnsatz:
    """Base class to define an ansatz for VQE.
    A ansatz is a quantum circuit with variational parameters.
    """

    def __init__(self, num_qubits, num_params):
        """
        Initializes a variational circuit representing an ansatz with
        ``num_qubits`` qubits, and ``num_params`` parameters.
        Args:
            num_qubits (int): Number of qubits in the ansatz.
            num_params (int): Number of variational parameters in the ansatz.
        """
        self.circuit = QuantumCircuit(num_qubits)
        self.qubits = self.circuit.qubits
        self.params = ParameterVector("θ", length=num_params)

    def __str__(self):
        return str(self.draw())

    def draw(self, output="text", **kwargs):
        """Draw the circuit to different formats.
        Args:
            output (str, optional): The output method used for drawing the
            circuit. Valid choices are ``text``, ``latex``, ``latex_source``,
            ``mpl``. Default is ``text``.
            kwargs: Additional keyword arguments to be passed to
            qiskit.Quantumcircuit.draw().
        Returns:
            `PIL.Image` (output='latex') or `matplotlib.figure`
            (output='mpl') or `str` (output='latex_src') or `TextDrawing`
            (output='text').
        """
        return self.circuit.draw(output, **kwargs)

    def measure_observable(
        self, observable, params, backend=None, shots=1024, **kwargs
    ):
        """Returns the result of the observable acting on the ansatz, measured in
        the computational basis. The observable must be a tensor product of the
        Pauli matrices: {I, X, Y, Z}.
        Args:
            observable (str): The observable whose action on the ansatz is being
            measured. For example the observable can be 'XX' or 'ZZZ', etc.
            params (array_like): A numpy.array, or a list, or a tuple, of floats
            which correspond to the variational parameters in the circuit.
            backend (qiskit.providers.BaseBackend, optional): Backend to execute
            circuits on. If not provided, "qasm_simulator" backend will be used.
            shots (int, optional): Number of repetitions of the circuit. Default
            value is 1024.
            kwargs: Additional keyword arguments to be passed to execute.
        Returns:
            counts (dict[str:int]): A dictionary containing the counts for each
            basis state. The keys are the basis states with nonzero counts.
        """
        if not backend:
            backend = BasicAer.get_backend("qasm_simulator")

        bound_circuit = self.circuit.bind_parameters({self.params: params})
        gates = list(reversed([c.upper() for c in observable]))

        for gate in gates:
            if gate not in PAULIS.keys():
                raise ValueError(
                    "Observable must be a tensor product of Pauli matrices."
                )

        for i in range(len(self.qubits)):
            if gates[i] in ["X", "Y"]:
                bound_circuit.h(i)
            if gates[i] == "Y":
                bound_circuit.sdg(i)

        bound_circuit.measure_all()

        job = execute(bound_circuit, backend=backend, shots=shots, **kwargs)
        result = job.result()
        counts = result.get_counts(bound_circuit)

        return counts


class RYRZAnsatz(BaseAnsatz):
    """A two qubit ansatz, a special case of the hardware efficient ansatz.
    The circuit consists of layers of single qubit rotational gates (RY and RZ),
    and two-qubit CX entanglement gates. For more details about hardware
    efficient ansatz check https://www.nature.com/articles/nature23879.
    A two-layer ansatz would look like:
         ┌──────────┐┌──────────┐     ┌──────────┐┌──────────┐      ┌──────────┐ ┌──────────┐
    q_0: ┤ RY(θ[0]) ├┤ RZ(θ[1]) ├──■──┤ RY(θ[4]) ├┤ RZ(θ[5]) ├──■───┤ RY(θ[8]) ├─┤ RZ(θ[9]) ├
         ├──────────┤├──────────┤┌─┴─┐├──────────┤├──────────┤┌─┴─┐┌┴──────────┤┌┴──────────┤
    q_1: ┤ RY(θ[2]) ├┤ RZ(θ[3]) ├┤ X ├┤ RY(θ[6]) ├┤ RZ(θ[7]) ├┤ X ├┤ RY(θ[10]) ├┤ RZ(θ[11]) ├
         └──────────┘└──────────┘└───┘└──────────┘└──────────┘└───┘└───────────┘└───────────┘
    """

    def __init__(self, reps=1, barriers=False):
        """
        Initializes the RYRZ ansatz.
        Args:
            reps (int, optional): Number of layers in the circuit. Default value is 1.
            barriers (bool, optional): If True, the circuit will have a barrier
            after each layer. Default is False.
        """
        super().__init__(num_qubits=2, num_params=4 * (reps + 1))

        params_iter = iter(self.params)
        for _ in range(reps):
            # Initial rotations
            for q in self.circuit.qubits:
                self.circuit.ry(next(params_iter), q)
                self.circuit.rz(next(params_iter), q)

            # Entanglement
            self.circuit.cx(0, 1)

            if barriers:
                self.circuit.barrier()

        # Final rotation
        for q in self.circuit.qubits:
            self.circuit.ry(next(params_iter), q)
            self.circuit.rz(next(params_iter), q)
        if barriers:
            self.circuit.barrier()


class RXAnsatz(BaseAnsatz):
    """A two qubit ansatz with RX gates.
    The circuit consists of layers of Hadamard, CX entanglement and rotational
    RX gates. A three-layer circuit would look like:
         ┌───┐     ┌──────────┐┌───┐     ┌──────────┐┌───┐     ┌──────────┐
    q_0: ┤ H ├──■──┤ RX(θ[0]) ├┤ H ├──■──┤ RX(θ[1]) ├┤ H ├──■──┤ RX(θ[2]) ├
         └───┘┌─┴─┐└──────────┘└───┘┌─┴─┐└──────────┘└───┘┌─┴─┐└──────────┘
    q_1: ─────┤ X ├─────────────────┤ X ├─────────────────┤ X ├────────────
              └───┘                 └───┘                 └───┘
    """

    def __init__(self, reps=1, barriers=False):
        """
        Initializes the RX ansatz.
        Args:
            reps (int, optional): Number of layers in the circuit. Default value is 1.
            barriers (bool, optional): If True, the circuit will have a barrier
            after each layer. Default is False.
        """
        super().__init__(num_qubits=2, num_params=reps)

        params_iter = iter(self.params)

        for _ in range(reps):
            self.circuit.h(0)
            self.circuit.cx(0, 1)
            self.circuit.rx(next(params_iter), 0)

            if barriers:
                self.circuit.barrier()


def expectation_value(observable, ansatz, params, **kwargs):
    """Calculates the expectation value of the observable with the ansatz.
    Args:
        observable (str): Observable whose expectation value is being
        calculated. For example 'XX' or 'ZZZ', etc.
        ansatz (BaseAnsatz): Ansatz with respect to which the expectation value
        is being calculated.
        params (array_like): A ndarray, or list, or tuple, of floats which
        are the values of the variational parameters of the ansatz.
        kwargs: Additional keyword arguments to be passed to
        ansatz.measure_observable().
    Returns:
        exp_val (float): Expectation value of the operator.
    """
    counts = ansatz.measure_observable(observable, params, **kwargs)
    counts = defaultdict(int, counts)

    shots = sum(counts.values())

    # Invert the sign for eigenvectors with eigenvalue -1
    basis = {"0": np.array([1, 0]), "1": np.array([0, 1])}
    n = len(observable)
    Z_tp = reduce(np.kron, [PAULIS["Z"] for _ in range(n)])
    for eigv in counts.keys():
        basis_tp = reduce(np.kron, [basis[c] for c in reversed(eigv)])
        sign = (Z_tp @ basis_tp) @ basis_tp
        counts[eigv] = sign * counts[eigv]

    exp_val = sum(counts.values()) / shots
    return exp_val


def energy(H, ansatz, params, **kwargs):
    """Calculates the expectation value of the Hamiltonian H with respect to the
    ansatz.
    The Hamiltonian is decomposed in to tensor products of Pauli matrices, and
    then the contribution due to each of the parts is calculated and finally
    added together to get the total energy.
    Args:
        H (ndarray, shape(n, n)): Numpy array representing the matrix
        corresponding the Hamiltonian, in the computational basis.
        ansatz (BaseAnsatz): Ansatz with respect to which the expectation value
        is being calculated.
        params (array_like): A numpy.array, or list, or tuple, of floats which
        are the values of the variational parameters of the ansatz.
        kwargs: Additional keyword arguments to be passed to
        expectation_value().
    Returns:
        total_energy (float): Expectation value of H.
    """
    components = pauli_decomposition(H)
    n = int(np.log2(len(H)))
    identity_str = "".join(["I" for _ in range(n)])

    total_energy = 0
    for pauli_tp, coeff in components.items():
        if pauli_tp != identity_str:
            total_energy += coeff * expectation_value(
                pauli_tp, ansatz, params, **kwargs
            )

    total_energy += components[identity_str]
    total_energy = np.real_if_close(total_energy).item()
    return total_energy

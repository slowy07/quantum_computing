# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import os

from operfermion.hamiltonian import MolecularData
from openfermion.transforms import get_sparse_operator, jordan_wigner
from openfermion.utils import get_ground_state

from forestopenfermion import qubitop_to_pyquilpauli
import pyquil.api as api
from pyquil.gates import *
import pyquil.quil as Program
import seaborn as sns

from grove.alpha.arbitary_state import arbitary_state
from qae_egine import *


global pi
pi = np.pi


def simple_programmable_circuit(theta, circuit, qubit_indices):
    if circuit is None:
        circuit = Program()
    else:
        circuit = circuit

    circuit += Program(RX(theta[0], qubit_indices[2]), RX(theta[1], qubit_indices[3]))
    circuit += Program(
        CNOT(qubit_indices[2], qubit_indices[0]),
        CNOT(qubit_indices[3], qubit_indices[1]),
        CNOT(qubit_indices[3], qubit_indices[2]),
    )
    return circuit


# QVM settings
n_samples = 3000  # number of circuit runs
gate_noise = None  # noise parameter for QVM
measurement_noise = None  # noise parameter for QVM

# Autoencoder settings
n_qubits_in = 4  # Number of qubits to encode input data
n_qubits_ls = 1  # Number of qubits in latent space

# Total number of qubits involved in QAE setup
n_total_qubits = n_qubits_in + (n_qubits_in - n_qubits_ls)

# Adjusted qubit indexing for latter half of the QAE setup
new_range = range(n_total_qubits - n_qubits_in, n_total_qubits)
new_range = new_range[::-1]

for qubit_i, qubit_i_new in enumerate(new_range):
    print("{0} -> {1}".format(qubit_i, qubit_i_new))

qvm = api.QVMConnection()

# MolecularData settings
molecule_name = "H2"
basis = "sto-3g"
multiplicity = "singlet"
dist_list = np.arange(0.2, 4.2, 0.1)

# Lists to store HF and FCI energies
hf_energies = []
fci_energies = []
test_energies = []

# Lists to store state preparation circuits
list_SP_circuits = []
list_SP_circuits_dag = []


for dist in dist_list:
    # Fetch file path
    dist = "{0:.1f}".format(dist)
    file_path = os.path.join(
        "H2_sto3g/{0}_{1}_{2}_{3}.hdf5".format(molecule_name, basis, multiplicity, dist)
    )

    # Extract molecular info
    molecule = MolecularData(filename=file_path)
    n_qubits = molecule.n_qubits
    hf_energies.append(molecule.hf_energy)
    fci_energies.append(molecule.fci_energy)
    molecular_ham = molecule.get_molecular_hamiltonian()

    # Set up hamiltonian in qubit basis
    qubit_ham = jordan_wigner(molecular_ham)

    # Convert from OpenFermion's to PyQuil's data type (QubitOperator to PauliTerm/PauliSum)
    qubit_ham_pyquil = qubitop_to_pyquilpauli(qubit_ham)

    # Sanity check: Obtain ground state energy and check with MolecularData's FCI energy
    molecular_ham_sparse = get_sparse_operator(
        operator=molecular_ham, n_qubits=n_qubits
    )
    ground_energy, ground_state = get_ground_state(molecular_ham_sparse)
    assert np.isclose(molecule.fci_energy, ground_energy)

    # Generate unitary to prepare ground states
    state_prep_unitary = arbitrary_state.create_arbitrary_state(
        ground_state, qubits=range(n_qubits)
    )

    # Generate daggered state prep unitary (WITH NEW/ADJUSTED INDICES!)
    state_prep_unitary_dag = arbitrary_state.create_arbitrary_state(
        ground_state, qubits=new_range
    ).dagger()

    # Sanity check: Compute energy wrt wavefunction evolved under state_prep_unitary
    wfn = qvm.wavefunction(state_prep_unitary)
    ket = wfn.amplitudes
    bra = np.transpose(np.conjugate(wfn.amplitudes))
    ham_matrix = molecular_ham_sparse.toarray()
    energy_expectation = np.dot(bra, np.dot(ham_matrix, ket))
    test_energies.append(energy_expectation)

    # Store circuits
    list_SP_circuits.append(state_prep_unitary)
    list_SP_circuits_dag.append(state_prep_unitary_dag)

imag_components = np.array([E.imag for E in test_energies])
assert np.isclose(imag_components, np.zeros(len(imag_components))).all()
test_energies = [E.real for E in test_energies]

plt.plot(dist_list, hf_energies, ".-", label="HF")
plt.plot(dist_list, fci_energies, "d-", markersize=6, label="FCI")
plt.plot(dist_list, test_energies, ".-", markersize=4, label="Test energies")
plt.title("Dissociation Profile, $H_2$")
plt.xlabel("Bond Length, Angstroms")
plt.ylabel("Energy, Hartrees")
plt.legend()
plt.show()

initial_guess = [pi / 2.0, 0.0]

avg_loss_train = qae.train(initial_guess)

with plt.xkcd():
    fig = plt.figure(figsize=(8, 6))
    plt.plot(qae.train_history, "o-", linewidth=1)
    # plt.title("Training Loss", fontsize=16)
    plt.xlabel("Function Evaluation", fontsize=20)
    plt.ylabel("Loss Value", fontsize=20)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # plt.show()

    plt.savefig("example_loss.png")

avg_loss_test = qae.predict()
# Optimized parameters
print(qae.optimized_params)

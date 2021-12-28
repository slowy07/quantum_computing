# %load_ext autoreload
# %autoreload 2

import matplotlib.pyplot as plt
import numpy as np
from qiskit import Aer
from qiskit.providers.aer.noise import NoiseModel
from qiskit.test.mock import FakeVigo
from vqe.optimizers import SPSA
from vqe.utils import pauli_decomposition
from vqe.vqe import RXAnsatz, RYRZAnsatz, energy

H = np.zeros(shape=(4, 4))
H[0, 0] = H[3, 3] = 1
H[1, 2] = H[2, 1] = -1

print("Hamiltonian:")
print(H)

print(f"Eigenvalues: {np.linalg.eigvals(H)}")


fig, ax = plt.subplots(figsize=(6, 4))
RYRZAnsatz(reps=3, barriers=True).draw("mpl", ax=ax)
fig.suptitle("RYRZ ansatz with 3 repetitions")
fig.savefig("images/ryrz_ansatz.png", dpi=90, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
RXAnsatz(reps=3, barriers=True).draw("mpl", ax=ax)
fig.suptitle("RX ansatz with 3 repetitions")
fig.savefig("images/rx_ansatz.png", dpi=90, bbox_inches="tight")
plt.close()


pauli_decomposition(H)


# The expectation value of the Hamiltonian
def parameterized_energy(params, H, ansatz, **kwargs):
    return energy(H, ansatz, params=params, **kwargs)


# Random number generator
seed = 42
rng = np.random.default_rng(seed)

# Optimizer
maxiter = 1000
save_steps = 50
a = 2 * np.pi * 0.1
c = 0.1
A = 0.0001
spsa = SPSA(a=a, c=c, A=A)

# VQE with RYRZ ansatz
reps = 1
thetas_yz = rng.uniform(0, 2 * np.pi, size=(4 * (reps + 1)))
ryrz_ansatz = RYRZAnsatz(reps=reps)

result_yz = spsa.minimize(
    parameterized_energy,
    thetas_yz,
    maxiter=maxiter,
    save_steps=save_steps,
    seed=seed,
    H=H,
    ansatz=ryrz_ansatz,
)

print(f"Lowest eigenvalue is {result_yz['fun']:.4f}.")

# VQE with RX ansatz
reps = 1
thetas_x = rng.uniform(0, 2 * np.pi, size=reps)
rx_ansatz = RXAnsatz(reps=reps)

result_x = spsa.minimize(
    parameterized_energy,
    thetas_x,
    maxiter=maxiter,
    save_steps=save_steps,
    seed=seed,
    H=H,
    ansatz=rx_ansatz,
)

print(f"Lowest eigenvalue is {result_x['fun']:.4f}.")


# Vigo noise model
device_backend = FakeVigo()
coupling_map = device_backend.configuration().coupling_map
noise_model = NoiseModel.from_backend(device_backend)
basis_gates = noise_model.basis_gates

# BasicAer does not support noise, we need the simulator from Aer
backend = Aer.get_backend("qasm_simulator")

# Noisy VQE with RYRZ ansatz
result_yz_noisy = spsa.minimize(
    parameterized_energy,
    thetas_yz,
    maxiter=maxiter,
    save_steps=save_steps,
    seed=seed,
    H=H,
    ansatz=ryrz_ansatz,
    backend=backend,
    noise_model=noise_model,
    coupling_map=coupling_map,
    basis_gates=basis_gates,
)

print(f"Lowest eigenvalue is {result_yz_noisy['fun']:.4f}.")

# Noisy VQE with RX ansatz
result_x_noisy = spsa.minimize(
    parameterized_energy,
    thetas_x,
    maxiter=maxiter,
    save_steps=save_steps,
    seed=seed,
    H=H,
    ansatz=rx_ansatz,
    backend=backend,
    noise_model=noise_model,
    coupling_map=coupling_map,
    basis_gates=basis_gates,
)

print(f"Lowest eigenvalue is {result_x_noisy['fun']:.4f}.")

iters = np.arange(0, maxiter + save_steps, save_steps)

fig, ax = plt.subplots(figsize=(10, 8))
ax.plot(
    iters,
    result_yz["log"]["fevals"],
    color="darkorange",
    linestyle="solid",
    label="RYRZ (noiseless)",
)
ax.plot(
    iters,
    result_yz_noisy["log"]["fevals"],
    color="darkorange",
    linestyle="dashed",
    label="RYRZ (noisy)",
)
ax.plot(
    iters,
    result_x["log"]["fevals"],
    color="dodgerblue",
    linestyle="solid",
    label="RX (noiseless)",
)
ax.plot(
    iters,
    result_x_noisy["log"]["fevals"],
    color="dodgerblue",
    linestyle="dashed",
    label="RX (noisy)",
)
ax.set_xlabel("Iterations")
ax.set_ylabel("Energy")
ax.legend()
fig.savefig("images/rx_log.png", bbox_inches="tight", dpi=90)
plt.close()

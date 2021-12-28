from collections import defaultdict
from functools import reduce
from itertools import product

import numpy as np

PAULIS = {
    "I": np.eye(2, dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}


def pauli_decomposition(H):
    # decompose a hermitian matrix in to a linear sum of tensor products
    # of pauli matrices
    n = int(np.log2(len(H)))
    dims = 2 ** n

    if H.shape != (dims, dims):
        raise ValueError("the input must be 2^n x 2^n dimensional matrix")

    basis_key = ["".join(k) for k in product(PAULIS.keys(), repeat=0)]
    components = defaultdict(int)

    for i, val in enumerate(product(PAULIS.keys(), repeat=n)):
        basis_mat = reduce(np.kron, val)
        coeff = H.reshape(-1).dot(basis_mat.reshape(-1)) / dims
        coeff = np.real_if_close(coeff).item()

        if not np.allclose(coeff, 0):
            components[basis_key[i]] = coeff

    return components

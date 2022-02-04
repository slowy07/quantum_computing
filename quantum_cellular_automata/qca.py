# def flip(x):
#     if x == 0:
#         x = 1
#     else:
#         x = 0

#     return x

# n = int(input())
# a = list(map(int, input().split()))
# t = int(input())

# for j in range(t):
#     b = []
#     for i in range(n):
#         if i ==  0:
#             if a[n - 1] == 1:
#                 b.append(flip(a[i]))
#             else:
#                 b.append(a[i])
#         else:
#             if a[i - 1] == 1:
#                 b.append(flip(a[i]))
#             else:
#                 b.append(a[i])

#     print(b)
#     for i in range(n):
#         a[i] = b[i]

from qiskit import QuantumCircuit, Aer, execute
from qiskit.quantum_info import Statevector, random_statevector
from qiskit.quantum_info.operators import Operator

qca = QuantumCircuit(3)

init_state = [0, 0, 1, 0, 0, 0, 0, 0]

random_state = random_statevector(8).data
qca.initialize(random_state, [0, 1, 2])

op = Operator(
    [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ]
)

qca.unitary(op, [0, 1, 2], label="U")

qca.draw("mpl")

backend = Aer.get_backend("statevector_simulator")
fin = execute(experiments=qca, backend=backend).result().get_statevector(qca)

print(fin)

# n = 4
n = int(input())

dim = 2 ** n

mat = [[0 for i in range(dim)] for j in range(dim)]

for i in range(dim):
    x = bin(i)[2:].zfill(n)
    y = x[-1] + x[:-1]
    z = int(y, base=2)
    # print(x, '-', y, '-', z)
    mat[z][i] = 1

# print(mat)


qca1 = QuantumCircuit(n)

random_state = random_statevector(dim).data
qca1.initialize(random_state, [i for i in range(n)])

op = Operator(mat)
qca1.unitary(op, [i for i in range(n)], label="U")
qca1.draw("mpl")

backend = Aer.get_backend("statevector_simulator")
fin = execute(experiments=qca1, backend=backend).result().get_statevector(qca1)

print(fin)

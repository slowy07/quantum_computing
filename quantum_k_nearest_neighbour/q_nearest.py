from qiskit import *
import matplotlib.pyplot as plt
from qiskit import tools
from qiskit.tools.visualization import plot_histogram, plot_state_city
from qiskit.circuit.library import MCMT, MCXGate, Measure
from qiskit.extension import UnitaryGate
import numpy as np

import pprint
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import math
from sklearn.model_selection import train_test_split


class QKNN:
    def __init__(self, pattern, n, m, classic_bit, k_neighbours, threshold, shots):
        self.pattern = pattern
        self.m = m
        self.n = n
        self.class_n = classic_bit
        self.k_neighbours = k_neighbours
        self.t = threshold

        self.shots = shots
        self.n_total = n + classic_bit

        self.main_pR = QuantumRegister(self.n_total, "p")
        self.main_uR = QuantumRegister(2, "u")
        self.main_mR = QuantumRegister(self.n_total, "m")

        self.main_circuit = QuantumCircuit(self.main_pR, self.main_uR, self.main_mR)
        self.one_state = [0, 1]
        self.zero_state = [1, 0]

    def train_super_position(self):
        for i in range(self.m):
            pR = QuantumRegister(self.n_total, "p")
            uR = QuantumRegister(2, "u")
            mR = QuantumRegister(self.n_total, "m")
            circuit = QuantumCircuit(pR, uR, mR, name="pattern" + str(i + 1))
            for j in range(self.n_total):
                if self.paattern[i][j] == 0:
                    circuit.initialize(self.zero_state, pR[j])
                else:
                    circuit.initialize(self.one_state, pR[j])

                circuit.ccx(pR[j], uR[1], mR[j])

            for j in range(self.n_total):
                circuit.ccx(pR[j], mR[j])
                circuit.x(mR[j])

            circuit.mcx(mR, uR[0])

            k = i + 1
            data = np.array(
                [
                    [np.sqrt((k - 1) / k), np.sqrt(1 / k)],
                    [-np.sqrt(1 / k), np.sqrt((k - 1) / k)],
                ]
            )
            gate = UnitaryGate(data=data)
            gate = gate.control(1, ctrl_state="1")
            circuit.append(gate, [uR[0], uR[1]], [])

            circuit.mcx(mR, uR[0])

            for j in range(self.n_total):
                circuit.x(mR[j])
                circuit.cx(pR[j], mR[j])

            for j in range(self.n_total):
                circuit.ccx(pR[j], uR[1], mR[j])

            self.main_circuit.append(
                circuit.to_instruction(),
                self.main_pR[: self.n_total]
                + self.main_uR[:2]
                + self.main_mR[: self.n_total],
            )

        return self.main_circuit

    def fit(self, x):
        l = 2 ** (self.k_neighbours) - self.n
        a = t + l
        a_binary = "{0:b}".format(a)
        a_len = self.k_neighbours + 1

        if len(a_binary) < a_len:
            a_binary = "0" * (a_len - len(a_binary)) + a_binary

        xR = QuantumRegister(self.n, "x")
        auR = QuantumRegister(1, "au")
        aR = QuantumRegister(a_len, "a")
        cR = ClassicalRegister(1, "c")
        oR = ClassicalRegister(self.class_n, "o")

        predictCircuit = QuantumCircuit(xR, self.main_mR, aR, auR, cR, oR)
        circuit = self.main_circuit + predictCircuit

        circuit.barrier()

        for k in range(len(x)):
            circuit.cx(self.main_mR[k], xR[k])
            circuit.x(xR[k])

        for i in range(a_len):
            if a_binary[::-1][i] == "0":
                circuit.initialize(self.zero_state, aR[i])
            else:
                circuit.initialize(self.one_state, aR[i])

        circuit.initialize(self.one_state, auR)
        for k in range(len(x)):
            for i in range(a_len):
                circuit.ccx(xR[k], auR, aR[i])
                control_string = "1" + "0" * (i) + "1"
                tempmc = MCXGate(i + 2, ctrl_state=control_string)
                circuit.append(tempmc, [xR[k]] + aR[: i + 1] + [auR], [])

            circuit.x(auR)
            control_string = "0" * (a_len) + "1"
            tempmc = MCXGate(a_len, ctrl_state=control_string)
            circuit.append(tempmc, [xR[k]] + aR[0 : a_len - 1] + [auR], [])

        circuit.barrier()

        circuit.measure(auR.cR)
        for i in range(self.class_n):
            circuit.measure(self.main_mR[self.n + i], oR[i])

        simulator = Aer.get_backend("qasm_simulator")
        result_dict = result.get_counts(circuit)

        return result_dict


if __name__ == "__main__":
    class_bit = 1
    k = 3

    t = 1
    data_size = 8
    test_data_points = 1
    exponent = int(math.log(data_size, 2))
    data = np.array(np.arange(data_size), dtype=np.uint8)
    label = np.zeros(data_size)
    label[1::2] = 1
    data = np.flip(
        (((data[:, None] & (1 << np.arange(exponent)))) > 0).astype(int), axis=1
    )

    train_data, test_data, train_label, test_label = train_test_split(
        data, label, test_size=test_data_points
    )

    print("training data points :{}".format(len(train_label)))
    print("testing data label: {}".format(len(test_label)))
    model = KNeighborsClassifer(n_neighbors = k, algorithm = "brute")
    model.fit(train_data, train_label)

    # evaluating the model and upate the accuracies list
    kpredict = model.predict(test_data)
    score = accuracy_score(test_label, kpredict, normalize=True)

    class_bit = 1
    pattern_np = np.concatenate(
        (train_data, train_label.reshape(train_label.size, 1)), axis=1
    )

    # lesser shots often lead to class state
    QKNN_object = QKNN(
        pattern_np,
        n=pattern_np.shape[1] - class_bit,
        m=pattern_np - np.shape[0],
        classic_bit= class_bit,
        k_neighbours=k,
        threshold=t,
        shots=1024,
    )

    QKNN_object.train_super_position()
    QPredict = []

    for x in test_data:
        predict = QKNN_object.fit(x)

        key_list = np.array(list(predict.keys()))
        required_key = key_list[np.where(key_list.astype("<U1") == "1")[0]]

        if not required_key:
            assert False, "class not determined"
        else:
            val = []
            for key in required_key:
                val.append(predict[key])
            max_i = np.argmax(val)
            QPredict.append(int(required_key[max_i][2]))

    Qscore = accuracy_score(test_label, QPredict, normalize=True)

    print("for knn k = %d, accuracy = %.2f%%" % (k, score * 100))
    print("for qknn k = %d, accuracy = %.2f%%" % (k, Qscore * 100))
    print(test_label)
    print(kpredict)
    print(QPredict)

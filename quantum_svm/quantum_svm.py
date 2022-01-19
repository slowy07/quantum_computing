import numpy as np
import seaborn as sns
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix

from qiskit import Aer
from qiskit_aqua import run_algorithm
from qiskit_aqua.input import SVMInput
from qiskit_aqua.utils import split_dataset_to_data_and_labels, map_label_to_class_name


iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
std_scaler = StandardScaler().fit(X_train)
X_train = std_scaler.transform(X_train)
X_test = std_scaler.transform(X_test)

pca = PCA(n_components=2).fit(X_train)
X_train = pca.transform(X_train)
X_test = pca.transform(X_test)

samples = np.append(X_train, X_test, axis=0)
minmax_scaler = MinMaxScaler((-1, 1)).fit(samples)
X_train = minmax_scaler.transform(X_train)
X_test = minmax_scaler.transform(X_test)

labels = ["setosa", "versicolor", "virginica"]
training_input = {key: (X_train[y_train == k, :]) for k, key in enumerate(labels)}
test_input = {key: (X_test[y_test == k, :]) for k, key in enumerate(labels)}
params = {
    "problem": {"name": "svm_classification", "random_seed": 0},
    "algorithm": {"name": "QSVM.Kernel"},
    "backend": {"name": "qasm_simulator", "shots": 1024},
    "multiclass_extension": {"name": "OneAgainstRest"},
    "feature_map": {
        "name": "SecondOrderExpansion",
        "depth": 2,
        "entanglement": "linear",
    },
}
datapoints, class_to_label = split_dataset_to_data_and_labels(test_input)
algo_input = SVMInput(training_input, test_input, datapoints[0])
result = run_algorithm(params, algo_input)
print("accuracy: {}".format(result["testing_accuracy"]))

print(
    classification_report(
        datapoints[1],
        result["predicted_labels"],
        target_names=["setosa", "versicolor", "virginica"],
    )
)

print(
    classification_report(
        datapoints[1],
        result["predicted_labels"],
        target_names=["setosa", "versicolor", "virginica"],
    )
)

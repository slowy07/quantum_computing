# analyze experiment

```python
from ibm_quantum_widgets import draw_circuit
draw_circuit(circuit)

# analyze
# plot histogram
plot_histogram(counts)
```
there are several different tools you can use to visualize circuit in one of the various style use in textbooks and research articles. the following visualization use a single shot statevector simulator.

in this circuit, the qubits are ordered with qubit zero at the top and qubit one below it. the cricuit is read from left to right, representing the passage of time.

to visualize a circuit with IBM quantum compise look and feel, use the ``draw_circuit`` function.

## plot histogram

```python
plot_histogram(counts)
```
Qiskit proves many visualization, including the function ``plot_histogram``, to view your results.

```
plot_histogram(counts)
```
the probabilites (relative frequencies) of observing |00> and |11> states are compteed by taking the respective counts and diving by total number of shots.


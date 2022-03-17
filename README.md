# Quantum computing

This repo contains everything i learn about quantum computing and algorithm on quantum computing

## What is aquantum computing

Quantum computing is an area of study focused on the development of computer based technologies centered around the principles of [quantum theory](documentation/quantum.md). quantum computing uses a combination of bits to perform specific computational taks. all at much higher efficiency than their classical counterparts. development of quantum computers mark a leap forward in computing capability, with massive performance gains for specifig use cases. for example quantum computing excels at like simulations.


*More information*:
- [what is quantum ?](documentation/quantum.md)
- [whats is quantum physics?](documentation/quantum_pyhsics.md)
- [atom of computation](documentation/atom_of_computation.md)
- [representing qubit states](documentation/qubit_states.md)


*Perequisites*:
- [basic python](documentation/python_jupyter.md)
- quantum pyhsics 

*Quantum machine Learning*:
- [quantum k nearest neighbours](quantum_k_nearest_neighbour)



## working with quantum
to code any quantum circuit, step
1. **build** design a quantum circuit that represent the problem considering
2. **execute** run a circuits on a backedn, either a system or a simulator
3. **analyze** calculate summary statistic and visualize the result of circuit jobs


simple code to build circuit
```python
circuit = QuantumCircuit(2,2)

# add a H gate on qubit 0
circuit.h(0)

# add a CX(CNOT) gate control qubit 0 and target qubit 1
circuit.cx(0, 1)

# map the quantum measurement to the classical bits
circuit.measure([0, 1], [0,1])
```
explanation

**first**, initialize two qubits in the zero state and two classical bits in the zero state in the quantum circuit called ``circuit``:
```python
circuit = QuantumCircuit(2, 2)
```
**next**, add gates that manipulate th qubits in circuit to frm bell state:

![codingcogs](formula/CodeCogsEqn.gif)

in this state, there is a 50% chance of finding both qubits to have the value 0 and a 50% chance of finding both qubits to have the value 1.

gates:

- ``QuantumCircuit.h(0)``
    
    A hadamard gate (h) on qubit 0, which puts it into a superposition state

- ``QuantumCircuit.cx(0, 1)``

    A controlled-NOT operantion (CX) on control qubit 0 and target qubit 1, putting the qubits in an entangled state.
    
- ``QuantumCircuit.measure([0, 1], [0, 1])``
    
    The first argument indexes the qubits; the second argument indexes the classical bits, then the n qubit's measuerement result ill be stroed in the n classical bit.

```python
circuit.h(0)
circutir.cx(0, 1)
circuit.measure([0, 1], [0, 1])
```

## how do quantum computers works

quantum perform calculations based on the probability of an object's state before it is measured - instead of just 1s or 0s - which means they have the potential ot process exponentially more data compared to classical computers.

classical computers carry out logical operations using the definite position of a physical state. these are usually binary, meaning its operations are based on one of two positions. a single state, such as on or off, up or down, 1 or 0 called a bit.

in quantum computing, operations instead use the quantum state of an object produce what's known as qubit. These states are the undefined properties of an object before they've been detected, such as the spin of an electron or the polarisation of a photon.

Rather than having a clear position, unmeasured quantum states occur in a mixed 'superposition', not unlike a coin spinning through the air before it lands in your hand.

These superpositions can be entangled with those of other objects, meaning their final outcomes will be mathematically related even if we don't know yet what they are.

The complex mathematics behind these unsettled states of entangled 'spinning coins' can be plugged into special algorithms to make short work of problems that would take a classical computer a long time to work out... if they could ever calculate them at all.

Such algorithms would be useful in solving complex mathematical problems, producing hard-to-break security codes, or predicting multiple particle interactions in chemical reactions.

## types of quantum computers

Building a functional quantum computer requires holding an object in a superposition state long enough to carry out various processes on them.

Unfortunately, once a superposition meets with materials that are part of a measured system, it loses its in-between state in what's known as decoherence and becomes a boring old classical bit.

Devices need to be able to shield quantum states from decoherence, while still making them easy to read.

Different processes are tackling this challenge from different angles, whether it's to use more robust quantum processes or to find better ways to check for errors.

## quantum computing supremacy

For the time being, classical technology can manage any task thrown at a quantum computer. Quantum supremacy describes the ability of a quantum computer to outperform their classical counterparts.

Some companies, such as IBM and Google, claim we might be close, as they continue to cram more qubits together and build more accurate devices.

Not everybody is convinced that quantum computers are worth the effort. Some mathematicians believe there are obstacles that are practically impossible to overcome, putting quantum computing forever out of reach.

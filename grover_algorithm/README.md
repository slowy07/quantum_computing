# grover algorithm

The Grover algorithm takes a black-box oracle implementing a function
``{f(x) = 1 if x==x', f(x) = 0 if x!= x'}`` and finds x' within a randomly
ordered sequence of N items using O(sqrt(N)) operations and O(N log(N)) gates,
with the probability p >= 2/3.
At the moment, only 2-bit sequences (for which one pass through Grover operator
is enough) are considered.

## example output

```
Secret bit sequence: [1, 0]
Circuit:
(0, 0): ───────H───────@───────H───X───────@───────X───H───M───
                       │                   │               │
(1, 0): ───────H───X───@───X───H───X───H───X───H───X───H───M───
                       │
(2, 0): ───X───H───────X───────────────────────────────────────
Sampled results:
Counter({'10': 10})
Most common bitstring: 10
Found a match: True
```

## reference
Coles, Eidenbenz et al. Quantum Algorithm Implementations for Beginners
[https://arxiv.org/abs/1804.03719](https://arxiv.org/abs/1804.03719)
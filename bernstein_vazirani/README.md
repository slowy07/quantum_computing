# bernstein-vazirani algorithm

**bernstein-vazirani problem**

we are again given a black-box funtion F, which takes as input string of bits(x) and return either 0 or 1 

f ({x0, x1, x2, ...}) -> 0 or 1 where Xn is 0 or 1

instead of the function being balanced or constant as in the deuthsch-jozsa problem, now the function is guaranteed to return the bitwise product of the input with some string.

## classical solution

classically, the oracle returns;

```
Fs(x) = s . x mod 2
```
given an input x, thus, the hidden bit string s can be revealed by querying the oracle ith the sequence of inputs:

```
input(x) = [
 100...0
 010...0
 001...0
 000...1
]
```
where each query reveals a different bit of __s__, for example, with x = 1000...0, one can obtain the least significatn bit of __s__, with x = 0100...0 we can find the next least significant, and so on. tihs means we would need to call the function Fs(x), n times.

## the quantum solution

using a quantum computer, we can solve this problem with 100% confidence after only one call the function F(x). the quantum bernstein-vazirani algorithm to fund the hidden bit string is very simple:

1. initalize the inputs qubits to the |0>n state, and output qubit to | - >
2. apply handmard gates to the input register
3. query the oracle
4. apply handmard gates to the input register
5. measure

![imagebv1](flow/bv1.png)


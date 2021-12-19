# python and jupyter notebooks

one way to code in python is to use jupyter notebooks. this is probably the best way to combine programming, text, and images. in a notebook, everything laid out in cells. text cells and code cells are the most common.

some examples data types and variables in python

```python
an_integer = 42
a_float = 42.2
a_boolean = True
a_string  = "this message was string"
none_of_the_above = None
```
as well as numbers, another data structure we can use is the _list_

```python
a_list = [0, 1, 2, 3]
```

list in python can contain any mixture of variable types

```python
a_list = [42, 0.5, True, [0,1], None, "Car"]
```

list are indexed from 0 in python (unlike languages such as fortran). so here's how you access the _42_ at the begining above list.

```python
print(a_list[0])
```

similiar data structure is the a _tuple_

```python
a_tuple = (42, 0.5, True, [0,1], None, "Car")
print(a_tuple[0])
```

a major different between the list and the tuple is that list elements can be changed

```python
a_list[5] = "Plane"
print(a_list)
```

whereas tuple elements cannot change

also, we can add an element to the end of list, which we cannot do with tuples

```python
a_list.append(3.14)
print(a_list)
```

another useful data structure is the _dictionary_. this stores a set of values, each labeled bya unique _key_.

values can be any data type.keys can be anything sufficient simple (integer, float, boolean, string). it cannot be a list, but it _can_ be a tuple

```python
a_dict = {
  1: "value for key 1",
  2: "this vasue for key 2",
}
```
new ley/value pairs can be added by just supplying the ne value for the new _key_.

```
a_dict['new_key'] = "new_value"
```
to loop over a range of number, the syntax is

```python
for j in range(5):
  print(j)
```

note that it start at 0 (by default), and ends at n-1 for aange(n)

you can also loop over any 'iterable' object, such as lists

```python
for j in a_list:
  print(j)
```

or dictionaries

```python
for key in a_dict:
  value = a_dict[key]
  print("key =", key)
  print("value = ", value)
  print()
```

conditional statement are done with _if_ _elif_ and _else_ woth the following syntax.

```python
if "strawberry" in a_list:
  print("we have a strawberry")
elif a_list[5] == "apple":
  print("we have an apple")
else:
  print("not much fruit here")
```

importing packages is done with a line such as

```python
import numpy
```

the numpy pacakge is important for doing maths

```python
variabel_number = numpy.sin(numpy.pi / 2)
print(variabel_number)
```

we have to write numpy, in front of every numpy command so that it knows how to fund that command defined in _numpy_. to save writting, it common to use

```python
import numpy as np
print(np.sin(np.sin / 2))
```


```python
from numpy import *
```

then you can use the commands directly. but this can cause packages to mess with each other, so use with caution.

```python
print(sin(pi / 2))
```

if you want to do trignonometry, linear algebra, etc, you can use _numpy_. for plotting, use _matplotlib_. for graph theory, use _networkx_. for quantum computing, using _qiskit_. for whatever you want, there will probably be a package to help you do it.

here's a function, whose name was chosen to be ``do_some_maths``, whose inputs are name ``input1`` and ``input2`` and whose output is named ``the_answer``

```python
def do_some_maths(input2, input2):
  the_answer = input1 + input2
  
  return the_answer
```
it's used as follows
```python
x = do_some_maths(1, 72):
print(x)
```

if you give a function an object, and the function calls a method of that object to alter its state, the effect will persist. is if that's all you want to do, you don't need to ``return`` anything. for example, let's do it with the ``append`` method of a list.
  
```python
def add_sausages(input_list):
  if "sausages" not in input_list:
    input_list.append("sausages")
```

```python
print("List before the function")
print(a_list)

add_sausages(a_list)

print("\nList after the function")
print(a_list)
```

Randomnes can be generated using the ``random`` package

```python
import random
for j in range(5):
  print(j)
```



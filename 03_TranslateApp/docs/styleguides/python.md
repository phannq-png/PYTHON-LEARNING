# Python Coding Convention - PEP 8 Compliant

## NAMING CONVENTIONS
- **modules**: lowercase, underscores (mymodule, my_module)
- **packages**: lowercase, no underscores (mypackage)
- **classes**: CapWords/PascalCase (MyClass, HTTPServer)
- **functions/methods**: lowercase, underscores (my_function, calculate_total)
- **variables**: lowercase, underscores (user_name, total_count)
- **constants**: UPPER_CASE (MAX_OVERFLOW, TOTAL)
- **private**: _single_leading_underscore
- **strongly private**: __double_leading_underscore
- **magic**: __double_surrounding__ (__init__, __str__)

## FORMATTING

### Indentation
- 4 spaces per level (NO tabs)
- continuation lines: aligned or hanging indent

### Line Length
- **79 characters** for code (PEP 8 strict)
- **72 characters** for docstrings/comments
- Note: Black uses 88, but PEP 8 says 79

### Blank Lines
- 2 blank lines around top-level functions and classes
- 1 blank line between methods in a class
- 1 blank line to separate logical sections

### Whitespace
```python
# YES
spam(ham[1], {eggs: 2})
if x == 4:
    print(x, y)
foo = (0,)
dct['key'] = lst[index]

# NO
spam( ham[ 1 ], { eggs: 2 } )
if x == 4 :
    print(x , y)
foo = (0, )
dct ['key'] = lst [index]
```

## IMPORTS
```python
# Order: stdlib → third-party → local
# Alphabetical within each group
import os
import sys

import numpy as np
import pandas as pd

from mypackage import mymodule
from mypackage.subpackage import utils

# Avoid wildcard
from module import *  # NO

# One per line for clarity
import os
import sys
# NOT: import os, sys
```

## EXPRESSIONS

### Comparisons
```python
# YES
if x is None:
if x is not None:
if not seq:  # empty sequence
if seq:      # non-empty sequence

# NO
if x == None:
if len(seq) == 0:
if len(seq):
```

### String Quotes
- Single quotes ' and double quotes " are same
- Pick one and be consistent
- Triple quotes always use """

## COMMENTS

### Inline Comments
```python
x = x + 1  # Compensate for border
```

### Block Comments
```python
# This is a block comment.
# It can span multiple lines.
# Each line starts with #.
```

### Docstrings
```python
def function(arg1, arg2):
    """Summary line.
    
    Extended description of function.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2
        
    Returns:
        Description of return value
    """
    pass
```

## TYPE HINTS (PEP 484)
```python
def greeting(name: str) -> str:
    return f'Hello {name}'

# Variables
age: int = 25
names: list[str] = []

# Optional (3.10+)
def process(data: str | None = None) -> int:
    pass
```

## FUNCTION DEFINITIONS
```python
# YES - aligned
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# YES - hanging indent
def long_function_name(
    var_one, var_two,
    var_three, var_four
):
    print(var_one)
```

## CLASS DEFINITIONS
```python
class MyClass:
    """Docstring for class."""
    
    def __init__(self, value):
        self.value = value
    
    def method(self):
        """Docstring for method."""
        return self.value
```

## BEST PRACTICES

### Exception Handling
```python
# YES
try:
    value = collection[key]
except KeyError:
    return default_value

# NO
try:
    value = collection[key]
except:
    return default_value
```

### Context Managers
```python
# YES
with open('file.txt') as f:
    data = f.read()
```

### Boolean Checks
```python
# YES
if greeting:
if not greeting:

# NO
if greeting == True:
if greeting is True:
```

### Return Statements
```python
# YES - consistent
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

# NO - inconsistent
def foo(x):
    if x >= 0:
        return math.sqrt(x)
```

## AVOID
- Trailing whitespace
- Multiple statements on one line: `if x: y = 1`
- Mutable default arguments: `def f(x=[])`
- `from module import *`
- Global variables
- Single letter variables (except i, j, k in loops)

## PROGRAMMING RECOMMENDATIONS
- Use `is` and `is not` for None checks
- Use `isinstance()` not `type()`
- Use `''.startswith()` and `''.endswith()` not string slicing
- Object type comparisons: `isinstance(obj, int)` not `type(obj) is int`
- For sequences (str, list, tuple) use empty = False: `if not seq:`
- Don't compare boolean with `==`: use `if greeting:` not `if greeting == True:`

---
Reference: https://peps.python.org/pep-0008/

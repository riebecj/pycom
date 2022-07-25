# Pycom: A Python Compiler

#### It's called README.md for a reason. Read it thoroughly before creating a new issue.


## Installation

Simply:
> git clone https://github.com/Omyyyy/pycom.git\
> cd pycom\
> pip install -r requirements.txt\
> pip install -e .

Note: Do not touch the 'pycom.py.egg-info' folder that the last command will create. It will not work otherwise.

## Usage

If you followed the installation instructions correctly, this will work in every directory:

> pycom (flags) [source file]

### Flags
* -i (bool):\
    Print additional information about compilation (such as time taken). Defaults to off.

* -r (bool):\
    Run the generated executable automatically after compilation. Defaults to off.

* -rd (bool):\
    Run the generated executable automatically after compilation, and then delete it. Defaults to off.

* -o [output] (string):\
    The string specified after the flag will be the name of the generated executable. Defaults to the name of the Python file that was passed in.

* -fm | --fastmath (bool):\
    Perform aggressive optimisations speed on calculations at the cost of some precision. Defaults to off.

### Python dependencies:
> Python version 3.10+
> 'colorama' module (install with pip install -r requirements.txt)

### C++ dependencies:
> A recent version of the g++ compiler
> The Boost C++ library; download here: https://www.boost.org/users/history/version_1_79_0.html (put the folder into usr/gcc/include/)

### Run tests

> python3 runtests.py

## What is Pycom?

Pycom is effectively a compiler for Python code, bringing it down to a native executable (20-30x the speed of Python interpetation) with C++ as 'intermediate representation'. It supports almost all Pythonic syntax along with a lot of the standard library and inbuilt functions. To see what is currently supported and not supported, check the 'Examples' section below.

## Why and when use Pycom?

Python is slow. While many optimisations and new implementations of it have vastly improved its speed, generating native code that can run as a standalone executable from Python code has never really been done. As a result, no matter what, Python code has never hit levels of speed and portability that C/C++. Pycom aims to tackle this.

Due to Pycom (currenly) not supporting all Python features from all versions, you should only really use it if you want to run simple applications with nothing too crazy or pythonic going on (again, check 'Examples')

## Examples

What Pycom supports and is good at:

High iteration loops:

```
for i in range(1, 1000001):
    if i % 3 == 0:
        print(i)
```

```
def is_prime(n):
    if n == 1:
        return 0
    for i in range(2, n):
        if n%i == 0:
            return 0

    return 1

def main():
    total = 0
    for i in range(1, 101):
        total += is_prime(i)

    print(total)
```

## Speed benchmarks and comparisons

| Benchmark | CPython | Pycom | Pycom with --fastmath | pypy | 
| ----------- | ----------- | ----------- | ----------- | ----------- |
| Multiples of 3 and 5 | 9.383s | 0.133s | 0.106s | 0.495s |
| Primes | 17.127s | 4.441s | 3.994s | 4.577s |
| Stack Operations | 8.857s | 2.132s | 1.992s | 3.113s |

(All of these can be found under ./benchmarks/)

## Supported Features

- All 'turing complete' features of Python: if, else, for, while, etc.
- f'' strings
- Some in built functions
- Some math library functions
- List comprehensions
- Python-style arbitarily large intergers

## Not supported yet

- Pythonic ways of writing certain blocks (one line if...else, etc.)
- Multi-line string literals
- A lot of libraries included in stdlib
- Classes
- Try, except and finally blocks
- Heterozygous lists; lists with more than one data type in them

## Small quirks and differences to CPython:

- If you declare an integer variable like 'n = 3', this will be interpreted as a C++ 64 bit integer instead of\
Python's arbitary size integers; to declare an integer of infinite size, use 'n: int = 3'
- Don't use semicolons in your Python source; Pycom will throw an error.
- Cannot support an 'if \__name__ == "\__main__": ' type thing; the main() function is alreaduy entry point
- If you have no functions in your code, you can do everything as you normally would:
```
print("Hello, World") # This will compile
```
- But if you have at least one user defined function, the starting point needs to be in a main() function block,\
as such:
```
def printhello():
    print("Hello!")

def main():
    printhello() 

# Will compile 
```

```
def printhello():
    print("Hello!")

printhello() 

# Will not compile
```

It's inconventient and the latter may be supported sometime, but this is just how it is for now. Also if you do have a\
'main()' function, it cannot return a value as it an entry point. The compiler will throw an error.

I will work on trying to remove these exceptions and quirks and try to make Pycom and CPython completely identical,\
but right now, it is quite experimental and has quite a bit of room for improvement.

## Contributing

Read 'CONTRIBUTING.txt'
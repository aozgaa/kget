# kget

This is a client for downloading, testing, and submitting c++ solutions to kattis.

# Installation

Requires `python3` and `make`.

```
python3 -m pip install -e git+https://github.com/aozgaa/kget.git#egg=kget
```

# Usage

## Get/Download/Fetch problem
```
kget get <problem_name>
```
eg: for problem `stringmatching`, this is:
```
$ kget get stringmatching
Downloading samples
Samples extracted to 'stringmatching'
```

The remainder of this document uses the problem `stringmatching`.

## Adding Tests

The kattis problems include sample problems, but additional cases are often needed to exercise corner cases or large problem instances.

### Input/Output Tests
Create a `<testname>.in` and `<testname>.ans` file in the problem directory, eg:
```
touch stringmatching/t1.in
touch stringmatching/t1.ans
```
The test will then run when invoked with either of the methods described below.

### (Python) Generated Input/Outputs
Create a `<testname>.in.py` and/or `<testname>.ans.py` file in the problem directory, eg:
```
touch stringmatching/t1.in.py
touch stringmatching/t1.ans.py
```
The test runner of your choice will then generate the corresponding `*.in`/`*.ans` file by capturing the stdout of the python script, called with no arguments.

## Run Tests with kget
```
$ kget test stringmatching
Testing stringmatching
make: Entering directory '/<omitted>/stringmatching'
g++ -g    solution.cpp   -o solution
running test: ./solution < stringmatching.in > stringmatching.out

real    0m0.001s
user    0m0.000s
sys     0m0.001s
test-stringmatching: comparing stringmatching.out stringmatching.ans
0a1,4
> 2 4
>
> 5
> 7
running test: ./solution < t1.in > t1.out

real    0m0.001s
user    0m0.001s
sys     0m0.000s
test-t1: comparing t1.out t1.ans
Failed tests:
stringmatching.out
make: Leaving directory '/<omitted>/stringmatching'
```

## Run Tests with make
```
$ make -C stringmatching/
make: Entering directory '/<omitted>/stringmatching'
g++ -g    solution.cpp   -o solution
running test: ./solution < stringmatching.in > stringmatching.out

real    0m0.001s
user    0m0.000s
sys     0m0.001s
test-stringmatching: comparing stringmatching.out stringmatching.ans
0a1,4
> 2 4
>
> 5
> 7
running test: ./solution < t1.in > t1.out

real    0m0.001s
user    0m0.001s
sys     0m0.000s
test-t1: comparing t1.out t1.ans
Failed tests:
stringmatching.out
make: Leaving directory '/<omitted>/stringmatching'
```

## Compare Diffs

It is sometimes useful to see an interactive diff when debugging.
The `make` target `vimdiff` or `vimdiff-<testname>` will open vimdiff with
`.in`, `.out`, and `.ans` files for comparison.

## Submit
```
$ kget submit stringmatching
Submission received. Submission ID: 101<omitted>
Submission url: https://open.kattis.com/submissions/101<omitted>
```

# Contributing

Contributions are welcome! Please feel free to open a pull request with a description of your improvement.

This application is built using [setuptools](https://setuptools.pypa.io/en/latest/userguide/index.html#).
In particular, the package can be built with
```
python -m build
```
and installed locally with
```
pip install --editable .
```

## Testing

Testing is currently manual. Only a "golden test" is checked in to compare basic clone functionality across changes:
```
python ./src/kget.py get stringmatching
diff --brief --recursive stringmatching/ testdata/stringmatching/
```

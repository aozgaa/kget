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

Create a `<testname>.in` and `<testname.ans>` file in the problem directory, eg:
```
touch stringmatching/t1.in
touch stringmatching/t1.ans
```
The test will then run when invoked with either of the methods above.

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

## Submit
```
$ kget submit stringmatching
Submission received. Submission ID: 101<omitted>
Submission url: https://open.kattis.com/submissions/101<omitted>
```





SHELL := /bin/bash

CXXFLAGS = -g

pyin := $(basename $(wildcard *.in.py)) # .in files generated via python script
pyans := $(basename $(wildcard *.ans.py)) # .ans files generated via python script
tests := $(addprefix test-, $(basename $(wildcard *.in) $(pyin)))
$(info tests found: [${tests}])
vimdiffs := $(addprefix vimdiff-, $(basename $(wildcard *.in)))

.ONESHELL:
.DELETE_ON_ERROR:

.PHONY: test test-% clean
.INTERMEDIATE: test_failures.out
test: solution $(tests)
	@if [ -s test_failures.out ]; then echo "Failed tests:" ; cat test_failures.out ; else echo "Success, all tests passed."; fi
	@rm -f test_failures.out
test-%: %.out %.ans
	@echo "$@: comparing $^"
	@if ! diff $^; then echo $* >> test_failures.out ; fi

solution: solution.cpp

.PRECIOUS: %.out
%.out: %.in solution
	@echo "running test: ./solution < $< > $@"
	@time ./solution < $< > $@

.PRECIOUS: %.in
%.in: %.in.py
	@echo "generating test input: python $< > $@"
	@python $< > $@

.PRECIOUS: %.ans
%.ans: %.ans.py
	@echo "generating test answer: python $< > $@"
	@python $< > $@

clean:
	rm -f solution
	rm -f *.out
	rm -f $(pyin)
	rm -f $(pyans)

# recommend using :qa to quit all windows at once
.PHONY: vimdiff vimdiff-%
vimdiff: solution $(vimdiffs)
	@echo "Done"
vimdiff-%: .EXTRA_PREREQS = %.in
vimdiff-%: %.ans %.out
	@vimdiff $^ -c ':to split %:r.in'

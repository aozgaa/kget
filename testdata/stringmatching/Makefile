SHELL := /bin/bash

CXXFLAGS = -g

tests := $(addprefix test-, $(basename $(wildcard *.in)))
vimdiffs := $(addprefix vimdiff-, $(basename $(wildcard *.in)))

.PHONY: test test-%
test: solution $(tests)
	@echo "Success, all tests passed."
test-%: %.out %.ans
	@echo "$@: comparing $^"
	@diff $^

.PHONY: vimdiff vimdiff-%
vimdiff: solution $(vimdiffs)
	@echo "Done"
vimdiff-%: .EXTRA_PREREQS = %.in
vimdiff-%: %.ans %.out
	vimdiff $^ -c ':to split %:r.in'

clean:
	rm -f solution
	rm -f *.out

solution: solution.cpp

.PRECIOUS: %.out
%.out: %.in solution
	@echo "running test: ./solution < $< > $@"
	@time ./solution < $< > $@

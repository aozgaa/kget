import argparse
import pathlib
import configparser
import os
import requests
import re
import subprocess
import sys
import tempfile
import zipfile
import shutil

config_path = os.path.join(pathlib.Path.home(), ".kattisrc")

cfg = configparser.ConfigParser()
if not cfg.read(config_path):
    raise ValueError(f"could not find config at {config_path}")

bits_stub = """#if defined(__clang__)
#include<cassert>
#include<cctype>
#include<climits>
#include<cmath>
#include<cstddef>
#include<cstdint>
#include<cstdio>
#include<cstdlib>
#include<cstring>
#include<ctime>

#include <array>
#include <bitset>
#include <deque>
// #include <flat_map>
// #include <flat_set>
#include <forward_list>
#include <list>
#include <map>
// #include <mdspan>
#include <queue>
#include <set>
// #include <span>
#include <stack>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include <algorithm>
#include <functional>
#include <limits>
#include <numeric>
// #include <print>
#include <utility>

using namespace std;
#elif defined(__GNUG__)
#include <bits/stdc++.h>
#include <bits/extc++.h>

using namespace std;
using namespace __gnu_pbds;
typedef tree<string, null_type, less<string>, rb_tree_tag,
        tree_order_statistics_node_update> ost;

#endif
"""

cxx_stub = """#include "bits.h"

int main() {
    return 0;
}
"""

makefile_stub = """
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
"""


def download(soln_dir: str, problem: str):
    hostname = cfg["kattis"]["hostname"]
    res = requests.get(
        f"https://{hostname}/problems/{problem}/file/statement/samples.zip"
    )

    if res.status_code == 404:
        print(f"problem {problem} not found")
        return
    print("Downloading samples")
    with tempfile.TemporaryFile() as tf:
        tf.write(res.content)
        with zipfile.ZipFile(tf, "r") as zip_ref:
            zip_ref.extractall(f"{soln_dir}")
            print(f"Samples extracted to '{soln_dir}'")
    open(f"{soln_dir}/solution.cpp", "w").write(cxx_stub)
    open(f"{soln_dir}/bits.h", "w").write(bits_stub)
    open(f"{soln_dir}/Makefile", "w").write(makefile_stub)


def login(cfg):
    """Log in to Kattis using the access information in a kattisrc file

    Returns a requests.Response with cookies needed to be able to submit
    """
    username = cfg["user"]["username"]
    token = cfg["user"]["token"]
    loginurl = cfg["kattis"]["loginurl"]

    res = requests.post(
        loginurl,
        data={"user": username, "token": token, "script": "true"},
        headers={"User-Agent": "kget-submit"},
    )

    if res.status_code != 200:
        print(f"login status code: {res.status_code}")
        sys.exit(1)

    return res


def submit(cfg, cookies, soln_dir: str, problem: str, files=[], tag=""):
    sub_files = []
    if files == []:
        files = os.listdir(soln_dir)
    for fname in files:
        if fname.endswith(".cpp") or fname.endswith(".h"):
            if fname.startswith("gen"):
                continue  # skip any gen scripts
            with open(f"{soln_dir}/{fname}") as f:
                sub_files.append(
                    (
                        "sub_file[]",
                        (
                            fname,
                            f.read(),
                            "application/octet-stream",
                        ),
                    )
                )

    data = {
        "submit": "true",
        "submit_ctr": 2,
        "language": "C++",
        "mainclass": "",
        "problem": problem,
        "tag": tag,
        "script": "true",
    }

    submit_url = cfg["kattis"]["submissionurl"]

    res = requests.post(
        submit_url,
        data=data,
        files=sub_files,
        cookies=cookies,
        headers={"User-Agent": "kget-submit"},
    )

    if res.status_code != 200:
        print(f"login status code: {res.status_code}")
        sys.exit(1)

    return res


def get_submit_url(cfg, sres):
    url = cfg["kattis"]["submissionsurl"]

    m = re.search(r"Submission ID: (\d+)", sres.text)
    if not m:
        print("could not find submission id")
        return None
    id = m.group(1)
    return f"{url}/{id}"


def main():
    parser = argparse.ArgumentParser(prog="kget", description="CLI to kattis problems")
    parser.add_argument(
        "command", nargs=None, help="command to run, must be one of get,test,submit"
    )
    parser.add_argument(
        "solution_dir",
        nargs=None,
        help="directory containing problem. The basename of the canonical path must have the same name as the problem",
    )
    # fixme: make separate parser for subcommands?
    parser.add_argument(
            "files",
            nargs='*',
            help="list of files to submit. Only applicable for submit command"
            )
    args = parser.parse_args()
    problem = os.path.basename(os.path.realpath(args.solution_dir))
    if args.command == "get":
        download(args.solution_dir, problem)
    elif args.command == "test":
        print(f"Testing {args.solution_dir}")
        cp = subprocess.run([shutil.which("make"), "-C", args.solution_dir])
        sys.exit(cp.returncode)
    elif args.command == "submit":
        lres = login(cfg)
        sres = submit(cfg, lres.cookies, args.solution_dir, problem, args.files)
        plain_result = sres.text.replace("<br />", "\n")
        print(plain_result)
        print(f"Submission url: {get_submit_url(cfg, sres)}")
    else:
        print(f"invalid command: {args.command}")
        parser.print_help()


if __name__ == "__main__":
    main()

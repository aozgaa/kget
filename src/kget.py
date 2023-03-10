# [ ] add submitter
# [ ] add tester -- shell out to make

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

cxx_stub = """#include <bits/stdc++.h>
#include <bits/extc++.h>

using namespace std;
using namespace __gnu_pbds;

typedef tree<string, null_type, less<string>, rb_tree_tag,
        tree_order_statistics_node_update> ost;

int main() {
    return 0;
}
"""

makefile_stub = """SHELL := /bin/bash

CXXFLAGS = -g

tests := $(addprefix test-, $(basename $(wildcard *.in)))
vimdiffs := $(addprefix vimdiff-, $(basename $(wildcard *.in)))

test_failed := 0

.ONESHELL:
.PHONY: test test-%
test: solution $(tests)
	@if [ -s test_failures.out ] ; then \
		echo "Failed tests:" ; \
		cat test_failures.out ; \
	else \
		echo "Success, all tests passed." ; \
	fi
	rm -f test_failures.out
test-%: %.out %.ans
	@echo "$@: comparing $^"
	@if ! diff $^; then echo $< >> test_failures.out ; fi

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
"""


def download(soln_dir: str):
    problem = os.path.basename(soln_dir)
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


def submit(cfg, cookies, soln_dir, tag=""):
    problem = os.path.basename(soln_dir)
    sub_files = []
    with open(f"{soln_dir}/solution.cpp") as f:
        sub_files = [
            (
                "sub_file[]",
                (
                    "solution.cpp",
                    f.read(),
                    "application/octet-stream",
                ),
            )
        ]

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
        help="directory containing problem. Must have same name as the problem",
    )
    args = parser.parse_args()
    if args.command == "get":
        download(args.solution_dir)
    elif args.command == "test":
        print(f"Testing {args.solution_dir}")
        cp = subprocess.run([shutil.which("make"), "-C", args.solution_dir])
        sys.exit(cp.returncode)
    elif args.command == "submit":
        lres = login(cfg)
        sres = submit(cfg, lres.cookies, args.solution_dir)
        plain_result = sres.text.replace("<br />", "\n")
        print(plain_result)
        print(f"Submission url: {get_submit_url(cfg, sres)}")
    else:
        print("invalid command")
        parser.print_help()
    pass


if __name__ == "__main__":
    main()
    # download(sys.argv[1])

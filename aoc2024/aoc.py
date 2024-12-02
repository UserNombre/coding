#!/usr/bin/env python3

import sys
import argparse
import traceback
import importlib
from pathlib import Path

def solve(string_input):
    processed_input = aoc.process_input(string_input)
    result = aoc.compute_result(processed_input)
    return result

def run(path):
    string_input = path.read_text()
    result = solve(string_input)
    print(result)

def check():
    result = solve(aoc.sample_input)
    if result == aoc.sample_result:
        print("Check succeeded")
        print(f"{result} == {aoc.sample_result}")
    else:
        print("Check failed")
        print(f"{result} != {aoc.sample_result}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("path")
    args = parser.parse_args()

    path = Path(args.path)
    module_name = str(path.with_suffix(""))
    globals()["aoc"] = importlib.import_module(module_name)

    if args.command == "run":
        run(path.with_suffix(".txt"))
    elif args.command == "check":
        check()
    else:
        raise UserWarning(f"command {args.command} does not exist")

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(e)
    except ModuleNotFoundError as e:
        print(e)
    except UserWarning as e:
        print(f"Usage error: {e}")
    except Exception as e:
        print(traceback.format_exc())

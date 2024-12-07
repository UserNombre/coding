#!/usr/bin/env python3

import sys
import code
import argparse
import traceback
import importlib
from pathlib import Path

def run(args):
    if args.filename:
        path = Path(args.filename)
    else:
        path = Path(args.path).with_suffix(".txt")
    string_input = path.read_text()
    if args.interactive:
        code.interact(local=dict(globals(), **locals()))
    result = aoc.solve(string_input)
    print(result)

def check(args):
    if args.interactive:
        code.interact(local=dict(globals(), **locals()))
    result = aoc.solve(aoc.sample_input)
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
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true")
    parser.add_argument("-f", "--filename")
    args = parser.parse_args()

    module_name = str(Path(args.path).with_suffix(""))
    globals()["aoc"] = importlib.import_module(module_name)

    aoc.debug = args.debug
    if args.command == "run":
        run(args)
    elif args.command == "check":
        check(args)
    else:
        raise UserWarning(f"command {args.command} does not exist")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except FileNotFoundError as e:
        print(e)
    except ModuleNotFoundError as e:
        print(e)
    except UserWarning as e:
        print(f"Usage error: {e}")
    except Exception as e:
        print(traceback.format_exc())

#!/usr/bin/env python3

import helpers
from pathlib import Path

def run(module):
    if module.input_file:
        input_file = Path(module.input_file)
    else:
        input_file = Path(module.__file__).with_suffix(".txt")
    string_input = input_file.read_text()
    result = module.solve(string_input)
    if module.debug:
        print()
    print(result)
    if module.interact:
        shell(module, locals())

def check(module):
    if not module.sample_input or not module.sample_result:
        raise UserWarning(f"sample_input or sample_result variables not defined")
    result = module.solve(module.sample_input)
    if module.debug:
        print()
    if result == module.sample_result:
        print("Check succeeded")
        print(f"{result} == {module.sample_result}")
    else:
        print("Check failed")
        print(f"{result} != {module.sample_result}")
    if module.interact:
        shell(module, locals())

def shell(module, variables={}):
    import code
    import readline
    import rlcompleter

    variables.update(vars(module))
    readline.set_completer(rlcompleter.Completer(variables).complete)
    readline.parse_and_bind("tab: complete")
    code.interact(local=variables)

def main(command, module_file, debug=False, interact=False, profile=False, input_file=None):
    import importlib

    module_name = str(Path(module_file).with_suffix(""))
    module = importlib.import_module(module_name)
    module.helpers = helpers
    module.debug = debug
    module.interact = interact
    module.profile = profile
    module.input_file = input_file

    if command in ["run", "check", "shell"]:
        module.mode = command
        if profile:
            from line_profiler import LineProfiler
            from inspect import getmembers, isfunction
            profiler = LineProfiler(*(member[1] for member in getmembers(module, isfunction)))
            profiler.enable()
        globals()[command](module)
        if profile:
            profiler.disable()
            helpers.print_separator("-")
            profiler.print_stats()
    else:
        raise UserWarning(f"command {command} does not exist")

def cli_main():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command to execute on the module")
    parser.add_argument("module_file", help="path to the python file containing the code")
    parser.add_argument("-d", "--debug", action="store_true", help="print debugging information")
    parser.add_argument("-i", "--interact", action="store_true", help="drop into an interactive shell after solve() is called")
    parser.add_argument("-p", "--profile", action="store_true", help="profile the code executed within the module")
    parser.add_argument("-f", "--input-file", help="path to the input file")
    args = parser.parse_args()

    try:
        if args.debug:
            sys.stdout.write("\033[?25l")
        main(args.command, args.module_file, args.debug, args.interact, args.profile, args.input_file)
    except KeyboardInterrupt:
        pass
    except (FileNotFoundError, ModuleNotFoundError, AttributeError) as e:
        print(f"{type(e).__name__}: {e}")
    except UserWarning as e:
        print(f"Usage error: {e}")
    except AssertionError as e:
        print(f"Assertion error: {e}")
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        if args.debug:
            import pdb
            sys.stdout.write("\033[?25h")
            pdb.post_mortem()
    finally:
        sys.stdout.write("\033[?25h")

if __name__ == "__main__":
    cli_main()

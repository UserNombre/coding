#!/usr/bin/env python3

from pathlib import Path

def run(module):
    if module.input_path:
        input_path = Path(module.input_path)
    else:
        input_path = Path(module.__file__).with_suffix(".txt")
    string_input = input_path.read_text()
    result = module.solve(string_input)
    print(result)
    if module.interact:
        shell(module, locals())

def check(module):
    result = module.solve(module.sample_input)
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

def main(command, module_path, input_path=None, debug=False, interact=False):
    import importlib

    module_name = str(Path(module_path).with_suffix(""))
    module = importlib.import_module(module_name)
    module.input_path = input_path
    module.debug = debug
    module.interact = interact

    if command in ["run", "check", "shell"]:
        module.mode = command
        globals()[command](module)
    else:
        raise UserWarning(f"command {command} does not exist")

def cli_main():
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("module_path")
    parser.add_argument("-p", "--input-path")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-i", "--interact", action="store_true")
    args = parser.parse_args()

    try:
        if args.debug:
            sys.stdout.write("\033[?25l")
        main(args.command, args.module_path, args.input_path, args.debug, args.interact)
    except KeyboardInterrupt:
        pass
    except FileNotFoundError as e:
        print(e)
    except ModuleNotFoundError as e:
        print(e)
    except UserWarning as e:
        print(f"Usage error: {e}")
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

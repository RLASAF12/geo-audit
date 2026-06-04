"""Entry-point shim for the geo-audit CLI.
The main logic lives in geo-audit.py; this importable module lets
setuptools wire up the 'geo-audit' console script.
"""
import runpy
import os
import sys


def main():
    script = os.path.join(os.path.dirname(__file__), "geo-audit.py")
    sys.exit(runpy.run_path(script, run_name="__main__").get("_exit_code", 0))


if __name__ == "__main__":
    main()

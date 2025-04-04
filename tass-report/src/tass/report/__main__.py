from .core.parse import parse, parse_result
from .report import report
from argparse import ArgumentParser
from pathlib import Path


def main(reporter, result, no_validate):
    _reporter = parse(Path(reporter).resolve(), no_validate)
    _result = parse_result(Path(result).resolve(), no_validate)
    report(_reporter, _result)


if __name__ == "__main__":
    argparse = ArgumentParser()

    argparse.add_argument("--reporter", required=True)
    argparse.add_argument("--result", required=True)

    argparse.add_argument("--no-validate", action="store_false",
                          default=True)

    main(**vars(argparse.parse_args()))
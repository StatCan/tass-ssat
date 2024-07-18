import argparse
import json
from . import conf as conf
from pathlib import Path


conversions = [
        "excel"
    ]


def scenario_excel(source, target):
    print(
        "Converting Excel:", source,
        "scenario to JSON:", target, "\n\n"
        )
    s = conf.convert(source)
    t = target + ".json"
    json.dump(s, open(t, 'w+', encoding='utf-8'), indent=4)
    return str(Path(t).resolve())


def main(convert, source, target):

    if convert == conversions[0]:
        return scenario_excel(source, target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("convert", choices=conversions)
    parser.add_argument("--source", "-s", required=True)
    parser.add_argument("--target", "-t", required=True)
    main(**vars(parser.parse_args()))

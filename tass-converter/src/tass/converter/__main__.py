import argparse
from . import convert as conf


conversions = [
        "excel"
    ]


def scenario(source, target):
    print(
        "Converting Excel:", source,
        "scenario to JSON:", target, "\n\n"
        )

    return conf.convert(source, target)


def main(source, target):

    scenario(source, target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # parser.add_argument("convert", choices=conversions)
    parser.add_argument("--source", "-s", required=True)
    parser.add_argument("--target", "-t", required=True)
    main(**vars(parser.parse_args()))

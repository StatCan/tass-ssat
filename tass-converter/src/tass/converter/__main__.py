import argparse
import json
from . import conf as conf
from . import page_conf as page_conf
from pathlib import Path


conversions = [
        "scenario",
        "specs",
        "pages"
    ]


def scenario(source, target):
    print(
        "Converting Excel:", source,
        "scenario to JSON:", target, "\n\n"
        )
    s = conf.convert(source)
    t = target + ".json"
    json.dump(s, open(t, 'w+', encoding='utf-8'), indent=4)
    return str(Path(t).resolve())


def specs(source, target):
    print(
        "Converting Excel specs:", source,
        "to page summary for:", target, "\n\n"
        )
    s = page_conf.convert_to_excel(source)
    t = target + ".xlsx"
    s.save(t)
    return str(Path(t).resolve())


def page(source, target):
    print(
        "Converting page summary:", source,
        "to JSON POM for:", target, "\n\n"
        )
    s = page_conf.convert_to_json(source)
    t = target + ".json"
    json.dump(s, open(t, 'w+', encoding='utf-8'), indent=4)
    return str(Path(t).resolve())


def main(convert, source, target):

    if convert == conversions[0]:
        return scenario(source, target)
    elif convert == conversions[1]:
        return specs(source, target)
    elif convert == conversions[2]:
        return page(source, target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("convert", choices=conversions)
    parser.add_argument("--source", "-s", required=True)
    parser.add_argument("--target", "-t", required=True)
    main(**vars(parser.parse_args()))

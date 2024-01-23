import argparse
import tass.tools.convert.conf as conf
import tass.tools.convert.page_conf as page_conf


conversions = [
        "scenario",
        "specs",
        "pages"
    ]


def scenario(source):
    print("Converting Excel:", source, "scenario to JSON\n\n")
    return conf.convert(source)

def specs(source, target):
    print("Converting Excel specs:", source, " to page summary for:", target, "\n\n")
    return page_conf.convert_to_excel(source, target)

def page(source, target):
    print("Converting page summary:", source, " to JSON POM for:", target, "\n\n")
    return page_conf.convert_to_json(source, target)


def main(args):
    method = args.convert

    if method == conversions[0]:
        return scenario(args.source)
    elif method == conversions[1]:
        if args.target and isinstance(args.target, str):
            return specs(args.source, args.target)
    elif method == conversions[2]:
        if args.target and isinstance(args.target, str):
            return page(args.source, args.target)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("convert", choices=conversions)
    parser.add_argument("--source", "-s", required=True)
    parser.add_argument("--target", "-t")
    main(parser.parse_args())

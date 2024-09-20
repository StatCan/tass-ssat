import argparse
from . import core

def main(file):
	core.execute(file)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("--file", "-f", required=True)
	main(**vars(parser.parse_args()))
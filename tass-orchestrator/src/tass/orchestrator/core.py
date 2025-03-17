import json
from pathlib import Path
from tass.converter import __main__ as tass_conv
from tass.core import __main__ as tass_base

def run_conversion(conversion):
	tass_conv.main(conversion["conv-prop"]["convert"],
		           conversion["conv-prop"]["source"],
		           conversion["conv-prop"]["target"])

def run_executor(executor):
	tass_base.main(executor["base-prop"]["file_path"],
		           executor["base-prop"]["no_validate"])

def run_reporter(reporter):
	# TASS reporter module not currently implemented.
	pass

def run_flows(file):
	try:
		f = open(Path(file).resolve())
	except IOError as e:
		print(e)
		return
	with f:
		orch = json.load(f)

	for flow in orch["Test_flow"]:
		for conversion in flow["conversion"]:
			run_conversion(conversion)

		for executor in flow["executor"]:
			run_executor(executor)

		for reporter in flow["reporter"]:
			run_reporter(reporter)
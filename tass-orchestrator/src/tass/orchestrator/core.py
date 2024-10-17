import json
import tass.converter
from tass.base import __main__

def run_conversion(conversion):
	print("######### test conversion ############")
	print(conversion)

def run_executor(executor):
	print("########## test executor ############")
	print(executor)
	tass.base.__main__.main(executor, True)

def run_reporter(reporter):
	print("############ test reporter ##############")
	print("TASS reporter module not currently implemented.")
	print(reporter)

def run_flows(file):
	print("Executor!")
	print(file)
	try:
		f = open(file)
	except IOError as e:
		print(e)
		return
	with f:
		orch = json.load(f)

	for flow in orch["Test_flow"]:
		print("######## Test flow #########")
		print(flow)

		for conversion in flow["conversion"]:
			run_conversion(conversion)

		for executor in flow["executor"]:
			run_executor(executor)

		for reporter in flow["reporter"]:
			run_reporter(reporter)

	print("######## Test orch #########")
	print(orch)
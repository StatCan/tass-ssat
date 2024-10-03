import json

def execute(file):
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
			print("######### test conversion ############")
			print(conversion)

		for executor in flow["executor"]:
			print("########## test executor ############")
			print(executor)

		for reporter in flow["reporter"]:
			print("############ test reporter ##############")
			print(reporter)

	print("######## Test orch #########")
	print(orch)
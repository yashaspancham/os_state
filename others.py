
def machine_id():
	with open("/etc/machine-id","r") as f:
		return f.read()
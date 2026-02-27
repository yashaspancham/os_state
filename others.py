from datetime import datetime

def get_machine_id():
	with open("/etc/machine-id","r") as f:
		return f.read()


def current_time():
	return str(datetime.now())

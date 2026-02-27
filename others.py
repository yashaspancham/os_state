from datetime import datetime
import os

def get_machine_id():
	with open("/etc/machine-id","r") as f:
		return f.read()


def current_time():
	return str(datetime.now())


def get_absolute_path():
	absolute_path = os.path.abspath(__file__)
	absolute_path_list=absolute_path.split("/")[:-1]
	return "/".join(absolute_path_list)
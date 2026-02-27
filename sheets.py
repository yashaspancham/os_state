import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import others
load_dotenv(others.get_absolute_path()+"/.env")


def auth():
	scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
	try:
		CREDS_FILE=os.getenv("CREDS_FILE")
		absolute_path_creds_file=others.get_absolute_path()+"/"+CREDS_FILE
		creds = ServiceAccountCredentials.from_json_keyfile_name(absolute_path_creds_file, scope)
		client = gspread.authorize(creds)
		return client
	except FileNotFoundError:
		print("Error: 'creds.json' not found. Make sure the file exists.")
		return None
	except Exception as e:
		print(f"Authentication falied with error: {e}")
		return None


def ping_sheet(client,SHEET_ID):
    	try:
        	sheet=client.open_by_key(SHEET_ID)
    	except Exception as e:
        	print(f"Connection Error: {e}")
        	exit(1)


def check_page_exists(spreadsheet):
    	machine_id=others.get_machine_id()
    	pages = spreadsheet.worksheets()
    	page_titles=[p.title for p in pages]
    	if machine_id in page_titles:
        	return True
    	return False


def create_page(spreadsheet):
    	machine_id=others.get_machine_id()
    	CPU_ROW=["number_of_cores", "cpu_usage_%",]
    	MEMORY_ROW=["memory_used_%", "memory_used_gb", "total_memory_gb", "free_memory_gb",]
    	DISK_ROW=["disk_used_gb", "disk_used_%", "disk_total_gb", "disk_free_gb",]
    	OS_ROW=["distro_name", "disttro_pretty_name", "distro", "os_name", "os_verison", "kernal_version", "os_architecture"]
    	FIRST_ROW=["Time Stamp"]+CPU_ROW+MEMORY_ROW+DISK_ROW+OS_ROW
    	new_sheet=spreadsheet.add_worksheet(title=machine_id,rows=100, cols=17)
    	new_sheet.append_row(FIRST_ROW)


def add_entry(spreadsheet,state:dict):
    	machine_id=others.get_machine_id()
    	cpu_info=state["cpu"]
    	memory_info=state["memory"]
    	disk_info=state["disk"]
    	os_info=state["os"]
    	cpu_row=[cpu_info['number_of_cores'],cpu_info['cpu_usage_%']]
    	memory_row=[memory_info["memory_used_%"], memory_info["memory_used_gb"], memory_info["total_memory_gb"], memory_info["free_memory_gb"]]
    	disk_row=[disk_info["disk_used_gb"], disk_info["disk_used_%"], disk_info["disk_total_gb"], disk_info["disk_free_gb"]]
    	os_row=[os_info["distro_name"], os_info["disttro_pretty_name"], os_info["distro"], os_info["os_name"], os_info["os_verison"], os_info["kernal_version"], os_info["os_architecture"]]
    	row=[others.current_time()]+cpu_row+memory_row+disk_row+os_row
    	machine_sheet=spreadsheet.worksheet(machine_id)
    	machine_sheet.append_row(row)

def send_to_sheet(state:dict):
    	client=auth()
    	SHEET_ID=os.getenv("SHEET_ID")
    	if not client:
        	exit(1)
    	ping_sheet(client,SHEET_ID)
    	spreadsheet=client.open_by_key(SHEET_ID)
    	if not check_page_exists(spreadsheet):
        	create_page(spreadsheet)

    	add_entry(spreadsheet,state)

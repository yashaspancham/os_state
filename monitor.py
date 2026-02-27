from  metrics import moniter_and_collect
from sheets import send_to_sheet
import others


def main():
	state=moniter_and_collect()
	send_to_sheet(state)

if __name__ == "__main__":
	main()
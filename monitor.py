import metrics
import sheets
import others

def main():
    state={
        "cpu":metrics.cpu_info(),
        "memory":metrics.memory_info(),
        "disk":metrics.disk_info(),
        "os":metrics.os_info(),
    }
    print(f"machine-id: {others.machine_id()} \nstate: {state}")
    sheets.add_entry()

if __name__ == "__main__":
    main()

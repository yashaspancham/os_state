import utils


def main():
        state={
                "cpu":utils.cpu_info(),
                "memory":utils.memory_info(),
                "disk":utils.disk_info(),
                "os":utils.os_info(),
        }
        print(state)


if __name__ == "__main__":
        main()
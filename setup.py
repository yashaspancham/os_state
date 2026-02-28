import subprocess
import sys
import os


def create_env(sheet_id):
        env_line_1 = "SHEET_ID=" + sheet_id
        env_line_2 = "CREDS_FILE=creds.json"
        with open(".env", "a") as env_file:
                env_file.write(env_line_1 + "\n")
                env_file.write(env_line_2 + "\n")



def check_sheet_id(sheet_id):
        if not sheet_id:
                print("Sheet_ID not Found")
                exit(1)
        if type(sheet_id) != str:
                print("Sheet_ID must be of type `str`")
                exit(1)


def create_venv(venv_name: str = "os_venv") -> str:
        if os.path.isdir(venv_name):
                print(f"virtualenv '{venv_name}' already exists")
                return venv_name
        print(f"creating virtualenv '{venv_name}'...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_name])
        return venv_name


def is_venv_active():
        if os.environ.get("VIRTUAL_ENV"):
                return True
        base_prefix = getattr(sys, "base_prefix", None)
        real_prefix = getattr(sys, "real_prefix", None)
        prefix = getattr(sys, "prefix", None)
        if real_prefix and real_prefix != prefix:
                return True
        if base_prefix and base_prefix != prefix:
                return True
        return False


def activate_venv():
        if is_venv_active():
                return
        venv_name = "os_venv"
        py = os.path.join(venv_name, "bin", "python")
        if not os.path.exists(py):
                py = os.path.join(venv_name, "Scripts", "python.exe")
        if not os.path.exists(py):
                raise FileNotFoundError(f"python executable not found in virtualenv '{venv_name}'")
        os.environ["VIRTUAL_ENV"] = os.path.abspath(venv_name)
        print(f"restarting under virtualenv python: {py}")
        os.execv(py, [py] + sys.argv)


def parse_requirements(path: str) -> list[str]:
        """Return a list of pip-compatible requirement strings.

        Handles both `pip freeze` output and the two‑column table produced by
        `pip list`. For each non-empty, non-comment line, the first one or two
        whitespace-separated tokens are joined with ``==``.  Example input:

            certifi              2026.1.4

        becomes ``"certifi==2026.1.4"``.
        """

        reqs: list[str] = []
        with open(path) as f:
                for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                                continue
                        parts = line.split()
                        if len(parts) == 1:
                                reqs.append(parts[0])
                        else:
                                reqs.append(parts[0] + "==" + parts[1])
        return reqs


def install_libs(requirements_file: str = "requirements.txt", venv_name: str = "os_venv") -> None:
        # convert file if necessary
        sanitized = None
        try:
                sanitized = parse_requirements(requirements_file)
        except FileNotFoundError:
                raise
        # write temporary file if we changed formatting
        if sanitized:
                tmp = requirements_file + ".tmp"
                with open(tmp, "w") as fh:
                        fh.write("\n".join(sanitized) + "\n")
                requirements_file = tmp
        pip_path = os.path.join(venv_name, "bin", "pip")
        if not os.path.exists(pip_path):
                pip_path = os.path.join(venv_name, "Scripts", "pip.exe")
        if not os.path.exists(pip_path):
                raise FileNotFoundError(f"pip not found in virtualenv '{venv_name}'")
        subprocess.check_call([pip_path, "install", "--upgrade", "pip"]) 
        subprocess.check_call([pip_path, "install", "-r", requirements_file])



def main():
        sheet_id = input("Enter the Sheet_id: ")
        check_sheet_id(sheet_id)
        create_env(sheet_id)
        venv = create_venv()
        if not is_venv_active():
                activate_venv()
        install_libs(venv_name=venv)


if __name__ == "__main__":
        main()
import psutil
import platform
import shutil

def cpu_info():
        return {
                "number_of_cores": psutil.cpu_count(),
                "cpu_usage_%": psutil.cpu_percent(interval=1),
        }


def memory_info():
        mem = psutil.virtual_memory()
        return {
                "memory_used_%": mem.percent,
                "memory_used_gb": round(mem.used / (1024**3), 2),
                "total_memory_gb": round(mem.total / (1024**3), 2),
                "free_memory_gb": round(mem.available / (1024**3), 2),
        }


def disk_info():
        # retuns disk_used, total_disk, free_disk
        usage = psutil.disk_usage("/")
        total_gb = usage.total / (1024**3)
        used_gb = usage.used / (1024**3)
        used_percentage = (used_gb/total_gb)*100
        free_gb = usage.free / (1024**3)
        return {
                "disk_used_gb": round(used_gb, 2),
                "disk_used_%": round(used_percentage, 2),
                "disk_total_gb": round(total_gb, 2),
                "disk_free_gb": round(free_gb, 2),
        }


def os_info():
        # returns os_type, os_version, os_architecture, boot_time
        print({"distro_name":platform.freedesktop_os_release()})
        distro_name=platform.freedesktop_os_release()
        return {
                "distro_name":distro_name["NAME"],
                "disttro_pretty_name":distro_name["PRETTY_NAME"],
                "distro":distro_name["ID_LIKE"],    
                "os_name": platform.system(),
                "os_verison":platform.version(),
                "kernal_version":platform.release(),
                "os_architecture":platform.machine(),
        }


def hardware_info():
        pass

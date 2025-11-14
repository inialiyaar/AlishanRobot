import psutil

def get_system_stats():
    ram = psutil.virtual_memory().percent

    cpu = psutil.cpu_percent(interval=0.5)

    disk = psutil.disk_usage('/').percent

    return ram, cpu, disk
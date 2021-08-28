import psutil
import platform
import GPUtil
from tabulate import tabulate
from datetime import datetime


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


print("=" * 40, "System Information", "=" * 40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")

# boot
print("=" * 40, "Boot Time", "=" * 40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

# cpu info
print("=" * 40, "CPU Info", "=" * 40)
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# cpu freq
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# cpu usage
print("CPU Usage Per Core: ")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")
# gpu info
print("=" * 40, "GPU Information", "=" * 40)
gpus = GPUtil.getGPUs()
list_gpus = []
for gpu in gpus:
    gpu_id = gpu.id
    gpu_name = gpu.name
    gpu_load = f"{gpu.load * 100}%"
    gpu_free_memory = f"{gpu.memoryFree}MB"
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    gpu_util_memory = f"{gpu.memoryUtil}%"
    gpu_temp = f"{gpu.temperature}°C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory, gpu_total_memory, gpu_util_memory, gpu_temp,
        gpu_uuid

    ))

print(tabulate(list_gpus, headers=(
    "id", "name", "load", "free memory", "used memory", "total memory", "util memory", "temperature", "uuid")))
# memory info
print("=" * 40, "Memory Information", "=" * 40)
svmem = psutil.virtual_memory()

print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("=" * 20, "SWAP", "=" * 20)
# get the swap memory if it exists
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Used: {get_size(swap.used)}")
print(f"Free: {get_size(swap.free)}")
print(f"Percentage: {swap.percent}%")
# Disk info
print("=" * 40, "Disk Information", "=" * 40)
print("Partitions and Usage:")
# get all partitions
part = psutil.disk_partitions()
for partition in part:
    print(f"=== Device: {partition.device} ===")
    print(f" Mountpoint: {partition.mountpoint}")
    print(f" File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        continue
    print(f" Total size: {get_size(partition_usage.total)}")
    print(f" Used: {get_size(partition_usage.used)}")
    print(f" Free: {get_size(partition_usage.free)}")
    print(f" Percentage: {partition_usage.percent}%")

disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total Write: {get_size(disk_io.write_bytes)}")
# Network info
print("=" * 40, "Network Information", "=" * 40)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f" Ip Address: {address.address}")
            print(f" Netmask: {address.netmask}")
            print(f" Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f" MAC Address: {address.address}")
            print(f" Netmask: {address.netmask}")
            print(f" Broadcast MAC: {address.broadcast}")

net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

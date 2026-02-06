import psutil
import time
from datetime import datetime


# ===== OCI Configuration =====
PROJECT_NAME = "OCI Data Centre Monitoring (Simulation)"
ENVIRONMENT = "OCI-UK-LONDON-DC01"
RACK_ID = "RACK-07"

CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 85

ALERT_COOLDOWN_SECONDS = 60
SUMMARY_EVERY_N_CYCLES = 12  # 12 * 5 seconds = 60 seconds
_last_alert_time = {"cpu": 0, "memory": 0, "disk": 0}
# ==============================



def get_system_metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    return cpu, memory, disk


def log_metrics(cpu, memory, disk, status):
    with open("system_log.txt", "a") as f:
        f.write(f"{datetime.now()} | STATUS: {status} | CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%\n")



def can_alert(metric_key):
    now = time.time()
    if now - _last_alert_time[metric_key] >= ALERT_COOLDOWN_SECONDS:
        _last_alert_time[metric_key] = now
        return True
    return False





def check_alerts(cpu, memory, disk):
    if cpu > CPU_THRESHOLD and can_alert("cpu"):
        message = f"[{ENVIRONMENT}][{RACK_ID}] CRITICAL: CPU usage high ({cpu}%)."
        print("🔴", message)
        log_alert(message)

    if memory > MEMORY_THRESHOLD and can_alert("memory"):
        message = f"[{ENVIRONMENT}][{RACK_ID}] CRITICAL: Memory usage high ({memory}%)."
        print("🔴", message)
        log_alert(message)

    if disk > DISK_THRESHOLD and can_alert("disk"):
        message = f"[{ENVIRONMENT}][{RACK_ID}] WARNING: Disk usage high ({disk}%) - notify capacity planning."
        print("⚠️", message)
        log_alert(message)


def get_health_status(cpu, memory, disk):
    if cpu > CPU_THRESHOLD or memory > MEMORY_THRESHOLD:
        return "CRITICAL"
    if disk > DISK_THRESHOLD:
        return "WARNING"
    return "OK"



def log_alert(message):
    with open("alerts_log.txt", "a") as f:
        f.write(f"{datetime.now()} | {message}\n")



def main():
    print(f"{PROJECT_NAME}")
    print(f"Environment: {ENVIRONMENT} | Rack: {RACK_ID}")
    print("Status: ACTIVE\n")


    cycle = 0

    try:
        while True:
            cpu, memory, disk = get_system_metrics()
            status = get_health_status(cpu, memory, disk)

            print(f"[{status}] CPU: {cpu}% | Memory: {memory}% | Disk: {disk}%")

            log_metrics(cpu, memory, disk, status)
            check_alerts(cpu, memory, disk)

            cycle += 1
            if cycle % SUMMARY_EVERY_N_CYCLES == 0:
                summary = f"[{ENVIRONMENT}][{RACK_ID}] 60s Summary -> CPU: {cpu}% | MEM: {memory}% | DISK: {disk}% | STATUS: {status}"
                print("📊", summary)
                log_alert(summary)

            time.sleep(5)

    except KeyboardInterrupt:
        shutdown_msg = f"[{ENVIRONMENT}][{RACK_ID}] Monitoring stopped by user."
        print("\n🛑", shutdown_msg)
        log_alert(shutdown_msg)




if __name__ == "__main__":
    main()

# combined_monitor.py

import threading
import psutil
import time
import subprocess
import csv
import os

# CSV file paths
cpu_memory_csv = "cpu_memory_data.csv"
system_info_csv = "system_info_data.csv"

# Create CSV files and write headers if they don't exist
if not os.path.exists(cpu_memory_csv):
    with open(cpu_memory_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Core1", "Core2", "Core3", "Core4", "MemoryUsage"])

if not os.path.exists(system_info_csv):
    with open(system_info_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPUInfo", "MemoryInfo", "BatteryInfo"])

# Monitor CPU and Memory Usage with psutil and save to CSV
def monitor_cpu_memory():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        memory_info = psutil.virtual_memory()
        
        print("CPU Utilization:")
        for i, usage in enumerate(cpu_percent):
            print(f"  Core {i+1}: {usage}%")
        
        print(f"Memory Usage: {memory_info.percent}%")
        
        # Save data to CSV
        with open(cpu_memory_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S")] + cpu_percent + [memory_info.percent])
        
        print("="*40)
        time.sleep(5)  # Adjust the interval as needed

# Function to run PowerShell commands and capture their output
def run_powershell_command(command):
    try:
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Failed to run command '{command}': {e}")
        return None

# Monitor additional system information using PowerShell and save to CSV
def monitor_system_info():
    while True:
        # CPU Information
        cpu_info_command = "Get-WmiObject Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed"
        cpu_info = run_powershell_command(cpu_info_command)
        
        # Memory Information
        memory_info_command = "Get-WmiObject Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory"
        memory_info = run_powershell_command(memory_info_command)
        
        # Battery Information (if applicable)
        battery_info_command = "Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus"
        battery_info = run_powershell_command(battery_info_command)

        print("System Information:")
        print("CPU Information:")
        print(cpu_info)
        
        print("Memory Information:")
        print(memory_info)
        
        if battery_info:
            print("Battery Information:")
            print(battery_info)
        else:
            print("No battery information available.")
        
        # Save data to CSV
        with open(system_info_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), cpu_info, memory_info, battery_info if battery_info else "N/A"])
        
        print("="*40)
        time.sleep(60)  # Update less frequently for system info

# Main function to run all monitoring in separate threads
if __name__ == "__main__":
    threads = []
    
    # Thread for CPU and memory monitoring
    t1 = threading.Thread(target=monitor_cpu_memory)
    # Thread for system information monitoring using PowerShell
    t2 = threading.Thread(target=monitor_system_info)
    
    threads.extend([t1, t2])
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Ensure all threads complete
    for t in threads:
        t.join()

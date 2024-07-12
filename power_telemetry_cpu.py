import psutil
import time
import csv
import os
import subprocess

# CSV file paths
cpu_memory_csv = "cpu_memory_data.csv"
system_info_csv = "system_info_data.csv"

# Create CSV files and write headers if they don't exist
def create_csv_files():
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
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    memory_info = psutil.virtual_memory()
    
    # Save data to CSV
    with open(cpu_memory_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S")] + cpu_percent + [memory_info.percent])

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
    # CPU Information
    cpu_info_command = "Get-WmiObject Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed"
    cpu_info = run_powershell_command(cpu_info_command)
    
    # Memory Information
    memory_info_command = "Get-WmiObject Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory"
    memory_info = run_powershell_command(memory_info_command)
    
    # Battery Information (if applicable)
    battery_info_command = "Get-WmiObject Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus"
    battery_info = run_powershell_command(battery_info_command)
    
    # Save data to CSV
    with open(system_info_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), cpu_info, memory_info, battery_info if battery_info else "N/A"])

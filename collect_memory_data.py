import subprocess
import os
import pandas as pd
import psutil

def run_powershell_command(command):
    """
    Run a PowerShell command and return the output.
    """
    try:
        result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True, check=True)
        print(result.stdout)  # Print stdout for debugging
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running PowerShell command: {e}")
        print(f"Command: {command}")
        print(f"stderr: {e.stderr}")
        return None

def collect_perfmon_memory_data():
    """
    Collect memory data using Performance Monitor.
    """
    command = 'Get-Counter -Counter "\\Memory\\Available Bytes" -SampleInterval 1 -MaxSamples 60 | Select-Object -ExpandProperty CounterSamples | Select-Object Timestamp, CookedValue | ConvertTo-Csv -NoTypeInformation | Out-File -FilePath data/perfmon_memory_data.csv -Encoding utf8'
    output = run_powershell_command(command)
    if output is not None:
        print("Collected Performance Monitor memory data.")

def collect_process_memory_data():
    """
    Collect memory utilization data for each process.
    """
    try:
        process_list = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            process_list.append({
                'PID': proc.info['pid'],
                'Process': proc.info['name'],
                'Memory Usage (MB)': proc.info['memory_info'].rss / 1024 / 1024  # Memory in MB
            })
        df = pd.DataFrame(process_list)
        df.to_csv('data/process_memory_data.csv', index=False)
        print("Collected process memory data.")
    except Exception as e:
        print(f"Error collecting Process Memory data: {e}")
def collect_core_memory_usage():
    """
    Collect memory usage data for all cores.
    """
    try:
        core_memory_usage = []
        mem_info = psutil.virtual_memory()
        # Get the memory usage for each core
        for core in range(psutil.cpu_count(logical=True)):
            # Example method of calculating memory usage based on available memory
            core_usage = psutil.cpu_percent(percpu=True, interval=1)[core]  # CPU usage percentage for the core
            # Assuming uniform distribution of memory
            available_memory_mb = mem_info.available / (1024 * 1024)  # Convert bytes to MB
            core_memory_usage.append((core, available_memory_mb * (core_usage / 100)))
        df = pd.DataFrame(core_memory_usage, columns=['Core', 'Memory Usage (MB)'])
        df.to_csv('data/core_memory_usage.csv', index=False)
        print("Collected Core Memory Usage data.")
    except Exception as e:
        print(f"Error collecting Core Memory Usage data: {e}")



if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    collect_perfmon_memory_data()
    collect_process_memory_data()
    collect_core_memory_usage()


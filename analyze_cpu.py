import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Load the data
df = pd.read_csv("cpu_memory_data.csv", parse_dates=["Timestamp"])

# Print the columns to inspect the available data
print("Columns in CSV file:", df.columns)

# Define the columns for memory usage and CPU utilization
memory_usage_column = 'MemoryUsage'
cpu_columns = ['Core1', 'Core2', 'Core3', 'Core4']  # Adjust this list if you have more cores

# Check if the 'MemoryUsage' column is present and plot memory usage over time
if memory_usage_column not in df.columns:
    print(f"Column '{memory_usage_column}' not found in CSV file.")
else:
    # Initialize lists to store the data
    timestamps = df['Timestamp']
    memory_usage_percentages = df[memory_usage_column]

    # Plot Memory Usage over Time
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, memory_usage_percentages, label="Memory Usage (%)", color='blue', linestyle='-', marker='o')
    plt.xlabel("Time")
    plt.ylabel("Memory Usage (%)")
    plt.title("Memory Usage Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("memory_usage_over_time.png")
    plt.show()

# Check if the CPU utilization columns are present and plot CPU utilization for each core
missing_cpu_columns = [col for col in cpu_columns if col not in df.columns]
if missing_cpu_columns:
    print(f"Columns {missing_cpu_columns} not found in CSV file.")
else:
    # Initialize lists to store CPU utilization data
    core_usage_data = {core: df[core] for core in cpu_columns}

    # Plot CPU Utilization over Time for each core
    plt.figure(figsize=(12, 8))
    for core, usage in core_usage_data.items():
        plt.plot(timestamps, usage, label=f"{core} Usage (%)", linestyle='-', marker='o')

    plt.xlabel("Time")
    plt.ylabel("CPU Usage (%)")
    plt.title("CPU Usage Over Time by Core")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("cpu_usage_over_time.png")
    plt.show()

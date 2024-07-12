import pandas as pd
import matplotlib.pyplot as plt

def analyze_cpu_data(cpu_data_file):
    # Read CPU utilization data from CSV
    cpu_data = pd.read_csv(cpu_data_file)

    # Plot CPU utilization over time
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(cpu_data['Timestamp'], cpu_data['Core1'], label='Core 1', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core2'], label='Core 2', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core3'], label='Core 3', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core4'], label='Core 4', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core5'], label='Core 5', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core6'], label='Core 6', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core7'], label='Core 7', marker='o')
    ax.plot(cpu_data['Timestamp'], cpu_data['Core8'], label='Core 8', marker='o')

    ax.set_xlabel('Timestamp')
    ax.set_ylabel('CPU Utilization (%)')
    ax.set_title('CPU Utilization Over Time')
    ax.legend()
    ax.grid(True)
    
    return fig

if __name__ == "__main__":
    # Example usage
    cpu_data_file = "cpu_memory_data.csv"
    fig = analyze_cpu_data(cpu_data_file)
    plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def analyze_perfmon_memory_data():
    """
    Analyze memory data collected from Performance Monitor and generate a graph.
    """
    try:
        if not os.path.isfile('data/perfmon_memory_data.csv'):
            raise FileNotFoundError('perfmon_memory_data.csv not found. Please ensure Performance Monitor data is collected.')

        df = pd.read_csv('data/perfmon_memory_data.csv')
        if 'Timestamp' not in df.columns or 'CookedValue' not in df.columns:
            raise KeyError("Required columns are missing from the Performance Monitor data.")
        
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.rename(columns={'CookedValue': 'Available Bytes'}, inplace=True)
        df['Available MBytes'] = df['Available Bytes'] / 1024 / 1024
        
        plt.figure(figsize=(12, 8))
        sns.lineplot(data=df, x='Timestamp', y='Available MBytes', color='blue')
        plt.title('Available Memory Over Time (Performance Monitor)')
        plt.xlabel('Time')
        plt.ylabel('Available Memory (MB)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/perfmon_memory_usage.png')
        plt.show()
        print("Generated graph for Performance Monitor data.")
    except Exception as e:
        print(f"Error analyzing Performance Monitor data: {e}")

def analyze_process_memory_data():
    """
    Analyze memory utilization by individual processes.
    """
    try:
        if not os.path.isfile('data/process_memory_data.csv'):
            raise FileNotFoundError('process_memory_data.csv not found. Please collect process memory data.')

        df = pd.read_csv('data/process_memory_data.csv')
        if 'Process' not in df.columns or 'Memory Usage (MB)' not in df.columns:
            raise KeyError("Required columns are missing from the Process Memory data.")
        
        # Drop rows where 'Process' is NaN
        df = df.dropna(subset=['Process'])

        # Drop the 'PID' column as it's not needed for the analysis
        df = df.drop(columns=['PID'])

        # Sort the processes by memory usage in descending order and take the top 10
        df_sorted = df.sort_values(by='Memory Usage (MB)', ascending=False).head(10)

        plt.figure(figsize=(12, 8))
        sns.barplot(data=df_sorted, x='Process', y='Memory Usage (MB)', color='purple')  # Show only top 10 processes
        plt.title('Memory Utilization by Process')
        plt.xlabel('Process')
        plt.ylabel('Memory Usage (MB)')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('reports/process_memory_utilization.png')
        plt.show()
        print("Generated graph for memory utilization by process.")
    except Exception as e:
        print(f"Error analyzing Process Memory data: {e}")

import pandas as pd
import matplotlib.pyplot as plt

def  analyze_core_memory_usage():
    try:
        df = pd.read_csv('data/core_memory_usage.csv')
        plt.figure(figsize=(12, 6))
        plt.bar(df['Core'], df['Memory Usage (MB)'], color='teal')
        plt.title('Memory Utilization per Core')
        plt.xlabel('Core')
        plt.ylabel('Memory Usage (MB)')
        plt.tight_layout()
        plt.savefig('reports/core_memory_usage.png')
        plt.show()
        print("Generated graph for Core Memory data.")
    except Exception as e:
        print(f"Error analyzing Core Memory data: {e}")

def analyze_wmic_memory_data():
    """
    Analyze memory data collected from WMIC and generate a graph.
    """
    try:
        if not os.path.isfile('data/wmic_memory_data.csv'):
            raise FileNotFoundError('wmic_memory_data.csv not found. Please collect WMIC memory data.')

        # Read CSV file and clean up data
        df = pd.read_csv('data/wmic_memory_data.csv', delimiter=',', encoding='utf-8', skiprows=1)
        df = df.rename(columns={'Capacity': 'Capacity (Bytes)'})

        # Convert Capacity from bytes to GB
        df['Capacity (GB)'] = df['Capacity (Bytes)'] / (1024 ** 3)

        plt.figure(figsize=(12, 8))
        plt.bar(range(len(df['Capacity (GB)'])), df['Capacity (GB)'])
        plt.title('Memory Capacity (GB)')
        plt.xlabel('Memory Chip')
        plt.ylabel('Memory Capacity (GB)')
        plt.xticks(range(len(df['Capacity (GB)'])), [f'Chip {i+1}' for i in range(len(df['Capacity (GB)']))])
        plt.tight_layout()
        plt.savefig('reports/wmic_memory_capacity.png')
        plt.show()
        print("Generated graph for WMIC Memory Data.")
    except Exception as e:
        print(f"Error analyzing WMIC Memory data: {e}")

def analyze_task_manager_memory_data():
    """
    Analyze memory utilization data collected from Task Manager and generate a graph.
    """
    try:
        if not os.path.isfile('data/task_manager_memory_data.csv'):
            raise FileNotFoundError('task_manager_memory_data.csv not found. Please collect Task Manager memory data.')

        df = pd.read_csv('data/task_manager_memory_data.csv', encoding='utf-8-sig')  # Ensure correct encoding
        if 'Name' not in df.columns or 'Memory Usage (MB)' not in df.columns:
            raise KeyError("Required columns are missing from the Task Manager Memory data. Check if 'Name' and 'Memory Usage (MB)' are present.")

        # Rename columns to match the expected names
        df.rename(columns={'Name': 'Process'}, inplace=True)

        # Drop rows where 'Process' is NaN
        df = df.dropna(subset=['Process'])

        # Show only the top 10 processes with the highest memory usage
        df_sorted = df.sort_values(by='Memory Usage (MB)', ascending=False).head(10)

        plt.figure(figsize=(16, 10))  # Adjusted for better readability
        sns.set_style('darkgrid')  # Set plot style
        sns.barplot(data=df_sorted, x='Process', y='Memory Usage (MB)', color='blue')  # Show only top 10 processes
        plt.title('Task Manager Memory Utilization by Process')
        plt.xlabel('Process')
        plt.ylabel('Memory Usage (MB)')
        plt.xticks(rotation=45, ha='right')  # Rotate and align X-axis labels
        plt.tight_layout()
        plt.savefig('reports/task_manager_memory_utilization.png')
        plt.show()
        print("Generated graph for Task Manager memory data.")
    except Exception as e:
        print(f"Error analyzing Task Manager Memory data: {e}")

if __name__ == '__main__':
    analyze_perfmon_memory_data()
    analyze_process_memory_data()
    analyze_core_memory_usage()
    analyze_wmic_memory_data()
    analyze_task_manager_memory_data()

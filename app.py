import streamlit as st
import os
import pandas as pd
import threading
import matplotlib.pyplot as plt
import seaborn as sns
from power_telemetry_cpu import create_csv_files, monitor_cpu_memory, monitor_system_info
from analyze_cpu import analyze_cpu_data
from network import plot_network_statistics
from battery import generate_battery_report
from batteryplot import plot_battery_data
from collect_memory_data import collect_perfmon_memory_data, collect_process_memory_data, collect_core_memory_usage
from analyze_memory_data import analyze_perfmon_memory_data, analyze_process_memory_data, analyze_core_memory_usage

# Ensure the 'data' and 'reports' directories exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('reports'):
    os.makedirs('reports')

# CSV file paths
perfmon_memory_csv = "data/perfmon_memory_data.csv"
process_memory_csv = "data/process_memory_data.csv"
core_memory_csv = "data/core_memory_usage.csv"
cpu_memory_csv = "data/cpu_memory_data.csv"
system_info_csv = "data/system_info_data.csv"

# Function to create CSV files and write headers if they don't exist
def create_csv_files():
    if not os.path.exists(cpu_memory_csv):
        with open(cpu_memory_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Core1", "Core2", "Core3", "Core4", "Core5", "Core6", "Core7", "Core8", "MemoryUsage"])

    if not os.path.exists(system_info_csv):
        with open(system_info_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "CPUInfo", "MemoryInfo", "BatteryInfo"])

# Function to display CPU utilization data and perform data collection
def display_cpu_utilization():
    if st.button("Collect Data"):
        collection_placeholder = st.empty()
        collection_placeholder.warning("Data collection is in progress...")

        create_csv_files()

        t1 = threading.Thread(target=monitor_cpu_memory)
        t2 = threading.Thread(target=monitor_system_info)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        collection_placeholder.empty()
        st.success("Data collection complete. Results saved to CSV files.")

    if st.button("Visualise Data"):
        cpu_data = pd.read_csv(cpu_memory_csv)
        st.write("### CPU Utilization Over Time")
        fig = analyze_cpu_data(cpu_memory_csv)
        st.pyplot(fig)

# Function to collect memory data when button is clicked
def collect_memory_data():
    collect_perfmon_memory_data(output_file=perfmon_memory_csv)
    collect_process_memory_data(output_file=process_memory_csv)
    collect_core_memory_usage(output_file=core_memory_csv)

# Function to display memory analysis when button is clicked
def display_memory_analysis():
    st.write("### Memory Analysis")

    # Display Performance Monitor Memory Data
    if os.path.exists(perfmon_memory_csv):
        st.write("#### Performance Monitor Memory Data")
        df_perfmon = pd.read_csv(perfmon_memory_csv)
        st.dataframe(df_perfmon)
        
        st.write("##### Performance Monitor Memory Data Graph")
        df_perfmon['Timestamp'] = pd.to_datetime(df_perfmon['Timestamp'])
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_perfmon, x='Timestamp', y='Available MBytes', color='blue')
        plt.title('Available Memory Over Time (Performance Monitor)')
        plt.xlabel('Time')
        plt.ylabel('Available Memory (MB)')
        plt.xticks(rotation=45)
        st.pyplot()

    else:
        st.write("#### Performance Monitor Memory Data not found. Please collect data first.")

    # Display Process Memory Data
    if os.path.exists(process_memory_csv):
        st.write("#### Process Memory Data")
        df_process = pd.read_csv(process_memory_csv)
        st.dataframe(df_process)
        
        st.write("##### Process Memory Data Graph")
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_process.head(10), x='Process', y='Memory Usage (MB)', color='purple')
        plt.title('Memory Utilization by Process')
        plt.xlabel('Process')
        plt.ylabel('Memory Usage (MB)')
        plt.xticks(rotation=90)
        st.pyplot()

    else:
        st.write("#### Process Memory Data not found. Please collect data first.")

    # Display Core Memory Usage Data
    if os.path.exists(core_memory_csv):
        st.write("#### Core Memory Usage Data")
        df_core = pd.read_csv(core_memory_csv)
        st.dataframe(df_core)
        
        st.write("##### Core Memory Usage Data Graph")
        plt.figure(figsize=(12, 6))
        plt.bar(df_core['Core'], df_core['Memory Usage (MB)'], color='teal')
        plt.title('Memory Utilization per Core')
        plt.xlabel('Core')
        plt.ylabel('Memory Usage (MB)')
        st.pyplot()

    else:
        st.write("#### Core Memory Usage Data not found. Please collect data first.")

# Function to display NIC statistics
def display_nic_statistics():
    st.write("### NIC Monitoring")
    fig = plot_network_statistics()
    st.pyplot(fig)

# Function to display Battery data and plots
def display_battery_data():
    generate_battery_report()
    fig1, fig2, fig3, fig4, daily_efficiency, histogram_path, hourly_plot_path, average_discharge_rate, correlation = plot_battery_data()

    st.write("### Battery Monitoring")
    st.write(f"**Average Discharge Rate:** {average_discharge_rate:.2f} mWh/hr")
    st.write(f"**Correlation between Discharge (mWh) and Battery (%):** {correlation:.2f}")

    st.pyplot(fig1)
    st.pyplot(fig2)
    st.pyplot(fig3)
    st.pyplot(fig4)

    st.write("### Daily Efficiency")
    st.dataframe(daily_efficiency)

    st.image(histogram_path, caption="Discharge Rate Histogram")
    st.image(hourly_plot_path, caption="Hourly Discharge Rates")

# Set up the Streamlit UI
st.set_page_config(layout="wide")
st.title("System Monitoring")

# Create tabs for CPU, MEMORY, NIC, BATTERY
tabs = ["CPU", "MEMORY", "NIC", "BATTERY"]
selected_tab = st.sidebar.selectbox("Select a device to monitor:", tabs)

if selected_tab == "CPU":
    display_cpu_utilization()

elif selected_tab == "MEMORY":
    st.write("### MEMORY Monitoring")
    st.write("Click below to collect memory data:")
    if st.button("Collect Memory Data"):
        collect_memory_data()
        st.success("Memory data collection complete.")

    st.write("Click below to analyze memory data:")
    if st.button("Analyze Memory Data"):
        display_memory_analysis()

elif selected_tab == "NIC":
    display_nic_statistics()

elif selected_tab == "BATTERY":
    display_battery_data()

import streamlit as st
import os
import pandas as pd
import threading
import matplotlib.pyplot as plt
import seaborn as sns

from network import plot_network_statistics
from battery import generate_battery_report
from batteryplot import plot_battery_data
import subprocess
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
def collect_cpu_data():
    subprocess.run(['python', 'power_telemetry_cpu.py'])


def analyze_cpu_data():
    subprocess.run(['python', 'analyze_cpu.py'])
    cwd = os.getcwd()

# List all files in the current directory
    files_in_cwd = os.listdir(cwd)

# Filter only the .png files
    png_files = [file for file in files_in_cwd if file.endswith('.png')]

# Display each .png file
    for png_file in png_files:
        image_path = os.path.join(cwd, png_file)
        image = plt.imread(image_path)
        st.image(image, caption=png_file, use_column_width=True)

def collect_memory_data():
    subprocess.run(['python', 'collect_memory_data.py'])

# Function to analyze memory data and plot graphs
def analyze_memory_data():
    subprocess.run(['python', 'analyze_memory_data.py'])
    # Display graphs from 'reports' folder
    report_files = os.listdir('reports')
    for file in report_files:
        if file.endswith('.png'):
            image_path = os.path.join('reports', file)
            image = plt.imread(image_path)
            st.image(image, caption=file, use_column_width=True)



def display_cpu_utilization():
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Collect Data'):
            collection_placeholder = st.empty()
            collection_placeholder.warning("Data collection is in progress...")

            collect_cpu_data()

            collection_placeholder.empty()
            st.success("Data collection complete. Results saved to CSV files.")

    with col2:
        if st.button('Visualize Data'):
            analyze_cpu_data()

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
        analyze_memory_data()

elif selected_tab == "NIC":
    display_nic_statistics()

elif selected_tab == "BATTERY":
    display_battery_data()

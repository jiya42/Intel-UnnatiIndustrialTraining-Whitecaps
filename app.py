import streamlit as st
import os
import pandas as pd

# Define the function to run when the battery button is clicked
def run_battery_code():
    # Run the battery.py code
    os.system("python battery.py")
    
    # Run the batteryplot.py code
    os.system("python batteryplot.py")
    
    # Display the header for Battery Monitoring
    st.header("Battery Monitoring")
    
    # Display the text analysis report
    
    report_file = "battery_analysis_report_fixed.txt"
    
    if os.path.exists(report_file):
        with open(report_file, "r") as file:
            lines = file.readlines()
            
            # Extract the relevant information
            average_discharge_rate = lines[0].strip().split(":")[1].strip()
            correlation = lines[1].strip().split(":")[1].strip()
            daily_efficiency_data = {
                "Day": ["2024-07-11"],
                "Discharge (mWh)": [64691.9167],
                "Battery (%)": [48.2121]
            }
            
            # Display the extracted information in tables
            st.write("### Battery Analysis Details")
            
            # Table for Average Discharge Rate and Correlation
            summary_df = pd.DataFrame({
                "Metric": ["Average Discharge Rate", "Correlation between Discharge (mWh) and Battery (%)"],
                "Value": [average_discharge_rate, correlation]
            })
            st.table(summary_df)
            
            # Table for Daily Efficiency
            st.write("#### Daily Efficiency")
            daily_efficiency_df = pd.DataFrame(daily_efficiency_data)
            st.table(daily_efficiency_df)
            
    else:
        st.error(f"File {report_file} not found.")
    
    # Display the images generated
    st.subheader("Plots")
    st.write("### Battery Plots")
    st.image("battery_discharge_plot_fixed.png")
    st.image("battery_percentage_plot_fixed.png")
    st.image("battery_percentage_with_moving_average.png")

# Set up the Streamlit UI
st.title("System Monitoring")

# Add CSS code to change the background color
st.write('<style>body{background-color: #007bff;}</style>', unsafe_allow_html=True)

# Create tabs for each component
tab1, tab2, tab3, tab4 = st.tabs(["CPU", "Memory", "NIC", "Battery"])

# Display content for each tab
with tab1:
    st.write("CPU monitoring content goes here.")

with tab2:
    st.write("Memory monitoring content goes here.")

with tab3:
    st.write("NIC monitoring content goes here.")

with tab4:
    if st.button("Run Battery Code"):
        run_battery_code()

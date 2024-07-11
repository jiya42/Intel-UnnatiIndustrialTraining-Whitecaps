import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
df = pd.read_csv('C:\\Users\\honey\\windows-tdp\\battery\\battery_report.csv')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime, set errors to NaT

# Check for invalid dates
print(f"Number of invalid dates: {df['Date'].isna().sum()}")  # Count of invalid date entries

# Filter out invalid dates
df = df.dropna(subset=['Date'])
df.reset_index(drop=True, inplace=True)

# Recalculate discharge values, ensuring no negative values are included
df['Discharge (mWh)'] = (df['Battery (%)'].shift(1) - df['Battery (%)']) * 100
df = df[df['Discharge (mWh)'] >= 0]  # Filter out negative discharge values

# Calculate time differences in hours
df['Time Delta'] = df['Date'].diff().dt.total_seconds() / 3600  # Hours
df = df[df['Time Delta'] > 0]  # Ensure 'Time Delta' is positive
df['Discharge (mWh)'] = df['Discharge (mWh)'] * df['Time Delta']  # Adjust discharge calculation

# Drop the first row which will have NaN values for 'Discharge (mWh)'
df.dropna(subset=['Discharge (mWh)'], inplace=True)

# Save the fixed CSV data
df.to_csv('C:\\Users\\honey\\windows-tdp\\battery\\battery_report.csv', index=False)

# Plot discharge over time
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Discharge (mWh)'], marker='o', linestyle='-', color='b')
plt.xlabel('Date')
plt.ylabel('Discharge (mWh)')
plt.title('Battery Discharge Over Time')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('battery_discharge_plot_fixed.png')
plt.show()

# Plot battery percentage over time
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Battery (%)'], marker='o', linestyle='-', color='r')
plt.xlabel('Date')
plt.ylabel('Battery (%)')
plt.title('Battery Percentage Over Time')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('battery_percentage_plot_fixed.png')
plt.show()

# Plot battery data with a moving average to smooth out the fluctuations
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Battery (%)'], marker='o', linestyle='-', color='r', label='Battery (%)')
plt.plot(df['Date'], df['Battery (%)'].rolling(window=5).mean(), color='b', label='5-period Moving Average')
plt.xlabel('Date')
plt.ylabel('Battery (%)')
plt.title('Battery Percentage Over Time with Moving Average')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.savefig('battery_percentage_with_moving_average.png')
plt.show()

# Calculate average discharge per hour
df['Hour'] = df['Date'].dt.hour
df['Day'] = df['Date'].dt.date

# Group by day and calculate the average discharge per hour
daily_efficiency = df.groupby('Day').agg({'Discharge (mWh)': 'sum', 'Battery (%)': 'mean'})
print(daily_efficiency)

# Compute rate of discharge
df['Discharge Rate (mWh/hr)'] = df['Discharge (mWh)'] / (df['Date'].diff().dt.total_seconds() / 3600)  # mWh per hour
df.dropna(subset=['Discharge Rate (mWh/hr)'], inplace=True)

# Average discharge rate
average_discharge_rate = df['Discharge Rate (mWh/hr)'].mean()
print(f"Average Discharge Rate: {average_discharge_rate:.2f} mWh/hr")

# Compute correlation between Battery (%) and Discharge (mWh)
correlation = df['Discharge (mWh)'].corr(df['Battery (%)'])
print(f"Correlation between Discharge (mWh) and Battery (%): {correlation:.2f}")

# Create a summary report
with open('battery_analysis_report_fixed.txt', 'w') as file:
    file.write(f"Average Discharge Rate: {average_discharge_rate:.2f} mWh/hr\n")
    file.write(f"Correlation between Discharge (mWh) and Battery (%): {correlation:.2f}\n")
    file.write(f"Daily Efficiency:\n{daily_efficiency}\n")
    file.write("Plots saved as 'battery_discharge_plot_fixed.png', 'battery_percentage_plot_fixed.png', and 'battery_percentage_with_moving_average.png'\n")

# Additional Analysis

# Plot histogram of Discharge Rate
plt.figure(figsize=(10, 5))
plt.hist(df['Discharge Rate (mWh/hr)'], bins=20, color='purple', edgecolor='black')
plt.xlabel('Discharge Rate (mWh/hr)')
plt.ylabel('Frequency')
plt.title('Histogram of Discharge Rate')
plt.grid(True)
plt.tight_layout()
plt.savefig('discharge_rate_histogram.png')
plt.show()

# Compare Discharge Across Different Hours
hourly_discharge = df.groupby('Hour').agg({'Discharge (mWh)': 'mean'})
plt.figure(figsize=(12, 6))
plt.plot(hourly_discharge.index, hourly_discharge['Discharge (mWh)'], marker='o', linestyle='-', color='green')
plt.xlabel('Hour of Day')
plt.ylabel('Average Discharge (mWh)')
plt.title('Average Discharge per Hour')
plt.grid(True)
plt.xticks(range(24))
plt.tight_layout()
plt.savefig('hourly_discharge_plot.png')
plt.show()

# Save hourly discharge data
hourly_discharge.to_csv('hourly_discharge_summary.csv')

# Assess Battery Health Over Time
df['Battery Degradation (%)'] = df['Battery (%)'].pct_change() * 100  # Percentage change
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Battery Degradation (%)'], marker='o', linestyle='-', color='orange')
plt.xlabel('Date')
plt.ylabel('Battery Degradation (%)')
plt.title('Battery Degradation Over Time')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('battery_degradation_plot.png')
plt.show()

# Save battery degradation data
df[['Date', 'Battery Degradation (%)']].to_csv('battery_degradation_summary.csv', index=False)

# Calculate Power Consumption
df['Power Consumption (W)'] = df['Discharge (mWh)'] / df['Time Delta']  # mWh per hour to W
average_power_consumption = df['Power Consumption (W)'].mean()
print(f"Average Power Consumption: {average_power_consumption:.2f} W")

# Save power consumption data
df[['Date', 'Power Consumption (W)']].to_csv('power_consumption_summary.csv', index=False)

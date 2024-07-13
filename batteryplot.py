import pandas as pd
import matplotlib.pyplot as plt
import os

working_dir = os.getcwd()

def plot_battery_data():
    file_path = os.path.join(working_dir, 'battery_report.csv')
    df = pd.read_csv(file_path)

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])
    df.reset_index(drop=True, inplace=True)

    df['Discharge (mWh)'] = (df['Battery (%)'].shift(1) - df['Battery (%)']) * 100
    df = df[df['Discharge (mWh)'] >= 0]

    df['Time Delta'] = df['Date'].diff().dt.total_seconds() / 3600
    df = df[df['Time Delta'] > 0]
    df['Discharge (mWh)'] = df['Discharge (mWh)'] * df['Time Delta']
    df.dropna(subset=['Discharge (mWh)'], inplace=True)

    df.to_csv(file_path, index=False)

    df['Discharge Rate (mWh/hr)'] = df['Discharge (mWh)'] / df['Time Delta']
    average_discharge_rate = df['Discharge Rate (mWh/hr)'].mean()
    correlation = df['Discharge (mWh)'].corr(df['Battery (%)'])

    # Daily Efficiency Table
    df['Day'] = df['Date'].dt.date
    daily_efficiency = df.groupby('Day').agg({'Discharge (mWh)': 'sum', 'Battery (%)': 'mean'}).reset_index()

    # Histogram of Discharge Rates
    plt.figure(figsize=(10, 6))
    plt.hist(df['Discharge Rate (mWh/hr)'], bins=30, edgecolor='black')
    plt.xlabel('Discharge Rate (mWh/hr)')
    plt.ylabel('Frequency')
    plt.title('Discharge Rate Histogram')
    plt.grid(True)
    histogram_path = os.path.join(working_dir, 'discharge_rate_histogram.png')
    plt.savefig(histogram_path)
    plt.close()

    # Hourly Discharge Plot
    df['Hour'] = df['Date'].dt.hour
    hourly_discharge = df.groupby(['Day', 'Hour']).agg({'Discharge (mWh)': 'sum'}).reset_index()
    plt.figure(figsize=(10, 6))
    for day in hourly_discharge['Day'].unique():
        day_data = hourly_discharge[hourly_discharge['Day'] == day]
        plt.plot(day_data['Hour'], day_data['Discharge (mWh)'], marker='o', linestyle='-', label=str(day))
    plt.xlabel('Hour of the Day')
    plt.ylabel('Discharge (mWh)')
    plt.title('Hourly Discharge Rates')
    plt.legend(title='Date', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    hourly_plot_path = os.path.join(working_dir, 'hourly_discharge_plot.png')
    plt.savefig(hourly_plot_path)
    plt.close()

    # Create figures for Streamlit
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df['Date'], df['Discharge (mWh)'], marker='o', linestyle='-', color='b')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Discharge (mWh)')
    ax1.set_title('Battery Discharge Over Time')
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax1.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(df['Date'], df['Battery (%)'], marker='o', linestyle='-', color='r')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Battery (%)')
    ax2.set_title('Battery Percentage Over Time')
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax2.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.plot(df['Date'], df['Battery (%)'].rolling(window=5).mean(), color='b', label='5-period Moving Average')
    ax3.set_xlabel('Date')
    ax3.set_ylabel('Battery (%)')
    ax3.set_title('Battery Percentage Over Time with Moving Average')
    ax3.grid(True)
    ax3.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax3.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    ax3.legend()

    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.plot(daily_efficiency['Day'], daily_efficiency['Discharge (mWh)'], marker='o', linestyle='-', color='green')
    ax4.set_xlabel('Day')
    ax4.set_ylabel('Discharge (mWh)')
    ax4.set_title('Daily Discharge Over Time')
    ax4.grid(True)
    ax4.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    ax4.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    return fig1, fig2, fig3, fig4, daily_efficiency, histogram_path, hourly_plot_path, average_discharge_rate, correlation

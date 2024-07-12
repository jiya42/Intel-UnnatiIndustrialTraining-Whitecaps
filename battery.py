import subprocess
from bs4 import BeautifulSoup
import csv
import os
import tempfile

working_dir = os.getcwd()

def generate_battery_report():
    # Define the paths
    csv_report_path = os.path.join(working_dir, "battery_report.csv")

    # Create a temporary file in the current working directory
    with tempfile.NamedTemporaryFile(dir=working_dir, suffix='.html', delete=False) as tmp_file:
        html_report_path = tmp_file.name

    # Generate the battery report using powercfg
    subprocess.run(["powercfg", "/batteryreport", "/output", html_report_path], check=True)

    print(f"Battery life report saved to file path {html_report_path}.")

    # Parse the HTML report
    with open(html_report_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all tables in the HTML document
    tables = soup.find_all('table')

    # Print all table headers for debugging
    for idx, table in enumerate(tables):
        header_row = table.find('tr')
        headers = [th.text.strip() for th in header_row.find_all('th') or header_row.find_all('td')]
        print(f"Table {idx+1} Header Columns: {headers}")

    # Find the table with relevant battery data
    data_table = None

    # Look for a table with the required columns
    for table in tables:
        header_row = table.find('tr')
        if header_row:
            headers = [th.text.strip() for th in header_row.find_all('th') or header_row.find_all('td')]
            if 'START TIME' in headers and 'STATE' in headers and 'SOURCE' in headers and 'CAPACITY REMAINING' in headers:
                data_table = table
                break

    if data_table is None:
        raise ValueError("No suitable table found for battery data extraction")

    # Extract table header
    header_row = data_table.find('tr')
    columns = header_row.find_all('th') or header_row.find_all('td')

    # Print the columns for debugging
    print(f"Header Columns: {[col.text.strip() for col in columns]}")

    # Check if there are at least 4 columns in the header
    if len(columns) < 4:
        raise ValueError("Expected at least 4 columns in the table header")

    # Extract data rows from the table
    rows = data_table.find_all('tr')[1:]  # Skip the header row

    # Prepare data for CSV
    csv_data = []
    csv_data.append(['Date', 'Discharge (mWh)', 'Battery (%)'])  # Add header to CSV data

    # Initialize previous capacity for discharge calculation
    previous_capacity_percent = None
    previous_time = None

    # Extract the data from each row
    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 4:
            continue  # Skip rows that don't have enough columns

        # Extract text content from the columns
        start_time = columns[0].text.strip()
        state = columns[1].text.strip()
        source = columns[2].text.strip()
        capacity_remaining = columns[3].text.strip()

        # Extract percentage from 'capacity_remaining' field
        parts = capacity_remaining.split()
        if len(parts) >= 2:
            # Convert capacity percentage to integer
            try:
                current_capacity_percent = int(parts[0])  # Get the percentage as an integer
            except ValueError:
                continue  # Skip invalid percentage values

            battery_percent = current_capacity_percent  # Use as Battery (%)

            # Calculate discharge in mWh based on capacity change
            if previous_capacity_percent is not None and previous_time is not None:
                # Calculate the discharge (mWh) assuming 1% capacity change per 100 mWh
                discharge_mwh = (previous_capacity_percent - current_capacity_percent) * 100  # Simplistic discharge calculation

                # Add to CSV data only if there is a decrease in battery percentage
                if discharge_mwh > 0:
                    # Add to CSV data
                    csv_data.append([previous_time, discharge_mwh, previous_capacity_percent])

            # Update previous values
            previous_capacity_percent = current_capacity_percent
            previous_time = start_time

        # Debug output
        print(f"Extracted Data: Start Time: {start_time}, State: {state}, Source: {source}, Capacity Remaining: {capacity_remaining}")

    # Print CSV data for debugging
    print(f"CSV Data: {csv_data}")

    # Write the data to CSV
    with open(csv_report_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"Battery data saved to CSV file path {csv_report_path}.")

# Generate the battery report
generate_battery_report()

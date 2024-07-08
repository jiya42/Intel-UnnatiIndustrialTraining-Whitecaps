# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    stress-ng \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Make the Python scripts executable
RUN chmod +x scripts/collect_memory_data.py scripts/analyze_memory_data.py

# Default command to run the collection script
CMD ["python", "scripts/collect_memory_data.py"]

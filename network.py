import psutil
import matplotlib.pyplot as plt

# Get all network interfaces and their statistics
network_interfaces = psutil.net_io_counters(pernic=True)

# Initialize lists to store data for plotting
interfaces = []
bytes_sent = []
bytes_recv = []


# Iterate over each interface
for interface, stats in network_interfaces.items():
    interfaces.append(interface)
    bytes_sent.append(stats.bytes_sent)
    bytes_recv.append(stats.bytes_recv)

# Plotting the data
plt.figure(figsize=(10, 6))
plt.bar(interfaces, bytes_sent, alpha=0.7, label='Bytes Sent')
plt.bar(interfaces, bytes_recv, alpha=0.7, label='Bytes Received')
plt.xlabel('Network Interfaces')
plt.ylabel('Bytes')
plt.title('Network Interface Statistics')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as an image file (PNG format)
plt.savefig('network_statistics.png')

# Display the plot
plt.show()


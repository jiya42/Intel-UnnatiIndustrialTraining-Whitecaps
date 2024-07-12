import psutil
import matplotlib.pyplot as plt

def get_network_statistics():
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

    return interfaces, bytes_sent, bytes_recv

def plot_network_statistics():
    interfaces, bytes_sent, bytes_recv = get_network_statistics()

    # Plotting the data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(interfaces, bytes_sent, alpha=0.7, label='Bytes Sent')
    ax.bar(interfaces, bytes_recv, alpha=0.7, label='Bytes Received')
    ax.set_xlabel('Network Interfaces')
    ax.set_ylabel('Bytes')
    ax.set_title('Network Interface Statistics')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    return fig

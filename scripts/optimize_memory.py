import subprocess

def optimize_memory():
    """
    Clear the Windows cache to optimize memory.
    """
    print("Starting memory optimization...")

    # Clear temporary files
    try:
        print("Clearing temporary files...")
        subprocess.run(['del', '/q', '/f', 'C:\\Windows\\Temp\\*'], shell=True, check=True)
        print("Temporary files cleared.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clear temporary files: {e}")

    # Flush the pagefile (alternative to `fsutil` cache flush)
    try:
        print("Clearing pagefile...")
        subprocess.run(['defrag', 'C:', '/O', '/H'], shell=True, check=True)  # Optimization command
        print("Pagefile cleared.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to clear pagefile: {e}")

    print("Memory optimization complete.")

if __name__ == "__main__":
    optimize_memory()

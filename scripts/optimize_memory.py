import subprocess
import os

def clear_temp_files():
    """
    Clear temporary files.
    """
    try:
        temp_path = os.environ.get('TEMP', '/tmp')
        result = subprocess.run(['cmd', '/c', 'del', '/q', '/f', f'{temp_path}\\*'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Temporary files cleared.")
        else:
            print(f"Error clearing temporary files: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting memory optimization...")
    clear_temp_files()
    print("Memory optimization complete.")

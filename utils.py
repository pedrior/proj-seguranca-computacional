import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(message):
    """Log a message to the console and log system."""
    logging.info(message)

def run_command(command):
    """Run a system command safely with error handling."""
    try:
        subprocess.run(command, check=True)
        log_message(f"Executed command: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        log_message(f"Error executing command: {str(e)}")

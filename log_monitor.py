import re
import time
import os
from config import LOG_FILE, SSH_FAIL_REGEX, MAX_ATTEMPTS, CHECK_INTERVAL
from ip_handler import block_ip, is_ip_banned, failed_attempts, unblock_ips
from utils import log_message, retry_on_failure

def monitor_logs():
    """Monitors the log file for failed SSH login attempts."""
    try:
        with open(LOG_FILE, "r") as log_file:
            log_file.seek(0, 2)  # Move to the end of the file
            file_inode = os.fstat(log_file.fileno()).st_ino  # Get inode

            while True:
                line = log_file.readline()
                if not line:
                    current_inode = os.fstat(log_file.fileno()).st_ino
                    if current_inode != file_inode:
                        # Log file rotated, reopen
                        log_message("Log file rotated. Reopening...")
                        log_file.close()
                        log_file = open(LOG_FILE, "r")
                        log_file.seek(0, 2)  # Move to the end of the new log
                        file_inode = current_inode

                    time.sleep(CHECK_INTERVAL)
                    unblock_ips()
                    continue

                # Search for failed SSH login attempts
                match = re.search(SSH_FAIL_REGEX, line)
                if match:
                    ip_address = match.group(1)
                    process_incident(ip_address)
    except FileNotFoundError:
        log_message(f"Log file {LOG_FILE} not found.")
    except Exception as e:
        log_message(f"Error monitoring logs: {str(e)}")

def process_incident(ip_address):
    """Processes a failed login attempt from a specific IP address."""
    if is_ip_banned(ip_address):
        log_message(f"IP {ip_address} is already banned.")
        return

    failed_attempts[ip_address] += 1
    log_message(f"Failed attempts for IP {ip_address}: {failed_attempts[ip_address]}")

    if failed_attempts[ip_address] >= MAX_ATTEMPTS:
        block_ip(ip_address)
        failed_attempts[ip_address] = 0

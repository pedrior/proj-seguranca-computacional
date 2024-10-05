import subprocess
import time
from collections import defaultdict
from config import BAN_TIME
from utils import log_message

failed_attempts = defaultdict(int)
banned_ips = {}

def is_ip_banned(ip_address):
    """Checks if an IP is currently banned in iptables or in-memory."""
    try:
        command = ["sudo", "iptables", "-L", "INPUT", "-v", "-n"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if ip_address in result.stdout:
            return True

        # Check if IP is banned in memory
        return ip_address in banned_ips and time.time() < banned_ips[ip_address] + BAN_TIME
    except subprocess.CalledProcessError as e:
        log_message(f"Error checking if IP {ip_address} is banned: {str(e)}")
        return False

def block_ip(ip_address):
    """Block an IP using iptables."""
    try:
        command = ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]
        subprocess.run(command, check=True)
        banned_ips[ip_address] = time.time()
        log_message(f"Blocked IP: {ip_address}")
    except subprocess.CalledProcessError as e:
        log_message(f"Error blocking IP {ip_address}: {str(e)}")

def unblock_ips():
    """Unblock IPs that have exceeded the ban time."""
    current_time = time.time()
    for ip, ban_time in list(banned_ips.items()):
        if current_time > ban_time + BAN_TIME:
            try:
                command = ["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"]
                subprocess.run(command, check=True)
                del banned_ips[ip]
                log_message(f"Unblocked IP: {ip}")
            except subprocess.CalledProcessError as e:
                log_message(f"Error unblocking IP {ip}: {str(e)}")

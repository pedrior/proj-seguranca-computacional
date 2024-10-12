import subprocess
import time
import json
from collections import defaultdict
from config import BAN_TIME, PERSISTENCE_FILE
from utils import log_message, validate_ip, send_email

failed_attempts = defaultdict(int)
banned_ips = {}

def load_state():
    """Load failed attempts and banned IPs from a JSON file."""
    global failed_attempts, banned_ips
    try:
        with open(PERSISTENCE_FILE, "r") as f:
            state = json.load(f)
            failed_attempts.update(state["failed_attempts"])
            banned_ips.update(state["banned_ips"])
    except FileNotFoundError:
        log_message("Persistence file not found, starting fresh.")
    except Exception as e:
        log_message(f"Error loading state: {str(e)}")

def save_state():
    """Save failed attempts and banned IPs to a JSON file."""
    try:
        state = {
            "failed_attempts": dict(failed_attempts),
            "banned_ips": banned_ips
        }
        with open(PERSISTENCE_FILE, "w") as f:
            json.dump(state, f)
    except Exception as e:
        log_message(f"Error saving state: {str(e)}")

def is_ip_banned(ip_address):
    """Checks if an IP is currently banned in iptables or in-memory."""
    if not validate_ip(ip_address):
        return False

    try:
        command = ["sudo", "iptables", "-L", "INPUT", "-v", "-n"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # If the IP is not found in the iptables output, remove it from the in-memory banned_ips
        if ip_address not in result.stdout:
            if ip_address in banned_ips:
                log_message(f"IP {ip_address} manually unblocked; removing from internal list.")
                
                del banned_ips[ip_address]

            return False

        # If IP is found in iptables or it's still within the ban time in memory
        return ip_address in banned_ips and time.time() < banned_ips[ip_address] + BAN_TIME
    except subprocess.CalledProcessError as e:
        log_message(f"Error checking if IP {ip_address} is banned: {str(e)}")
        return False

def block_ip(ip_address):
    """Block an IP using iptables and send an email notification."""
    if not validate_ip(ip_address):
        return

    try:
        command = ["sudo", "iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"]
        subprocess.run(command, check=True)
        banned_ips[ip_address] = time.time()

        log_message(f"Blocked IP: {ip_address}")

        # Send email notification
        subject = f"IP Blocked: {ip_address}"
        body = f"The IP address {ip_address} has been blocked due to too many failed login attempts."

        send_email(subject, body)
        
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

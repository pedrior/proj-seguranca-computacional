import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM_EMAIL, SMTP_TO_EMAIL
import logging
import ipaddress

# Configure logging
logging.basicConfig(filename='ssh_monitor.log', level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_message(message):
    """Log a message to the console and log system."""
    logging.info(message)

def send_email(subject, body):
    """Send an email using the SMTP configuration."""
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SMTP_FROM_EMAIL
        msg['To'] = SMTP_TO_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM_EMAIL, SMTP_TO_EMAIL, msg.as_string())

        log_message(f"Email sent to {SMTP_TO_EMAIL}: {subject}")
    except Exception as e:
        log_message(f"Failed to send email: {str(e)}")

def retry_on_failure(func, retries=3, delay=1):
    """Retries a function on failure."""
    import time
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            log_message(f"Error: {str(e)}. Retrying {attempt+1}/{retries}...")
            time.sleep(delay)
    log_message(f"Failed after {retries} attempts.")

def validate_ip(ip_address):
    """Validate an IP address."""
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        log_message(f"Invalid IP address: {ip_address}")
        return False

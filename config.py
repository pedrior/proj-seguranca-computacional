LOG_FILE = "/var/log/auth.log"
PERSISTENCE_FILE = "ip_state.json"
SSH_FAIL_REGEX = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"
MAX_ATTEMPTS = 5
BAN_TIME = 3600  # 1 hour
CHECK_INTERVAL = 0.1  # Sleep time between log file checks

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = ""
SMTP_PASSWORD = ""
SMTP_FROM_EMAIL = ""
SMTP_TO_EMAIL = ""
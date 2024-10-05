LOG_FILE = "/var/log/auth.log"
SSH_FAIL_REGEX = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"
MAX_ATTEMPTS = 5
BAN_TIME = 3600  # 1 hour
CHECK_INTERVAL = 0.1  # Sleep time between log file checks

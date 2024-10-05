from log_monitor import monitor_logs
from utils import log_message

if __name__ == "__main__":
    log_message("Starting SSH log monitor...")
    try:
        monitor_logs()
    except KeyboardInterrupt:
        log_message("SSH log monitor stopped by user.")

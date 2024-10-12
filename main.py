from log_monitor import monitor_logs
from ip_handler import load_state, save_state
from utils import log_message

if __name__ == "__main__":
    log_message("Starting SSH log monitor...")
    load_state()
    try:
        monitor_logs()
    except KeyboardInterrupt:
        log_message("SSH log monitor stopped by user.")
        save_state()

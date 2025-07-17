# 🔐 SecureLogger – Cloud-Linked Stealth Keylogger

SecureLogger is a stealth keylogging tool built for educational and ethical research purposes. It captures keystrokes in real-time, stores them locally and remotely (via Firebase), and runs silently with startup persistence. This tool is built for red-team simulation and educational use. Obfuscation is left intentionally moderate to keep the code readable and demonstrate transparency in logic. Advanced evasion can be layered if desired using native compilation (e.g., Nuitka) or custom loaders.

> ⚠️ **This project is for ethical, authorized use only**. Do not deploy this tool on any system without explicit consent.

---

## 🧠 Features

- ✅ Real-time keystroke capture using `pynput`
- ✅ GUI interface using `Tkinter` (optional visibility)
- ✅ Encrypted log saving (AES via `cryptography`)
- ✅ Remote log exfiltration to Firebase Realtime Database
- ✅ Local SQLite backup
- ✅ Stealth mode toggle
- ✅ Kill switch via `Ctrl+Shift+Q`
- ✅ Persistence via Windows registry (Startup)
- ✅ PyArmor-obfuscated binary to minimize AV detection

---

## 🚀 Setup

### 🔧 Requirements

- Python 3.8+
- Windows OS (tested on Windows 10/11)
- Internet access (for Firebase upload)

Install dependencies:

```bash
pip install pynput cryptography requests pyarmor pyinstaller python-dotenv

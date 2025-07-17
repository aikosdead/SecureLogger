import tkinter as tk
from tkinter import filedialog, messagebox
from crypto_utils import decrypt_log

def open_and_decrypt():
    file_path = filedialog.askopenfilename(title="Select Encrypted Log", filetypes=[("Encrypted Logs", "*.enc")])
    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted = decrypt_log(encrypted_data)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, decrypted)
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed:\n{e}")

# UI
root = tk.Tk()
root.title("Log Decryption Viewer")
root.geometry("600x400")

open_button = tk.Button(root, text="Open Encrypted Log", command=open_and_decrypt)
open_button.pack(pady=10)

text_area = tk.Text(root, wrap=tk.WORD)
text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

root.mainloop()

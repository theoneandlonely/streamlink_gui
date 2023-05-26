import tkinter as tk
import subprocess
import os
from datetime import datetime
import time

STREAMLINK_PATH = r"C:\Program Files\Streamlink\bin\streamlink.exe"
DOWNLOADS_FOLDER = r"D:\downloads\streams"
STREAMER_FILE = os.path.join(DOWNLOADS_FOLDER, "streamer.txt")

def start_streamlink():
    url = entry.get()
    streamer = url.replace("https://www.twitch.tv/", "")
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{timestamp}_{streamer}.ts"

    # Überprüfen, ob die Datei bereits existiert und Inkrementieren der Zahl am Ende
    counter = 1
    while os.path.exists(os.path.join(DOWNLOADS_FOLDER, filename)):
        base, ext = os.path.splitext(filename)
        parts = base.split("_")
        if parts[-1].isdigit():
            parts[-1] = str(int(parts[-1]) + 1)
        else:
            parts.append("1")
        base = "_".join(parts)
        filename = base + ext

    command = [STREAMLINK_PATH, "-o", filename, url, "best"]

    # Starte den Streamlink-Prozess im Hintergrund
    subprocess.Popen(command)

    # Warte 5 Sekunden und aktualisiere die Dateiliste
    window.after(5000, update_file_list)

def update_file_list():
    file_list = [
        file_name for file_name in os.listdir(DOWNLOADS_FOLDER)
        if file_name != "streamlink.py" and file_name != "streamer.txt"
    ]
    listbox_files.delete(0, tk.END)
    for file_name in file_list:
        listbox_files.insert(tk.END, file_name)

def update_streamer_list():
    if os.path.exists(STREAMER_FILE):
        with open(STREAMER_FILE, "r") as file:
            streamer_list = [streamer.strip() for streamer in file.readlines()]
            listbox_streamers.delete(0, tk.END)
            listbox_streamers.insert(tk.END, *streamer_list)

def on_window_close():
    window.destroy()

def on_listbox_streamers_select(event):
    selected_streamer = listbox_streamers.get(listbox_streamers.curselection())
    entry.delete(0, tk.END)
    entry.insert(tk.END, "https://www.twitch.tv/" + selected_streamer)

# GUI erstellen
window = tk.Tk()
window.title("Streamlink Downloader")
window.protocol("WM_DELETE_WINDOW", on_window_close)

# Eingabefeld
entry = tk.Entry(window, width=40)
entry.pack()

# Button "Go"
button = tk.Button(window, text="Go", command=start_streamlink)
button.pack()

# Liste für Dateien
listbox_files = tk.Listbox(window, width=40, height=10)
listbox_files.pack()

# Aktualisiere Dateiliste beim Programmstart
update_file_list()

# Liste für Streamer
listbox_streamers = tk.Listbox(window, width=40, height=10)
listbox_streamers.pack()

# Aktualisiere Streamer-Liste beim Programmstart
update_streamer_list()

# Bei Auswahl eines Elements in der Streamer-Liste
listbox_streamers.bind("<<ListboxSelect>>", on_listbox_streamers_select)

window.mainloop()

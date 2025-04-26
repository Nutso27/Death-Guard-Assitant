
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import time
import pygame
import requests
import os
import customtkinter as ctk
import tempfile
import subprocess
import sys

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return filename

LORE_URL = "https://raw.githubusercontent.com/Nutso27/Death-Guard-Assitant/refs/heads/main/warhammer_lore.txt"
VERSION_URL = "https://raw.githubusercontent.com/Nutso27/Death-Guard-Assitant/refs/heads/main/version.json"
LOCAL_LORE = "warhammer_lore.txt"
LOCAL_VERSION = "1.2"

def sync_lore():
    try:
        remote = requests.get(LORE_URL)
        if remote.status_code == 200:
            new_lore = remote.text
            if not os.path.exists(LOCAL_LORE) or open(LOCAL_LORE, "r", encoding="utf-8").read() != new_lore:
                with open(LOCAL_LORE, "w", encoding="utf-8") as f:
                    f.write(new_lore)
                return True
    except Exception as e:
        print(f"Lore sync failed: {e}")
    return False

def auto_update():
    try:
        response = requests.get(VERSION_URL)
        if response.status_code == 200:
            version_data = response.json()
            if version_data["version"] != LOCAL_VERSION:
                installer_url = version_data["installer"]
                temp_path = os.path.join(tempfile.gettempdir(), "DeathGuard_Assistant_Installer.exe")
                installer = requests.get(installer_url)
                with open(temp_path, "wb") as f:
                    f.write(installer.content)
                subprocess.Popen([temp_path], shell=True)
                return True
    except Exception as e:
        print(f"Auto-update failed: {e}")
    return False

def play_vox_sound():
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path("vox_startup.wav"))
    pygame.mixer.music.play()

def boot_sequence(root, text_label, on_complete):
    updated = sync_lore()
    update_launched = auto_update()
    if update_launched:
        root.destroy()
        return

    messages = [
        ">> Initializing...",
        ">> Error: System integrity compromised.",
        ">> ███ Cogitator corrupted...",
        ">> ███ Daemonic infection detected...",
        ">> Nurgle protocol override active...",
        ">> Lore status: " + ("UPDATED" if updated else "UNCHANGED"),
        ">> WELCOME, INQUISITOR."
    ]
    delay = 1.5
    for msg in messages:
        text_label.config(text=msg)
        time.sleep(delay)
    root.after(500, on_complete)

def show_main_gui():
    try:
        subprocess.Popen([sys.executable, "lore_gui_ollama.py"])
    except Exception as e:
        print(f"Failed to launch main GUI: {e}")
    splash_root.destroy()

splash_root = tk.Tk()
splash_root.overrideredirect(True)

screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
splash_root.geometry(f"{screen_width}x{screen_height}+0+0")
splash_root.overrideredirect(True)

splash_root.configure(bg="black")

gif = Image.open(resource_path("glitch_splash.gif"))
frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
splash_label = tk.Label(splash_root, bg="black")
splash_label.pack(fill="both", expand=True)

text_overlay = tk.Label(splash_root, text="", fg="lime", bg="black", font=("Courier", 14))
text_overlay.place(relx=0.5, rely=0.85, anchor="center")

frame_index = 0
def animate():
    global frame_index
    frame = frames[frame_index]
    frame_index = (frame_index + 1) % len(frames)
    splash_label.configure(image=frame)
    splash_root.after(50, animate)

animate()
threading.Thread(target=play_vox_sound).start()
threading.Thread(target=boot_sequence, args=(splash_root, text_overlay, show_main_gui)).start()
splash_root.mainloop()

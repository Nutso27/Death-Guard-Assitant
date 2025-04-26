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
LOCAL_LORE = "lore/warhammer_lore.txt"  # updated path

def sync_lore():
    try:
        remote = requests.get(LORE_URL)
        if remote.status_code == 200:
            new_lore = remote.text
            os.makedirs(os.path.dirname(LOCAL_LORE), exist_ok=True)
            if not os.path.exists(LOCAL_LORE) or open(LOCAL_LORE, "r", encoding="utf-8").read() != new_lore:
                with open(LOCAL_LORE, "w", encoding="utf-8") as f:
                    f.write(new_lore)
                return True
    except Exception as e:
        print(f"Lore sync failed: {e}")
    return False

def play_vox_sound():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(resource_path("assets/vox_startup.wav"))
        pygame.mixer.music.play()
    except Exception as e:
        print(f"Sound error: {e}")

def boot_sequence(root, text_label, on_complete):
    updated = sync_lore()

    # Auto-update check DISABLED for stable release
    update_launched = False

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
        subprocess.Popen([sys.executable, os.path.join("src", "lore_gui_ollama.py")])
    except Exception as e:
        print(f"Failed to launch main GUI: {e}")
    splash_root.destroy()

# Create splash window
splash_root = tk.Tk()
splash_root.overrideredirect(True)
splash_root.attributes('-fullscreen', True)
splash_root.configure(bg="black")

# Load and animate GIF
try:
    gif = Image.open(resource_path("assets/glitch_splash.gif"))
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
except Exception as e:
    print(f"Error loading splash image: {e}")
    frames = []

splash_label = tk.Label(splash_root, bg="black")
splash_label.pack(fill="both", expand=True)

text_overlay = tk.Label(splash_root, text="", fg="lime", bg="black", font=("Courier", 18))
text_overlay.place(relx=0.5, rely=0.85, anchor="center")

frame_index = 0
def animate():
    global frame_index
    if frames:
        frame = frames[frame_index]
        frame_index = (frame_index + 1) % len(frames)
        splash_label.configure(image=frame)
    splash_root.after(50, animate)

animate()

# Start background threads
threading.Thread(target=play_vox_sound).start()
threading.Thread(target=boot_sequence, args=(splash_root, text_overlay, show_main_gui)).start()

splash_root.mainloop()

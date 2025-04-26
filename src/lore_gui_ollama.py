
import customtkinter as ctk

class NurgleCogitator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nurgle Cogitator - Inquisitorial Interface")
        self.geometry("720x480")
        self.iconbitmap("death_guard.ico")
        self.configure(bg='#1c1c1c')

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        label = ctk.CTkLabel(frame, text="Inquisitor Interface Ready", font=ctk.CTkFont(size=24, weight="bold"))
        label.pack(padx=20, pady=20)

        button = ctk.CTkButton(frame, text="View Synced Lore", command=self.show_lore)
        button.pack(pady=10)

    def show_lore(self):
        try:
            with open("warhammer_lore.txt", "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            content = "Lore file not found."
        
        lore_window = ctk.CTkToplevel(self)
        lore_window.title("Synced Lore")
        lore_window.geometry("600x400")
        text_box = ctk.CTkTextbox(lore_window, wrap="word")
        text_box.pack(expand=True, fill="both", padx=10, pady=10)
        text_box.insert("1.0", content)
        text_box.configure(state="disabled")

def launch():
    app = NurgleCogitator()
    app.mainloop()

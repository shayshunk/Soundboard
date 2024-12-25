import tkinter as tk
import customtkinter as ctk
from pygame import mixer

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

mixer.init()
mixer.set_num_channels(4)
bats = mixer.Channel(2)


def AddButton(window):
    if bats.get_busy():
        bats.stop()
    else:
        sound = mixer.Sound("bats.mp3")
        bats.play(sound)


# Creating window
window = ctk.CTk()

window.geometry("800x800")
window.title("Soundboard")

label = ctk.CTkLabel(master=window, text="Soundboard")
label.pack(pady=20)

button = ctk.CTkButton(master=window, text="Play Sound",
                       command=lambda: AddButton(window))
button.pack()

# Running
window.mainloop()

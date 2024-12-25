import tkinter as tk
import customtkinter as ctk
from pygame import mixer

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

mixer.init()
mixer.set_num_channels(8)


def AddSound():
    soundFile = tk.filedialog.askopenfilename()
    newChannel = mixer.find_channel(force=True)
    print(soundFile)
    sound = mixer.Sound(soundFile)
    newChannel.play(sound)


def AddButton(app):
    # Creating new button for sound
    newButton = ctk.CTkButton(master=app, text="", command=AddSound())
    newButton.configure(width=10, height=50)
    newButton.grid(row=1, column=0, padx=20, pady=20)

    # Adding entry box to get name for sound
    dialog = ctk.CTkInputDialog(
        text="Enter sound name:", title="Name your buton!")
    buttonName = dialog.get_input()
    newButton.configure(text=buttonName)


# Creating app
app = ctk.CTk()

app.geometry("800x800")
app.title("Soundboard")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

label = ctk.CTkLabel(master=app, text="Soundboard")
label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

button = ctk.CTkButton(master=app, text="Play Sound",
                       command=lambda: AddButton(app))
button.grid(row=0, column=1, padx=20, pady=20, sticky='ew')


# Running
app.mainloop()

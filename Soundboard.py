import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from math import floor

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

mixer.init()
totalChannels = 8
mixer.set_num_channels(totalChannels)

columns = 2


def PlaySound(buttonId):
    soundFile = soundDictionary[buttonId]
    sound = mixer.Sound(soundFile)
    newChannel = mixer.find_channel(force=True)
    newChannel.play(sound)


def AddSound(buttonId):
    # Asking user to associate file with button
    soundFile = tk.filedialog.askopenfilename()

    # Associating sound with dictionary
    soundDictionary[buttonId] = soundFile
    buttons[buttonId].configure(command=lambda: PlaySound(buttonId))


def AddButton(app):
    # Assigning new button to dictionary
    buttonId = str(len(buttons) + 1)

    # Figuring out where to place new button
    totalButtons = len(buttons)
    columnSpot = totalButtons % columns
    rowSpot = floor(totalButtons / 2) + 1

    # Creating new button for sound
    buttons[buttonId] = ctk.CTkButton(master=app, text="")
    buttons[buttonId].configure(command=AddSound(buttonId))
    buttons[buttonId].configure(width=150, height=100)
    buttons[buttonId].grid(row=rowSpot, column=columnSpot,
                           padx=20, pady=20, sticky="ew")

    # Adding entry box to get name for sound
    dialog = ctk.CTkInputDialog(
        text="Enter sound name:", title="Name your buton!")
    buttonName = dialog.get_input()
    buttons[buttonId].configure(text=buttonName)

    # Changing what clicking the button does
    buttons[buttonId].configure(command=lambda: PlaySound(buttonId))


# Creating app
app = ctk.CTk()

app.geometry("800x800")
app.title("Soundboard")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

buttons = {}
soundDictionary = {}

label = ctk.CTkLabel(master=app, text="Soundboard")
label.grid(row=0, column=0, padx=20, pady=20, sticky='ew')

button = ctk.CTkButton(master=app, text="Add Sound",
                       command=lambda: AddButton(app))
button.grid(row=0, column=1, padx=20, pady=20, sticky='ew')


# Running
app.mainloop()

import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from math import floor
import pywinstyles

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

mixer.init()
totalChannels = 8
mixer.set_num_channels(totalChannels)

columns = 4
span = columns - 1

buttons = {}
soundDictionary = {}
channelDictionary = {}
checkboxDictionary = {}


class Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.titleFont = ctk.CTkFont(family='Agency FB', size=32)
        self.defaultFont = ctk.CTkFont(family='Agency FB', size=24)
        self.checkboxFont = ctk.CTkFont(family='Agency FB', size=18)

        for i in range(columns):
            self.grid_columnconfigure(i, weight=1)

        # Hiding scrollbar
        yScrollbar = self._scrollbar
        yScrollbar.grid_forget()

        # Adding widgets onto frame
        # App title
        self.titleLabel = ctk.CTkLabel(
            master=self, text="Soundboard", font=self.titleFont)
        self.titleLabel.grid(row=0, column=0, columnspan=span,
                             padx=20, pady=20, sticky='WENS')

        # Add sound button
        self.button = ctk.CTkButton(
            master=self, text="Add Sound", command=lambda: self.AddButton(), font=self.defaultFont)
        self.button.grid(row=0, column=span, padx=20, pady=20, sticky='WENS')

        # Volume text
        self.volumeLabel = ctk.CTkLabel(
            master=self, text="Master Volume", font=self.defaultFont)
        self.volumeLabel.grid(row=1, column=0, padx=20, pady=20, sticky='WENS')

        # Volume slider
        self.volume = ctk.CTkSlider(
            master=self, from_=0, to=1.0, command=self.ChangeVolume)
        self.volume.set(1.0)
        self.volume.grid(row=1, column=1, columnspan=span,
                         padx=20, pady=20, sticky="EWNS")

    def AddButton(self):
        # Assigning new button to dictionary
        buttonId = str(len(buttons) + 1)

        # Figuring out where to place new button
        totalButtons = len(buttons)
        columnSpot = totalButtons % columns
        rowSpot = 2 * floor(totalButtons / columns) + 2

        # Creating new button for sound
        buttons[buttonId] = ctk.CTkButton(
            master=self, text="", font=self.defaultFont)
        buttons[buttonId].configure(command=self.AddSound(buttonId))
        buttons[buttonId].configure(width=150, height=100)
        buttons[buttonId].grid(row=rowSpot, column=columnSpot,
                               padx=20, pady=15, sticky="ew")

        checkboxVar = ctk.BooleanVar()
        checkboxDictionary[buttonId] = ctk.CTkCheckBox(
            master=self, text="Loop?", font=self.checkboxFont, variable=checkboxVar, command=lambda: self.CheckboxChecked(buttonId, checkboxVar))
        checkboxDictionary[buttonId].grid(row=rowSpot+1, column=columnSpot,
                                          padx=20, pady=0, sticky='w')

        # Adding entry box to get name for sound
        dialog = ctk.CTkInputDialog(
            text="Enter sound name:", title="Name your buton!")
        buttonName = dialog.get_input()

        if buttonName is None or buttonName == "":
            buttonName = "Unnamed"

        buttons[buttonId].configure(text=buttonName)

        # Changing what clicking the button does
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))

    def AddSound(self, buttonId):
        # Asking user to associate file with button
        soundFile = tk.filedialog.askopenfilename()

        # Associating sound with dictionary
        soundDictionary[buttonId] = soundFile
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))

    def PlaySound(self, buttonId):
        # Checking if that sound is already playing
        if buttonId in channelDictionary:
            if channelDictionary[buttonId].get_busy():
                channelDictionary[buttonId].stop()

        # Grabbing sound file
        soundFile = soundDictionary[buttonId]
        sound = mixer.Sound(soundFile)

        # Grabbing empty sound channel
        newChannel = mixer.find_channel(force=True)
        channelDictionary[buttonId] = newChannel
        print(newChannel)

        # Checking if loop is on
        if checkboxDictionary[buttonId].get():
            newChannel.play(sound, loops=-1)
        else:
            newChannel.play(sound)

    def CheckboxChecked(self, buttonId, checkboxVar):
        # Checking if unchecked or checked
        if not checkboxVar.get():
            if channelDictionary[buttonId].get_busy():
                channelDictionary[buttonId].stop()

    def ChangeVolume(self, value):
        for id in range(totalChannels):
            mixer.Channel(id).set_volume(value)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("Soundboard")

        # get the default colors of frame
        frame_fg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]

        mainFrame = Frame(master=self, width=600, height=600,
                          corner_radius=0, fg_color="transparent")
        self.my_frame = mainFrame
        self.my_frame.grid(row=0, column=0, sticky="nsew")


# Creating app
app = App()

# Running
app.mainloop()

import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from pygame import time
from math import floor
from CTkToolTip import *
import pandas as pd
from CTkMenuBar import *
import pprint
import csv

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

mixer.init()
totalChannels = 8
mixer.set_num_channels(totalChannels)

columns = 6
span = columns - 2

buttons = {}
buttonNameDictionary = {}
soundDictionary = {}
soundFileDictionary = {}
channelDictionary = {}
checkboxDictionary = {}
sliderDictionary = {}
tooltipDictionary = {}

soundboardData = pd.DataFrame()


class Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.titleFont = ctk.CTkFont(family='Agency FB', size=32)
        self.defaultFont = ctk.CTkFont(family='Agency FB', size=24)
        self.checkboxFont = ctk.CTkFont(family='Agency FB', size=18)

        for i in range(columns):
            self.grid_columnconfigure(i, weight=1, uniform="group")

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
        self.button.grid(row=0, column=span, columnspan=2,
                         padx=20, pady=20, sticky='WENS')

        # Volume text
        self.volumeLabel = ctk.CTkLabel(
            master=self, text="Master Volume", font=self.defaultFont)
        self.volumeLabel.grid(row=1, column=0, columnspan=2,
                              padx=20, pady=20, sticky='WENS')

        # Volume slider
        self.volume = ctk.CTkSlider(
            master=self, from_=0, to=1.0, command=self.ChangeVolume)
        self.volume.set(1.0)
        self.volume.grid(row=1, column=2, columnspan=span,
                         padx=20, pady=20, sticky="EWNS")

        # Tool tip
        self.sliderTooltip = CTkToolTip(self.volume, message="Volume: 100")

    def AddButton(self, soundFile=None, buttonName=None):

        # Asking user to associate file with button
        if soundFile is None:
            soundFile = tk.filedialog.askopenfilename()
            if soundFile is None or soundFile is '':
                return

        if buttonName is None:
            # Adding entry box to get name for sound
            dialog = ctk.CTkInputDialog(
                text="Enter sound name:", title="Name your buton!")
            buttonName = dialog.get_input()

        if buttonName == "":
            buttonName = "Unnamed"

        # Assigning new button to dictionary
        buttonId = str(len(buttons) + 1)

        # Associating sound with dictionary
        soundFileDictionary[buttonId] = soundFile

        # Figuring out where to place new button
        totalButtons = len(buttons)
        columnSpot = ((2 * totalButtons) % columns)
        rowSpot = 2 * floor(totalButtons * 2 / columns) + 2

        paddingx = (10, 10)

        if columnSpot == 0:
            paddingx = (20, 10)
        elif columnSpot == columns - 2:
            paddingx = (10, 20)

        # Creating new button for sound
        buttons[buttonId] = ctk.CTkButton(
            master=self, text="", font=self.defaultFont)
        buttons[buttonId].configure(width=150, height=100)
        buttons[buttonId].grid(row=rowSpot, column=columnSpot, columnspan=2,
                               padx=paddingx, pady=15, sticky="ewns")

        # checkboxVar = ctk.BooleanVar()
        checkboxDictionary[buttonId] = ctk.CTkCheckBox(
            master=self, text="Loop?", font=self.checkboxFont, command=lambda: self.CheckboxChecked(buttonId))
        checkboxDictionary[buttonId].grid(row=rowSpot+1, column=columnSpot,
                                          padx=(20, 0), pady=0)

        sliderDictionary[buttonId] = ctk.CTkSlider(
            master=self, from_=0, to=1.0)
        sliderDictionary[buttonId].set(1.0)
        sliderDictionary[buttonId].configure(
            command=lambda value: self.ChangeChannelVolume(buttonId, value))
        sliderDictionary[buttonId].grid(
            row=rowSpot+1, column=columnSpot+1, padx=(0, 20), pady=0, sticky='ew')
        tooltipDictionary[buttonId] = CTkToolTip(
            sliderDictionary[buttonId], message="Volume: 100")

        buttons[buttonId].configure(text=buttonName)

        # Changing what clicking the button does
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))

        # Grabbing names for dictionary
        buttonNameDictionary[buttonId] = buttons[buttonId].cget("text")
        pprint.pprint(buttonNameDictionary)
        pprint.pprint(soundFileDictionary)

        # Writing to file
        with open("Data.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            for key, value in soundFileDictionary.items():
                writer.writerow([value])
            for key, value in buttonNameDictionary.items():
                writer.writerow([value])

    def PlaySound(self, buttonId):
        # Checking if that sound is already playing
        if buttonId in channelDictionary:
            if channelDictionary[buttonId].get_busy():
                channelDictionary[buttonId].stop()
                del channelDictionary[buttonId]

        # Grabbing sound file
        soundFile = soundFileDictionary[buttonId]
        soundDictionary[buttonId] = mixer.Sound(soundFile)

        # Grabbing empty sound channel
        newChannel = mixer.find_channel(force=True)
        channelDictionary[buttonId] = newChannel

        # Checking if loop is on
        if checkboxDictionary[buttonId].get():
            newChannel.play(soundDictionary[buttonId], loops=-1)
        else:
            newChannel.play(soundDictionary[buttonId])

    def CheckboxChecked(self, buttonId):
        # Checking if unchecked or checked
        if not checkboxDictionary[buttonId].get():
            if channelDictionary[buttonId].get_busy():
                channelDictionary[buttonId].stop()

    def ChangeVolume(self, value):
        self.sliderTooltip.configure(
            message="Volume: " + str(int(value * 100)))
        for id in range(totalChannels):
            mixer.Channel(id).set_volume(value)

    def ChangeChannelVolume(self, buttonId, value):
        if buttonId in tooltipDictionary:
            tooltipDictionary[buttonId].configure(
                message="Volume: " + str(int(value * 100)))

        if buttonId in soundDictionary:
            soundDictionary[buttonId].set_volume(value)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("Soundboard")

        mainFrame = Frame(master=self, width=600, height=600,
                          corner_radius=0, fg_color="transparent")
        self.my_frame = mainFrame
        self.my_frame.grid(row=0, column=0, sticky="nsew")


# Creating app
app = App()

# Running
app.mainloop()

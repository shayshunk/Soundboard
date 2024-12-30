import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from pygame import time
from math import floor
from CTkToolTip import *
import pprint
import csv
import pandas as pd
from PIL import Image
import os.path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

mixer.init()
totalChannels = 8
mixer.set_num_channels(totalChannels)

columns = 9
span = columns - 3

buttons = {}
buttonNameDict = {}
soundDict = {}
soundFileDict = {}
channelDict = {}
loopDict = {}
sliderDict = {}
tooltipDict = {}
deleteDict = {}

loopColor = "#383838"


class Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.titleFont = ctk.CTkFont(family='Agency FB', size=32)
        self.defaultFont = ctk.CTkFont(family='Agency FB', size=24)
        self.checkboxFont = ctk.CTkFont(family='Agency FB', size=18)

        for i in range(columns):
            if i % 3 == 2:
                self.grid_columnconfigure(i, weight=3, uniform="group1")
            else:
                self.grid_columnconfigure(i, weight=0, uniform="group2")
        # Hiding scrollbar
        yScrollbar = self._scrollbar
        yScrollbar.grid_forget()

        # Grabbing loop image
        filepath = "icons8-loop-100.png"
        self.loopImage = ctk.CTkImage(light_image=Image.open(
            filepath), dark_image=Image.open(filepath), size=(25, 25))

        # Grabbing delete image
        filepath = "icons8-delete-90.png"
        self.deleteImage = ctk.CTkImage(light_image=Image.open(
            filepath), dark_image=Image.open(filepath), size=(25, 25))

        # Adding widgets onto frame
        # App title
        self.titleLabel = ctk.CTkLabel(
            master=self, text="Soundboard", font=self.titleFont)
        self.titleLabel.grid(row=0, column=0, columnspan=span,
                             padx=20, pady=20, sticky='WENS')

        # Add sound button
        self.button = ctk.CTkButton(
            master=self, text="Add Sound", command=lambda: self.AddButton(), font=self.defaultFont)
        self.button.grid(row=0, column=span, columnspan=3,
                         padx=20, pady=20, sticky='WENS')

        # Volume text
        self.volumeLabel = ctk.CTkLabel(
            master=self, text="Master Volume", font=self.defaultFont)
        self.volumeLabel.grid(row=1, column=0, columnspan=3,
                              padx=20, pady=20, sticky='WENS')

        # Volume slider
        self.volume = ctk.CTkSlider(
            master=self, from_=0, to=1.0, command=self.ChangeVolume)
        self.volume.set(1.0)
        self.volume.grid(row=1, column=3, columnspan=span,
                         padx=20, pady=20, sticky="EWNS")
        self.volume.bind("<ButtonRelease-1>",
                         lambda event: self.VolumeSave(event))

        # Tool tip
        self.sliderTooltip = CTkToolTip(self.volume, message="Volume: 100")

        self.LoadData()

    def VolumeSave(self, event):
        self.WriteToFile()

    def LoadData(self):
        # Check if csv exists
        if not os.path.isfile("Data.csv"):
            return

        # Checking if csv is empty
        try:
            dataframe = pd.read_csv("Data.csv", header=None)
        except pd.errors.EmptyDataError:
            return

        print(dataframe.head())

        soundFileDict = dataframe.loc[0].to_dict()
        buttonNameDict = dataframe.loc[1].to_dict()
        loopValues = dataframe.loc[2].to_dict()
        sliderValues = dataframe.loc[3].to_dict()
        volumeValue = float(dataframe.loc[4][0])

        self.volume.set(volumeValue)

        for i in range(len(buttonNameDict)):
            self.AddButton(
                soundFileDict[i], buttonNameDict[i], loopValues[i], sliderValues[i])

    def AddButton(self, soundFile=None, buttonName=None, loopValue=None, sliderValue=None):
        # Asking user to associate file with button
        if soundFile is None:
            soundFile = tk.filedialog.askopenfilename()
            if soundFile is None or soundFile == '':
                return

        if buttonName is None:
            # Adding entry box to get name for sound
            dialog = ctk.CTkInputDialog(
                text="Enter sound name:", title="Name your buton!")
            buttonName = dialog.get_input()

        if buttonName == "":
            buttonName = "Unnamed"

        # Assigning new button to Dict
        buttonId = len(buttons)

        # Associating sound with Dict
        soundFileDict[buttonId] = soundFile
        soundDict[buttonId] = mixer.Sound(soundFile)

        # Figuring out where to place new button
        totalButtons = buttonId
        columnSpot = ((3 * totalButtons) % columns)
        rowSpot = 2 * floor(totalButtons * 3 / columns) + 2

        paddingx = (10, 10)

        if columnSpot == 0:
            paddingx = (20, 10)
        elif columnSpot == columns - 3:
            paddingx = (10, 20)

        # Creating new button for sound
        buttons[buttonId] = ctk.CTkButton(
            master=self, text="", font=self.defaultFont)
        buttons[buttonId].configure(width=150, height=100)
        buttons[buttonId].grid(row=rowSpot, column=columnSpot, columnspan=3,
                               padx=paddingx, pady=15, sticky="ewns")

        if loopValue == '1':
            fgColor = loopColor
        else:
            fgColor = "transparent"

        loopDict[buttonId] = ctk.CTkButton(
            master=self, text="", image=self.loopImage, fg_color=fgColor, hover_color="#3c3c3c", command=lambda: self.LoopChecked(buttonId))
        loopDict[buttonId].configure(width=50, height=50)
        loopDict[buttonId].grid(row=rowSpot+1, column=columnSpot,
                                padx=(5, 0), pady=0)

        deleteDict[buttonId] = ctk.CTkButton(
            master=self, text="", image=self.deleteImage, fg_color="transparent", hover_color="#3c3c3c", command=lambda: self.DeleteSound(buttonId))
        deleteDict[buttonId].configure(width=50, height=50)
        deleteDict[buttonId].grid(
            row=rowSpot+1, column=columnSpot+1, padx=(5, 0), pady=0)

        if sliderValue is None:
            volume = 1.0
        else:
            volume = float(sliderValue)

        sliderDict[buttonId] = ctk.CTkSlider(
            master=self, from_=0, to=1.0)
        sliderDict[buttonId].set(volume)
        sliderDict[buttonId].configure(
            command=lambda value: self.ChangeChannelVolume(buttonId, value))
        sliderDict[buttonId].bind("<ButtonRelease-1>",
                                  lambda event: self.VolumeSave(event))
        sliderDict[buttonId].grid(
            row=rowSpot+1, column=columnSpot+2, padx=(0, 20), pady=0, sticky='ew')
        tooltipDict[buttonId] = CTkToolTip(
            sliderDict[buttonId], message="Volume: 100")

        buttons[buttonId].configure(text=buttonName)

        # Changing what clicking the button does
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))

        # Grabbing names for Dict
        buttonNameDict[buttonId] = buttons[buttonId].cget("text")

        # Writing to file
        self.WriteToFile()

    def PlaySound(self, buttonId):
        # Checking if that sound is already playing
        if buttonId in channelDict:
            if channelDict[buttonId].get_busy():
                channelDict[buttonId].stop()
                del channelDict[buttonId]

        # Grabbing empty sound channel
        newChannel = mixer.find_channel(force=True)
        channelDict[buttonId] = newChannel

        # Checking if loop is on
        if loopDict[buttonId].cget("fg_color") == loopColor:
            channelDict[buttonId].play(
                soundDict[buttonId], loops=-1)
        else:
            channelDict[buttonId].play(soundDict[buttonId])

    def LoopChecked(self, buttonId):
        # Checking if unchecked or checked
        if loopDict[buttonId].cget("fg_color") == "transparent":
            loopDict[buttonId].configure(fg_color=loopColor)
        else:
            loopDict[buttonId].configure(fg_color="transparent")
            if buttonId in channelDict:
                if channelDict[buttonId].get_busy():
                    channelDict[buttonId].stop()

        self.WriteToFile()

    def ChangeVolume(self, value):
        self.sliderTooltip.configure(
            message="Volume: " + str(int(value * 100)))
        for id in range(totalChannels):
            mixer.Channel(id).set_volume(value)

    def ChangeChannelVolume(self, buttonId, value):
        if buttonId in tooltipDict:
            tooltipDict[buttonId].configure(
                message="Volume: " + str(int(value * 100)))

        if buttonId in soundDict:
            soundDict[buttonId].set_volume(value)

    def DeleteSound(self, buttonId):
        # Check if sound playing first
        if buttonId in channelDict:
            if channelDict[buttonId].get_busy():
                channelDict[buttonId].stop()

        # Destroying and then updating dictionaries
        buttons[buttonId].destroy()
        del buttons[buttonId]

        deleteDict[buttonId].destroy()
        del deleteDict[buttonId]

        sliderDict[buttonId].destroy()
        del sliderDict[buttonId]

        loopDict[buttonId].destroy()
        del loopDict[buttonId]

        del soundDict[buttonId]
        del soundFileDict[buttonId]
        if buttonId in channelDict:
            del channelDict[buttonId]
        del buttonNameDict[buttonId]
        del tooltipDict[buttonId]

        # Saving
        self.WriteToFile()

        # Clearing
        for i in buttons:
            buttons[i].destroy()
            loopDict[i].destroy()
            sliderDict[i].destroy()
            deleteDict[i].destroy()

        buttons.clear()
        loopDict.clear()
        soundDict.clear()
        soundFileDict.clear()
        buttonNameDict.clear()
        tooltipDict.clear()
        sliderDict.clear()
        deleteDict.clear()
        channelDict.clear()

        self.LoadData()

    def WriteToFile(self):
        # Writing to file
        with open("Data.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(soundFileDict.values())
            writer.writerow(buttonNameDict.values())

            loopValues = []
            sliderValues = []
            for i in loopDict:
                if loopDict[i].cget("fg_color") == loopColor:
                    loopValues.append(1)
                else:
                    loopValues.append(0)

                sliderValues.append(sliderDict[i].get())

            writer.writerow(loopValues)
            writer.writerow(sliderValues)

            volume = []
            volume.append(self.volume.get())
            writer.writerow(volume)


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

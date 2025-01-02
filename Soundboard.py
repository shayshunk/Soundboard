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
import pdb

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

mixer.init()
totalChannels = 8
mixer.set_num_channels(totalChannels)

columns = 9
span = columns - 3

buttons = []
buttonNameList = []
soundList = []
soundFileList = []
channelDict = {}
loopList = []
sliderList = []
tooltipList = []
deleteList = []

loopColor = "#383838"


class Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.titleFont = ctk.CTkFont(family='Agency FB', size=32)
        self.defaultFont = ctk.CTkFont(family='Agency FB', size=24)
        self.checkboxFont = ctk.CTkFont(family='Agency FB', size=18)

        for i in range(columns):
            if i % 3 == 1:
                self.grid_columnconfigure(
                    i, weight=3, uniform="group1")
            else:
                self.grid_columnconfigure(
                    i, weight=0, uniform="group2")
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

        if (len(dataframe) != 5):
            return

        soundFileList = dataframe.loc[0].to_dict()
        buttonNameList = dataframe.loc[1].to_dict()
        loopValues = dataframe.loc[2].to_dict()
        sliderValues = dataframe.loc[3].to_dict()
        volumeValue = float(dataframe.loc[4][0])

        self.volume.set(volumeValue)

        for i in range(len(buttonNameList)):
            self.AddButton(
                soundFileList[i], buttonNameList[i], loopValues[i], sliderValues[i])

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

        # Assigning new button to List
        buttonId = len(buttons)

        # Associating sound with List
        soundFileList.append(soundFile)
        soundList.append(mixer.Sound(soundFile))

        # Figuring out where to place new button
        totalButtons = buttonId
        columnSpot = ((3 * totalButtons) % columns)
        rowSpot = 2 * floor(totalButtons * 3 / columns) + 2

        paddingx = (10, 10)

        # Creating new button for sound
        buttons.append(ctk.CTkButton(
            master=self, text="", font=self.defaultFont, anchor="center"))
        buttons[buttonId].configure(width=250, height=100)
        buttons[buttonId].grid(
            row=rowSpot, column=columnSpot, columnspan=3, padx=paddingx, pady=15)
        # Adding name to button
        buttons[buttonId].configure(text=buttonName)

        # Setting up button toggle for looping
        if loopValue == '1':
            fgColor = loopColor
        else:
            fgColor = "transparent"

        # Adding loop button
        loopList.append(ctk.CTkButton(
            master=self, text="", image=self.loopImage, fg_color=fgColor, hover_color="#3c3c3c", command=lambda: self.LoopChecked(buttonId)))
        loopList[buttonId].configure(width=50, height=50)
        loopList[buttonId].grid(row=rowSpot+1, column=columnSpot,
                                padx=(5, 0), pady=0)

        # Adding delete button
        deleteList.append(ctk.CTkButton(
            master=self, text="", image=self.deleteImage, fg_color="transparent", hover_color="#3c3c3c", command=lambda: self.DeleteSound(buttonId)))
        deleteList[buttonId].configure(width=50, height=50)
        deleteList[buttonId].grid(
            row=rowSpot+1, column=columnSpot+2, padx=(5, 0), pady=0)

        # Loading volume
        if sliderValue is None:
            volume = 1.0
        else:
            volume = float(sliderValue)

        # Adding volume slider
        sliderList.append(ctk.CTkSlider(
            master=self, from_=0, to=1.0))
        sliderList[buttonId].set(volume)
        sliderList[buttonId].configure(
            command=lambda value: self.ChangeChannelVolume(buttonId, value))
        sliderList[buttonId].bind("<ButtonRelease-1>",
                                  lambda event: self.VolumeSave(event))
        sliderList[buttonId].grid(
            row=rowSpot+1, column=columnSpot+1, padx=(0, 20), pady=0, sticky='ew')
        tooltipList.append(CTkToolTip(
            sliderList[buttonId], message="Volume: 100"))

        # Changing what clicking the button does
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))

        # Grabbing names for List
        buttonNameList.append(buttons[buttonId].cget("text"))

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
        if loopList[buttonId].cget("fg_color") == loopColor:
            channelDict[buttonId].play(
                soundList[buttonId], loops=-1)
        else:
            channelDict[buttonId].play(soundList[buttonId])

    def LoopChecked(self, buttonId):
        # Checking if unchecked or checked
        if loopList[buttonId].cget("fg_color") == "transparent":
            loopList[buttonId].configure(fg_color=loopColor)
        else:
            loopList[buttonId].configure(fg_color="transparent")
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
        if buttonId < len(tooltipList):
            tooltipList[buttonId].configure(
                message="Volume: " + str(int(value * 100)))

        if buttonId < len(soundList):
            soundList[buttonId].set_volume(value)

    def DeleteSound(self, buttonId):
        # Check if sound playing first
        if buttonId in channelDict:
            if channelDict[buttonId].get_busy():
                channelDict[buttonId].stop()
                print("Stopped looping sound that was deleted!")

        print("Deleting button: ", buttonId)

        # Destroying and then updating dictionaries
        buttons[buttonId].destroy()
        buttons.pop(buttonId)

        deleteList[buttonId].destroy()
        deleteList.pop(buttonId)

        sliderList[buttonId].destroy()
        sliderList.pop(buttonId)

        loopList[buttonId].destroy()
        loopList.pop(buttonId)

        soundList.pop(buttonId)
        soundFileList.pop(buttonId)
        buttonNameList.pop(buttonId)
        tooltipList.pop(buttonId)

        if buttonId in channelDict:
            del channelDict[buttonId]

        # Saving
        self.WriteToFile()

        # Rearrange grid
        self.RearrangeGrid()

    def RearrangeGrid(self):
        # Figuring out where to place buttons
        totalButtons = len(buttons)

        for i in range(totalButtons):

            columnSpot = ((3 * i) % columns)
            rowSpot = 2 * floor(i * 3 / columns) + 2

            paddingx = (10, 10)

            if columnSpot == 0:
                paddingx = (20, 10)
            elif columnSpot == columns - 3:
                paddingx = (10, 20)

            buttons[i].grid_configure(row=rowSpot, column=columnSpot)
            buttons[i].configure(command=lambda index=i: self.PlaySound(index))

            sliderList[i].grid_configure(row=rowSpot+1, column=columnSpot+2)
            sliderList[i].configure(
                command=lambda value, index=i: self.ChangeChannelVolume(index, value))

            deleteList[i].grid_configure(row=rowSpot+1, column=columnSpot+1)
            deleteList[i].configure(
                command=lambda index=i: self.DeleteSound(index))

            loopList[i].grid_configure(row=rowSpot+1, column=columnSpot)
            loopList[i].configure(
                command=lambda index=i: self.LoopChecked(index))

            tooltipList[i] = CTkToolTip(sliderList[i], message="Volume: 100")

    def WriteToFile(self):
        # Writing to file
        with open("Data.csv", 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(soundFileList)
            writer.writerow(buttonNameList)

            loopValues = []
            sliderValues = []
            for i in range(len(loopList)):
                if loopList[i].cget("fg_color") == loopColor:
                    loopValues.append(1)
                else:
                    loopValues.append(0)

                sliderValues.append(sliderList[i].get())

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

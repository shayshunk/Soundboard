import tkinter as tk
import customtkinter as ctk
from pygame import mixer
from math import floor

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

mixer.init()
totalChannels = 8
mixer.set_num_channels(totalChannels)

columns = 3
span = columns - 1

buttons = {}
soundDictionary = {}
channelDictionary = {}


class Frame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.defaultFont = ctk.CTkFont(family='Agency FB', size=24)

        for i in range(columns):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(i, weight=1)

        # Hiding scrollbar
        yScrollbar = self._scrollbar
        yScrollbar.grid_forget()
        # get the default colors of frame
        frame_fg = ctk.ThemeManager.theme["CTkFrame"]["fg_color"]

        # Adding widgets onto frame
        self.label = ctk.CTkLabel(
            master=self, text="Soundboard", font=self.defaultFont)
        self.label.grid(row=0, column=0, columnspan=span,
                        padx=20, pady=20, sticky='WENS')

        self.button = ctk.CTkButton(
            master=self, text="Add Sound", command=lambda: self.AddButton(app), font=self.defaultFont)
        self.button.grid(row=0, column=span, padx=20, pady=20, sticky='WENS')

    def PlaySound(self, buttonId):
        soundFile = soundDictionary[buttonId]
        sound = mixer.Sound(soundFile)
        newChannel = mixer.find_channel(force=True)
        channelDictionary[buttonId] = newChannel
        newChannel.play(sound)

    def AddSound(self, buttonId):
        # Asking user to associate file with button
        soundFile = tk.filedialog.askopenfilename()

        # Associating sound with dictionary
        soundDictionary[buttonId] = soundFile
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))

    def AddButton(self, app):
        # Assigning new button to dictionary
        buttonId = str(len(buttons) + 1)

        # Figuring out where to place new button
        totalButtons = len(buttons)
        columnSpot = totalButtons % columns
        rowSpot = floor(totalButtons / columns) + 1

        # Creating new button for sound
        buttons[buttonId] = ctk.CTkButton(
            master=self, text="", font=self.defaultFont)
        buttons[buttonId].configure(command=self.AddSound(buttonId))
        buttons[buttonId].configure(width=150, height=100)
        buttons[buttonId].grid(row=rowSpot, column=columnSpot,
                               padx=20, pady=20, sticky="ew")

        # Adding entry box to get name for sound
        dialog = ctk.CTkInputDialog(
            text="Enter sound name:", title="Name your buton!")
        buttonName = dialog.get_input()
        buttons[buttonId].configure(text=buttonName)

        # Changing what clicking the button does
        buttons[buttonId].configure(command=lambda: self.PlaySound(buttonId))


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

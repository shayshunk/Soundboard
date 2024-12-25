import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


def AddButton(window):
    newButton = customtkinter.CTkButton(master=window, text='Added')
    newButton.pack(pady=10)


# Creating window
window = customtkinter.CTk()

window.geometry("800x800")
window.title("Soundboard")

label = customtkinter.CTkLabel(master=window, text="Soundboard")
label.pack(pady=20)

button = customtkinter.CTkButton(master=window, text="Add Sound",
                                 command=lambda: AddButton(window))
button.pack()

# Running
window.mainloop()

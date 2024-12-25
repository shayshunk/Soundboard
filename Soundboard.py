import tkinter as tk
import ttkbootstrap as ttk


def AddButton(window):
    newButton = ttk.Button(master=window, text='Added')
    newButton.pack(pady=10)


# Creating window
window = ttk.Window(themename='solar')

window.geometry("800x800")
window.title("Soundboard")

label = ttk.Label(master=window, text="Soundboard")
label.pack(pady=20)

button = ttk.Button(master=window, text="Add Sound",
                    command=lambda: AddButton(window))
button.pack()

# Running
window.mainloop()

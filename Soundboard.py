import tkinter as tk
import ttkbootstrap as ttk

# Creating window
window = ttk.Window(themename='solar')

window.geometry("800x800")
window.title("Soundboard")

label = ttk.Label(master=window, text="Soundboard")
label.pack(pady=20)

textbox = ttk.Text(master=window, height=3)
textbox.pack()

button = ttk.Button(master=window, text="Add Sound")
button.pack()

# Running
window.mainloop()

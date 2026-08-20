
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import customtkinter
from media import download_video
import threading
import os
import sys
import ctypes

customtkinter.set_appearance_mode("dark")

if sys.platform.startswith("win"):
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

root = customtkinter.CTk()
root.title('Media Downloader')

if sys.platform.startswith("win"):
    root.iconbitmap(resource_path("appicon.ico"))

elif sys.platform.startswith("linux"):
    icon = tkinter.PhotoImage(file=resource_path("appicon.png"))
    root.iconphoto(True, icon)


root.resizable(False, False)
root.geometry('800x600')

selected_folder = None  





def button_event():
    if selected_folder is None:
        messagebox.showwarning("MISSING FOLDER", "Select a folder!")
        return

    url = entry.get()
    if not url:
        messagebox.showwarning("MISSING LINK", "Paste a link!")
        return        

    format_type = segmented_button_var.get()
    progresslabel.configure(text="0%")

    thread = threading.Thread(target=download_video, args=(url, selected_folder, format_type, update_progress))
    thread.start()
  

def segmented_button_callback(value):
    destination_label_mp.configure(text=f"Currently selected: {value}")

def select_destination():
    global selected_folder
    folder_chosen = filedialog.askdirectory()
    if folder_chosen:
        selected_folder = folder_chosen
        destination_label.configure(text=selected_folder)

def update_progress(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes',0)
        if total:
            percent = int(downloaded / total * 100)
            progresslabel.configure(text=f"{percent}%")
    elif d['status'] == 'finished':
        progresslabel.configure(text="100%") 


ascii_art = """ __  __          _ _       
|  \\/  | ___  __| (_) __ _ 
| |\\/| |/ _ \\/ _` | |/ _` |
| |  | |  __/ (_| | | (_| |
|_|  |_|\\___|\\__,_|_|\\__,_|
                           
 ____                      _                 _           
|  _ \\  _____      ___ __ | | ___   __ _  __| | ___ _ __ 
| | | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__|
| |_| | (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |   
|____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|   """

ascii_label = customtkinter.CTkLabel(root, text=ascii_art, font=("Courier", 10, "bold"), justify="center", text_color="#22D3EE")
ascii_label.place(x=400, y=100, anchor="center")

segmented_button_var = customtkinter.StringVar(value="mp3")
segmented_button = customtkinter.CTkSegmentedButton(root, values=["mp3", "mp4"],selected_color="#22D3EE",selected_hover_color="#0E7490",command=segmented_button_callback, variable=segmented_button_var, width=200)
segmented_button.place(x=670, y=270, anchor="center")

destination_label_mp = customtkinter.CTkLabel(root, text=f"Currently selected: {segmented_button_var.get()}")
destination_label_mp.place(x=670, y=570, anchor="center")

button = customtkinter.CTkButton(root, height=50, width=100, text="Download", font=("Helvetica", 20, "bold"), fg_color="#22D3EE", hover_color="#0E7490", command=button_event)
button.place(x=400, y=320, anchor="center")

buttonselect = customtkinter.CTkButton(root, height=10, width=10, text="Select Download Folder",hover_color="#0E7490",fg_color="#22D3EE", command=select_destination)
buttonselect.place(x=100, y=270, anchor="center")

destination_label = customtkinter.CTkLabel(root, text="No folder selected")
destination_label.place(x=120, y=570, anchor="center")

progresslabel = customtkinter.CTkLabel(root, text="0%")
progresslabel.place(x=400,y=550)

entry = customtkinter.CTkEntry(root, placeholder_text="Paste link here", width=400)
entry.place(x=400, y=270, anchor="center")


def select_all(event):
    entry.select_range(0,'end')
    entry.icursor('end')
    return "break"

def handle_paste(event):
    entry.delete(0, 'end')
    entry.insert(0, root.clipboard_get())
    return "break"

entry.bind('<Control-a>',select_all)
entry.bind('<Control-v>', handle_paste)

root.mainloop()
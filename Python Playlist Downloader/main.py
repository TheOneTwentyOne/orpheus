# This section imports all of the required packages
import threading
import os
import tkinter as tk
from tkinter import filedialog, ttk
from optionflac import filterPlaylistFlac
from optionmp3 import filterPlaylistMp3

# Event handler for dropdown selection
def on_dropdown_select(event):
    global dropdownOption
    selected_option.set(event.widget.get())
    dropdownOption = selected_option.get()

# Event handler for checkbox changes
def on_checkbox_change():
    global checkboxStates
    checkboxStates = [checkbox1_var.get(), checkbox2_var.get(), checkbox3_var.get(), checkbox4_var.get()]

# Function to open file explorer to select directory
def select_directory():
    directory = filedialog.askdirectory()
    directoryBox.delete(0, tk.END)  # Clear previous entry
    directoryBox.insert(0, directory)

# Function to update progress bar
def update_progress(value):
    current_value = progress_bar["value"]
    if current_value < value * 10:
        progress_bar["value"] = current_value + 1
        mainframe.after(10, update_progress, value)


# Function to start download process in a separate thread
def start_download():
    directory_path = directoryBox.get() + '/'
    
    # Ensure the 'duplicates' folder exists, otherwise create it
    if not os.path.exists(directory_path + "duplicates"):
        os.mkdir(directory_path + "duplicates")

    url_link = urlBox.get()

    progress_var = tk.DoubleVar()
    progress_bar.configure(variable=progress_var)
    progress_var.set(0)

    # Create a separate thread to execute the download process
    if dropdownOption == '.mp3':
        download_thread = threading.Thread(target=filterPlaylistMp3, args=(url_link, directory_path, progress_var))
        download_thread.start()
    elif dropdownOption == '.flac':
        download_thread = threading.Thread(target=filterPlaylistFlac, args=(url_link, directory_path, progress_var))
        download_thread.start()


# Main application window
mainframe = tk.Tk()
mainframe.geometry("800x450")
mainframe.resizable(False, False)
mainframe.title("YTPFLACU")

# Global variables
checkboxStates = [True, True, True, True]
dropdownOption = ''

# Assigns all of the values for the grid. 'i' is the width, 16, and 'j' is the height, 9.
style = ttk.Style()
style.configure('CustomFrame.TFrame', background='black', relief='solid', borderwidth=1)
frames = {(i, j): ttk.Frame(mainframe, height=50, width=50, relief='solid', style='CustomFrame.TFrame') for i in range(16) for j in range(9)}
for i, j in frames:
    frames[i, j].grid(row=j, column=i)

# Widgets and UI elements
titleLabel = tk.Label(mainframe, text="YouTube Playlist to .flac Utility (YTPFLACU)", font=("MS Sans Serif", 22, 'bold'))
titleLabel.grid(row=0, column=2, columnspan=12, rowspan=2)

style = ttk.Style()
style.configure("Horizontal.TSeparator", background="green")
horizontalSeparator = ttk.Separator(mainframe, orient='horizontal', style="Horizontal.TSeparator")
horizontalSeparator.grid(row=1, column=1, columnspan=14, rowspan=2, sticky='ew')

style = ttk.Style()
style.configure("Vertical.TSeparator", background="green")
verticalSeparator = ttk.Separator(mainframe, orient='vertical', style="Vertical.TSeparator")
verticalSeparator.grid(row=2, column=7, columnspan=2, rowspan=6, sticky='ns')

urlLabel = ttk.Label(mainframe, text="Playlist URL:", font=("MS Sans Serif", 11))
urlLabel.grid(row=2, column=0, columnspan=3)
urlBox = ttk.Entry(mainframe, width=40)
urlBox.grid(row=2, column=2, columnspan=6)

directoryLabel = ttk.Label(mainframe, text="Output directory:", font=("MS Sans Serif", 11))
directoryLabel.grid(row=3, column=0, columnspan=3)
directoryButton = ttk.Button(mainframe, text="Select through Explorer", command=select_directory)
directoryButton.grid(row=4, column=2, columnspan=6)
directoryBox = ttk.Entry(mainframe, width=37)
directoryBox.grid(row=3, column=2, columnspan=6)

selected_option = tk.StringVar()    
dropdown_label = ttk.Label(mainframe, text="Select a file type:", font=("MS Sans Serif", 11))
dropdown_label.grid(row=5, column=0, columnspan=3)

options = [".mp3", ".flac"]
dropdown = ttk.Combobox(mainframe, textvariable=selected_option, values=options)
dropdown.grid(row=5, column=2, columnspan=6)
dropdown.bind("<<ComboboxSelected>>", on_dropdown_select)

checkbox_values = [tk.BooleanVar() for _ in range(4)]
checkbox_frame = ttk.Frame(mainframe)
checkbox_frame.grid(row=6, column=2, columnspan=6, rowspan=2)

checkbox_label = ttk.Label(mainframe, text="Select what you want:", font=("MS Sans Serif", 11))
checkbox_label.grid(row=6, column=0, columnspan=3, rowspan=2)

checkbox1_var = tk.BooleanVar()
checkbox1 = ttk.Checkbutton(checkbox_frame, text="Checkbox 1", variable=checkbox1_var, command=on_checkbox_change)
checkbox1.grid(row=0, column=0, padx=5, pady=5)

checkbox2_var = tk.BooleanVar()
checkbox2 = ttk.Checkbutton(checkbox_frame, text="Checkbox 2", variable=checkbox2_var, command=on_checkbox_change)
checkbox2.grid(row=0, column=1, padx=5, pady=5)

checkbox3_var = tk.BooleanVar()
checkbox3 = ttk.Checkbutton(checkbox_frame, text="Checkbox 3", variable=checkbox3_var, command=on_checkbox_change)
checkbox3.grid(row=1, column=0, padx=5, pady=5)

checkbox4_var = tk.BooleanVar()
checkbox4 = ttk.Checkbutton(checkbox_frame, text="Checkbox 4", variable=checkbox4_var, command=on_checkbox_change)
checkbox4.grid(row=1, column=1, padx=5, pady=5)

# Start button event handler
start_button = ttk.Button(mainframe, text="Activate Program", command=start_download)
start_button.grid(row=5, column=10, columnspan=4)

# Progress bar
progress_bar = ttk.Progressbar(mainframe, orient="horizontal", length=250, mode="determinate")
progress_bar.grid(row=4, column=9, columnspan=6)

# Run the application
if __name__ == '__main__':
    mainframe.mainloop()
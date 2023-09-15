# Layman's Description:
# This Python script is a graphical user interface (GUI) tool designed to automate
# the process of transferring folders from one location on your computer to another.
# When you run the program, a window appears with several options and buttons.
# Two dropdown menus at the top allow you to select or browse the 'source' and 'destination'
# locations on your computer. Below these menus, you'll find "Execute" and "Rename" buttons.
# 
# 1. "Execute" Button: Starts the process of moving folders from the source to the destination.
# It only moves folders that don't have certain keywords or file extensions in their names
# (like "mkv", "1080p", etc.). It also shows a progress bar and a percentage counter indicating 
# how much of each file has been moved.
# 
# 2. "Rename" Button: Executes another Python script that renames existing folders in a specified way.
# 
# 3. Progress Bar: As folders are being moved, a progress bar fills up to show the status of the transfer.
# 
# 4. Percentage Counter: Next to the progress bar, a percentage counter updates in real-time to show
# the progress of each individual file being moved.
# 
# 5. Log Box: Below the progress bar, a text box shows log messages that provide additional information
# about the process, such as which file is currently being moved.
# 
# 6. Current File Label: A label at the bottom displays the name of the file currently being moved.
# 
# The script uses multi-threading to ensure that the GUI remains responsive during the transfer process.




import os
import re
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading
import subprocess

import tkinter.filedialog as filedialog

def browse_folder(combo_box):
    """
    Browse the folder and set the selected folder in the combo box.

    Parameters:
    combo_box (object): The combo box object to set the selected folder.

    Returns:
    None
    """
    print("Selecting folder...")
    folder_selected = filedialog.askdirectory()
    print("Folder selected:", folder_selected)
    combo_box.set(folder_selected)

def copy_with_progress(src, dest, progress_bar, progress_label, max_value, current_file_label):
    """
    Copies a file from the source path to the destination path with a progress bar and labels.
    
    Args:
        src (str): The path of the source file to be copied.
        dest (str): The path of the destination file.
        progress_bar (tkinter.ttk.Progressbar): The progress bar widget that shows the copying progress.
        progress_label (tkinter.Label): The label widget that shows the copying progress percentage.
        max_value (int): The maximum value of the progress bar.
        current_file_label (tkinter.Label): The label widget that shows the name of the current file being copied.
    
    Returns:
        None
    """
    with open(src, 'rb') as fsrc, open(dest, 'wb') as fdest:
        total_size = os.path.getsize(src)
        copied_size = 0
        chunk_size = 1024 * 1024

        while True:
            buf = fsrc.read(chunk_size)
            if not buf:
                break
            fdest.write(buf)
            
            copied_size += len(buf)
            progress_value = (copied_size / total_size) * max_value
            progress_bar["value"] = progress_value

            percentage = (copied_size / total_size) * 100
            progress_label.config(text=f"{percentage:.1f}%")
            progress_label.update()

            current_file_label.config(text=f"Copying: {os.path.basename(src)}")
            current_file_label.update()

            # Add print statements for debugging
            print(f"Copying {os.path.basename(src)}")
            print(f"Progress: {percentage:.1f}%")
            print(f"Progress value: {progress_value}")

def execute_transfer(src_combo, dest_combo, progress_bar, progress_label, log_text, current_file_label):
    """
    Executes a transfer of files from the source folder to the destination folder.

    Parameters:
    - src_combo (tkinter.ComboBox): The ComboBox widget containing the source folder path.
    - dest_combo (tkinter.ComboBox): The ComboBox widget containing the destination folder path.
    - progress_bar (tkinter.ProgressBar): The ProgressBar widget representing the progress of the transfer.
    - progress_label (tkinter.Label): The Label widget displaying the progress of the transfer.
    - log_text (tkinter.Text): The Text widget displaying the log of the transfer.
    - current_file_label (tkinter.Label): The Label widget displaying the name of the current file being transferred.

    Returns:
    - None

    Description:
    - Retrieves the source and destination folder paths from the ComboBox widgets.
    - Checks if the source and destination folders exist. If not, returns immediately.
    - Iterates over each folder in the source folder.
    - For each folder, checks if it is empty. If so, skips it and logs the skip.
    - Checks if the destination path already exists or if the folder path is not a directory. If so, continues to the next folder.
    - Checks if the folder name matches any of the specified patterns. If so, continues to the next folder.
    - Checks if the folder name matches the pattern for a folder with a year suffix. If so, creates the destination path.
    - For each file in the folder, copies it to the destination folder with progress tracking.
    - Logs the start of the copy and updates the progress bar and label.
    - Logs the completion of the copy and updates the progress bar and label.
    - Deletes the original folder.
    - Logs any errors that occur during the transfer.
    """
    src_folder = src_combo.get()
    dest_folder = dest_combo.get()

    if not os.path.exists(src_folder) or not os.path.exists(dest_folder):
        return

    for folder_name in os.listdir(src_folder):
        folder_path = os.path.join(src_folder, folder_name)
        dest_path = os.path.join(dest_folder, folder_name)

        # Check if folder is empty
        if not os.listdir(folder_path):
            print(f"Skipping empty folder {folder_name}")
            log_text.insert(tk.END, f"Skipping empty folder {folder_name}\n")
            log_text.yview(tk.END)
            continue

        if os.path.exists(dest_path) or not os.path.isdir(folder_path):
            continue

        if re.search(r"(mkv|dolby|bluray|dvdrip|remux|avc|truehd|atmos|dts|fgt|hdtv|remastered|dvd|rarbg|1080p|720p|480p|360p|1440p|2k|4k|mov|mkv|m4k|mp4|avi|mpg|mpeg|m4v|wmv|ts|m2ts|flv|divx|heiv)", folder_name, re.I):
            continue

        if re.match(r".+ \(\d{4}\)$", folder_name):
            try:
                os.makedirs(dest_path, exist_ok=True)
                
                for filename in os.listdir(folder_path):
                    src_file_path = os.path.join(folder_path, filename)
                    dest_file_path = os.path.join(dest_path, filename)

                    print(f"Starting to copy {filename}")
                    log_text.insert(tk.END, f"Starting to copy {filename}\n")
                    log_text.yview(tk.END)

                    copy_with_progress(src_file_path, dest_file_path, progress_bar, progress_label, 100, current_file_label)

                print(f"Move complete, now deleting original folder {folder_name}")
                log_text.insert(tk.END, f"Move complete, now deleting original folder {folder_name}\n")
                log_text.yview(tk.END)

                shutil.rmtree(folder_path)
            except Exception as e:
                print(f"Error moving {folder_name}: {str(e)}")
                log_text.insert(tk.END, f"Error moving {folder_name}: {str(e)}\n")
                log_text.yview(tk.END)


import threading

def execute_in_thread(src_combo, dest_combo, progress_bar, progress_label, log_text, current_file_label):
    """
    Executes the given function in a separate thread.

    :param src_combo: The source combo box.
    :param dest_combo: The destination combo box.
    :param progress_bar: The progress bar.
    :param progress_label: The progress label.
    :param log_text: The log text.
    :param current_file_label: The current file label.

    :return: None
    """
    print("Starting execution in thread")
    t = threading.Thread(target=execute_transfer, args=(src_combo, dest_combo, progress_bar, progress_label, log_text, current_file_label))
    t.start()
    print("Execution in thread started")

import subprocess
import tkinter as tk

import os
import subprocess

def execute_rename_script(log_text):
    """
    Executes a rename script.

    Parameters:
        log_text (Text): The text widget used to display the log output.

    Returns:
        None
    """
    script_path = os.path.join("C:", "Users", "bax11", "OneDrive", "Desktop", "Script_Tasks", "Main", "Rename Existing Folders.py")
    process = subprocess.Popen(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output)  # Added print statement for debugging
            log_text.insert(tk.END, output)
            log_text.yview(tk.END)

root = tk.Tk()
root.title("Movie Transfer Utility")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

src_options = ["C:\\Holds", "C:\\Users\\bax11\\AppData\\Roaming\\Kodi\\userdata\\addon_data\\plugin.video.ezra\\Movies Downloads"]
src_combo = ttk.Combobox(frame, values=src_options, width=47)
src_combo.grid(row=0, column=0, sticky=tk.W)
src_combo.current(0)
src_button = ttk.Button(frame, text="Browse", command=lambda: browse_folder(src_combo))
src_button.grid(row=0, column=1)

dest_options = [
    "\\\\192.168.1.145\\e\\HD Movies", "\\\\192.168.1.145\\f\\HD Movies", "\\\\192.168.1.145\\j\\HD Movies",
    "\\\\192.168.1.145\\k\\HD Movies", "\\\\192.168.1.145\\l\\HD Movies", "\\\\192.168.1.145\\m\\HD Movies",
    "\\\\192.168.1.145\\n\\HD Movies", "\\\\192.168.1.145\\e\\Adult", "\\\\192.168.1.145\\f\\Adult",
    "\\\\192.168.1.145\\j\\Adult", "\\\\192.168.1.145\\k\\Adult", "\\\\192.168.1.145\\l\\Adult",
    "\\\\192.168.1.145\\m\\Adult", "\\\\192.168.1.145\\n\\Adult"
]
dest_combo = ttk.Combobox(frame, values=dest_options, width=47)
dest_combo.grid(row=1, column=0, sticky=tk.W)
dest_combo.current(6)
dest_button = ttk.Button(frame, text="Browse", command=lambda: browse_folder(dest_combo))
dest_button.grid(row=1, column=1)

execute_button = ttk.Button(frame, text="Execute", command=lambda: execute_in_thread(src_combo, dest_combo, progress_bar, progress_label, log_text, current_file_label))
execute_button.grid(row=2, column=0)

rename_button = ttk.Button(frame, text="Rename", command=lambda: execute_rename_script(log_text))
rename_button.grid(row=2, column=1)

progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=2)

progress_label = tk.Label(frame, text="0.0%")
progress_label.grid(row=3, column=2)

log_text = tk.Text(frame, height=10, width=80, bg="black", fg="lime green", font=("Arial", 12, "bold"))
log_text.grid(row=4, columnspan=3)

current_file_label = tk.Label(frame, text="Current File: ")
current_file_label.grid(row=5, columnspan=3)

root.mainloop()








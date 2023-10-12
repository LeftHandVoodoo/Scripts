'''
Network Drive Stats Program:

This is a user-friendly application that helps you monitor your network drives' storage usage. It's built on Tkinter 
for easy interaction. With just a click on "Get Stats", the program will scan through a list of network drives and 
provide the following:

1. Drive Labels: Shows the name or path of each network drive.
2. Progress Bars: Displays a progress bar for each drive to indicate the percentage of disk space used.
3. Summary: Presents a final summary showing the total, used, and free space across all network drives in terabytes.

Feel free to run the program and get an instant snapshot of your network storage usage!

'''

import os
import subprocess
import re
import tkinter as tk
from tkinter import ttk
from tkinter import font

def get_network_drive_stats():
    """
    Retrieves network drive statistics.
    
    This function iterates over the network_paths list and retrieves the disk statistics for each network drive. It displays the drive label and a progress bar for each drive, indicating the percentage of disk space used. The function assumes that drive N has a total capacity of 12 TB, while all other drives have a total capacity of 8 TB. It uses the subprocess module to run the 'dir' command on each network drive and captures the output to extract the number of free bytes. It then calculates the amount of used and free disk space in TB and updates the total_all_drives_tb, used_all_drives_tb, and free_all_drives_tb variables accordingly. If the 'dir' command fails or the output does not contain the expected information, an error message is displayed. Finally, it calls the display_summary function to display the summary of the total, used, and free disk space for all network drives.
    """
    network_paths = [
        r'\\192.168.1.145\e',
        r'\\192.168.1.145\f',
        r'\\192.168.1.145\j',
        r'\\192.168.1.145\k',
        r'\\192.168.1.145\l',
        r'\\192.168.1.145\m',
        r'\\192.168.1.145\n'
    ]

    for widget in frame.winfo_children():
        widget.destroy()

    total_all_drives_tb = 0
    used_all_drives_tb = 0
    free_all_drives_tb = 0

    for network_path in network_paths:
        print(f"Getting stats for {network_path}...")
        label = ttk.Label(frame, text=f"Network Drive {network_path}", style='Header.TLabel')
        label.pack(fill=tk.X, pady=5)

        progress = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate", style='Custom.Horizontal.TProgressbar')
        progress.pack(fill=tk.X, pady=5)

        try:
            total_tb = 12 if 'n' in network_path[-1].lower() else 8  # Assuming drive N is 12 TB, others are 8 TB
            total_all_drives_tb += total_tb
            
            print(f"Running 'dir {network_path}'")
            result = subprocess.run(['dir', network_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            lines = result.stdout.strip().split('\n')
            print(f"Output of 'dir {network_path}': {lines}")
            
            free_bytes_match = re.search(r"(\d+([,]\d{3})*) bytes free", lines[-1])
            
            if free_bytes_match:
                free_bytes_str = free_bytes_match.group(1)
                free_bytes = int(free_bytes_str.replace(',', ''))
                
                free_tb = free_bytes / (1024 ** 4)
                used_tb = total_tb - free_tb
                
                free_all_drives_tb += free_tb
                used_all_drives_tb += used_tb
                
                percent_used = (used_tb / total_tb) * 100
                progress["value"] = percent_used

            else:
                label.config(text=f"Could not find disk stats for {network_path}")

        except Exception as e:
            label.config(text=f"An error occurred while getting stats for {network_path}: {e}")

    display_summary(total_all_drives_tb, used_all_drives_tb, free_all_drives_tb)

import tkinter as tk
from tkinter import ttk

def display_summary(total, used, free):
    """
    Creates a summary display on a Tkinter frame.

    Args:
        total (float): The total size of all drives in terabytes.
        used (float): The total used space across all drives in terabytes.
        free (float): The total free space across all drives in terabytes.

    Returns:
        None
    """
    frame = tk.Tk()

    label_summary = ttk.Label(frame, text="Summary:", style='Header.TLabel')
    label_summary.pack(fill=tk.X, pady=5)

    label_total = ttk.Label(frame, text=f"Total size of all drives: {total:.2f} TB", style='Body.TLabel')
    label_total.pack(fill=tk.X, pady=5)

    label_used = ttk.Label(frame, text=f"Total used across all drives: {used:.2f} TB", style='Body.TLabel')
    label_used.pack(fill=tk.X, pady=5)

    label_free = ttk.Label(frame, text=f"Total free across all drives: {free:.2f} TB", style='Body.TLabel')
    label_free.pack(fill=tk.X, pady=5)

    percent_used_all_drives = (used / total) * 100
    label_percent = ttk.Label(frame, text=f"Overall percent used: {percent_used_all_drives:.2f}%", style='Body.TLabel')
    label_percent.pack(fill=tk.X, pady=5)

    frame.mainloop()

# Debug print statements
total_size = 10
used_size = 5
free_size = 5

print(f"Total size: {total_size} TB")
print(f"Used size: {used_size} TB")
print(f"Free size: {free_size} TB")

display_summary(total_size, used_size, free_size)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Network Drive Stats")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Header.TLabel', font=('Arial', 14, 'bold'), background='#f1f1f1')
    style.configure('Body.TLabel', font=('Arial', 12), background='#f1f1f1')
    style.configure('Custom.Horizontal.TProgressbar', thickness=20, background='#00ff00', troughcolor='#f1f1f1')

    frame = ttk.Frame(root, padding="10", style='My.TFrame')
    frame.pack(fill=tk.BOTH, expand=True)

    button = ttk.Button(root, text="Get Stats", command=get_network_drive_stats)
    button.pack(fill=tk.X, padx=10, pady=10)

    root.mainloop()
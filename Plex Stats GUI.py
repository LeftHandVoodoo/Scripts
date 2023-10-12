import tkinter as tk
import os
import subprocess

def run_plex_movie_scraper():
    script_path = r'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Main\Plex Movie Scrapper.py'
    subprocess.run(['python', script_path])

def run_comparison():
    script_path = r'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Main\Comparison.py'
    subprocess.run(['python', script_path])

# Create the main window
root = tk.Tk()
root.title("Script Runner")

# Create buttons
plex_button = tk.Button(root, text="Plex Movie Scraper", command=run_plex_movie_scraper)
comparison_button = tk.Button(root, text="Comparison", command=run_comparison)

# Place buttons on the window
plex_button.pack()
comparison_button.pack()

# Run the Tkinter event loop
root.mainloop()

if __name__ == "__main__":
    run_plex_movie_scraper()
    run_comparison()
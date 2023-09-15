'''
This is a Folder Cleaner Program. It scans through the selected directory to find empty or less useful folders.
Once it identifies these folders, it presents you with a summary and asks for confirmation to move them to a "Trash_Folder".
The program uses a graphical interface built with Tkinter, so you can easily interact with it. Here's what it does:

1. "Undo Delete": Allows you to restore folders that were moved to the trash folder.
2. "Browse": Lets you select the folder you want to clean up.
3. "Output Panel": Displays the status and results of the folder cleaning operation.

Simply click "Browse" to choose a folder and let the program do its magic!

'''

import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, Text, messagebox, Button
from concurrent.futures import ThreadPoolExecutor
import magic
import subprocess

deleted_folders = []

def undo_delete():
    """
    Restores the deleted folders by moving them from the trash folder back to their original location.

    This function iterates over each tuple in the `deleted_folders` list, where each tuple contains the original folder path and the corresponding trash folder path. It attempts to move the trash folder back to the original location using the `shutil.move()` function. If the move is successful, it prints a message indicating that the folder has been restored. If an exception occurs during the move operation, it prints an error message.

    After restoring all the folders, the `deleted_folders` list is cleared using the `del` statement.

    Parameters:
        None

    Returns:
        None
    """
    for original_folder, trash_folder in deleted_folders:
        try:
            shutil.move(trash_folder, original_folder)
            print(f"Restored folder: {original_folder}")
        except Exception as e:
            print(f"Error restoring folder {original_folder}: {e}")
    del deleted_folders[:]

def create_or_get_trash_folder(folder):
    drive = os.path.splitdrive(folder)[0]
    trash_folder = os.path.join(drive + '/', 'Trash_Folder')
    if not os.path.exists(trash_folder):
        print(f"Creating directory: {trash_folder}")
        os.mkdir(trash_folder)
    return trash_folder

def confirmation_popup(empty_folders, total_size_MB, extension_tally, skipped_extension_tally, trash_folder):
    """
    Displays a confirmation popup to the user, asking if they want to move the empty folders to the trash folder.
    
    Parameters:
    - empty_folders (list): A list of empty folders to be moved to the trash folder.
    - total_size_MB (float): The total size of the files in the empty folders in MB.
    - extension_tally (dict): A dictionary containing the tally of each file extension in the empty folders.
    - skipped_extension_tally (dict): A dictionary containing the tally of skipped file extensions in the empty folders.
    - trash_folder (str): The path to the trash folder where the empty folders will be moved.
    
    Returns:
    - None
    
    Prints:
    - Confirmation Message: The message displayed in the confirmation popup.
    - User's Answer: The user's answer to the confirmation popup.
    - Moving folder from: The path of the folder being moved.
    - Moving folder to: The path of the destination folder in the trash folder.
    - Moved folder to trash folder: The path of the folder that was successfully moved to the trash folder.
    - Error moving folder to trash folder: The path of the folder that encountered an error while moving to the trash folder.
    - Folders moved to trash folder.
    - No folders moved.
    
    Inserts Text:
    - Moved folder to trash folder: Inserts a line of text indicating that a folder was moved to the trash folder.
    - Error moving folder to trash folder: Inserts a line of text indicating that an error occurred while moving a folder to the trash folder.
    - Folders moved to trash folder: Inserts a line of text indicating that all folders were successfully moved to the trash folder.
    - No folders moved: Inserts a line of text indicating that no folders were moved.
    """
    global deleted_folders
    message = f"Do you want to move these folders to the trash folder? Total file size: {total_size_MB} MB. "
    message += f"Total Folders: {len(empty_folders)}."
    print("Confirmation Message:", message)
    
    answer = messagebox.askyesno("Confirmation", message)
    print("User's Answer:", answer)
    
    if answer:
        for folder in empty_folders:
            try:
                new_folder_name = os.path.basename(folder)
                new_path = os.path.join(trash_folder, new_folder_name)
                print("Moving folder from:", folder)
                print("Moving folder to:", new_path)
                
                shutil.move(folder, new_path)
                deleted_folders.append((folder, new_path))
                
                print("Moved folder to trash folder:", folder)
                insert_text(f"Moved folder to trash folder: {folder}\n")
            except Exception as e:
                print("Error moving folder to trash folder:", folder, e)
                insert_text(f"Error moving folder {folder} to trash folder: {e}\n")
        
        print("Folders moved to trash folder.")
        insert_text("Folders moved to trash folder.\n")
        
        subprocess.run(f'explorer {trash_folder}')
    else:
        print("No folders moved.")
        insert_text("No folders moved.\n")

def insert_text(text):
    print("Inserting text:", text)
    output_text.insert(tk.END, text)
    output_text.see(tk.END)
    print("Text inserted successfully")

import threading
from tkinter import filedialog

def choose_folder():
    """
    Prompt the user to choose a folder and start a new thread to search and tally files in the selected folder.
    """
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        print(f"Selected folder: {folder_selected}")
        threading.Thread(target=search_and_tally, args=(folder_selected,)).start()

def search_and_tally(folder):
    """
    Given a folder, this function searches for files within the folder and tallies the number of files found.

    Parameters:
    - folder (str): The folder in which to search for files.

    Returns:
    None
    """
    # Implementation of search and tally functionality
    print("Searching for files in folder:", folder)
    print("Tallying the files found...")
    pass

def inspect_folder(dirpath, empty_folders, extension_tally, skipped_extension_tally, total_size):
    """
    Inspects a folder and collects information about its contents.

    Parameters:
        dirpath (str): The path of the folder to inspect.
        empty_folders (list): A list to store empty folders.
        extension_tally (dict): A dictionary to tally file extensions and their sizes.
        skipped_extension_tally (dict): A dictionary to tally skipped file extensions and their sizes.
        total_size (list): A list to store the total size of files in the folder.

    Returns:
        None
    """
    print(f"Checking folder: {dirpath}\n")
    has_media = False
    local_extension_tally = {}
    
    for file in os.listdir(dirpath):
        file_path = os.path.join(dirpath, file)
        mime = magic.Magic()
        file_type = mime.from_file(file_path)
        
        ext = os.path.splitext(file)[-1].lower()
        
        if 'video' in file_type or ext in ['.mov', '.avi', '.mkv', '.m4k', '.mpg', '.mpeg', '.mp4', '.m4v', '.wmv', '.ts', '.m2ts', '.iso', '.flv', '.divx', '.flv']:
            print("    Media file found, skipping folder.\n")
            has_media = True
            if ext not in skipped_extension_tally:
                skipped_extension_tally[ext] = 0
            skipped_extension_tally[ext] += os.path.getsize(file_path)
            break
            
        if ext not in local_extension_tally:
            local_extension_tally[ext] = 0
        local_extension_tally[ext] += os.path.getsize(file_path)
        
        total_size[0] += os.path.getsize(file_path)
    
    if not has_media:
        empty_folders.append(dirpath)
        for ext, size in local_extension_tally.items():
            if ext not in extension_tally:
                extension_tally[ext] = 0
            extension_tally[ext] += size

def search_and_tally(folder):
    """
    Searches through a given folder and tallies various information about its contents.

    Parameters:
        folder (str): The path to the folder to be searched.

    Returns:
        None
    """
    empty_folders = []
    extension_tally = {}
    skipped_extension_tally = {}
    total_size = [0]
    trash_folder = create_or_get_trash_folder(folder)

    with ThreadPoolExecutor() as executor:
        executor.map(lambda dirpath: inspect_folder(dirpath, empty_folders, extension_tally, skipped_extension_tally, total_size), (dirpath for dirpath, _, _ in os.walk(folder)))

    total_size_MB = round(total_size[0] / (1024 * 1024), 1)
    print(f"Total number of folders without media files: {len(empty_folders)}")
    print(f"Total size of files in these folders: {total_size_MB} MB")

    print("File extensions to be deleted:")
    for ext, size in extension_tally.items():
        size_MB = round(size / (1024 * 1024), 1)
        print(f"{ext} - {size_MB} MB")

    print("File extensions to be skipped:")
    for ext, size in skipped_extension_tally.items():
        size_MB = round(size / (1024 * 1024), 1)
        print(f"{ext} - {size_MB} MB")

    print("Do you want to move these folders to the trash folder? (See popup for confirmation)")
    confirmation_popup(empty_folders, total_size_MB, extension_tally, skipped_extension_tally, trash_folder)

root = tk.Tk()
root.title("Folder Cleaner")

browse_button = tk.Button(root, text="Browse", command=choose_folder)
browse_button.pack()

undo_button = Button(root, text="Undo Move", command=undo_delete)
undo_button.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = Text(root, bg="black", fg="#00FF00", font=("Courier", 12, "bold"), yscrollcommand=scrollbar.set)
output_text.pack(expand=1, fill=tk.BOTH)

scrollbar.config(command=output_text.yview)

root.mainloop()

import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog

def is_file_open(file_path):
    try:
        with open(file_path, 'a', os.O_EXCL) as file:
            print("File successfully opened")
            return False
    except (FileExistsError, PermissionError) as e:
        print(f"Error opening file: {e}")
        return True

def rename_folder(folder_name, directory_path, movie_extensions):
    folder_path = os.path.join(directory_path, folder_name)
    
    # Check if folder is empty
    if not os.listdir(folder_path):
        print(f"Skipping empty folder {folder_name}")
        return 'skip', folder_name, None

    year_match = re.search(r'\b\d{4}\b', folder_name)
    if not year_match:
        print(f"Skipping folder: {folder_name} because it does not contain a year.")
        return 'skip', folder_name, None

    year = year_match.group()
    movie_name = re.sub(r'[^\w\s]', ' ', folder_name[:year_match.start()]).strip()
    movie_name = ' '.join(movie_name.split())
    new_folder_name = f"{movie_name} ({year})"
    
    new_folder_path = os.path.join(directory_path, new_folder_name)
    if os.path.exists(new_folder_path):
        print(f"Warning: {new_folder_name} already exists. Skipping.")
        return 'skip', folder_name, None

    contains_movie = False
    for root, _, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in movie_extensions):
                file_path = os.path.join(root, file)
                if is_file_open(file_path):
                    print(f"Skipping folder: {folder_name} because {file} is still open or being written to.")
                    return 'file_open', folder_name, None
                contains_movie = True
                break
        if contains_movie:
            break
    
    if folder_name != new_folder_name:
        try:
            os.rename(folder_path, new_folder_path)
            print(f"Renaming folder: {folder_name} to {new_folder_name}.")
            return 'rename', folder_name, new_folder_name
        except PermissionError:
            print(f"Skipping folder: {folder_name} due to permission error")
            return 'permission_error', folder_name, None
    
    if not contains_movie:
        return 'no_movie', folder_name, None
    
    return 'skip', folder_name, None

if __name__ == '__main__':
    def rename_folders(directory_path):
        renamed_count = 0
        skipped_count = 0
        movie_extensions = ['.mov', '.mkv', '.m4k', '.mp4', '.avi', '.mpg', '.mpeg', '.m4v', '.wmv', '.ts', '.m2ts', '.flv', '.divx']
        
        folder_names = [name for name in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, name))]

        for folder_name in folder_names:
            status, old_name, new_name = rename_folder(folder_name, directory_path, movie_extensions)
            
            if status == 'rename':
                print(f"Renamed: {old_name} -> {new_name}")
                renamed_count += 1
            elif status == 'skip':
                print(f"Skipped: {old_name} (already in correct format or unrecognizable pattern)")
                skipped_count += 1
            elif status == 'permission_error':
                skipped_count += 1
            elif status == 'file_open':
                skipped_count += 1
        
        print(f"\nTotal folders renamed: {renamed_count}")
        print(f"Total folders skipped: {skipped_count}")

    root = tk.Tk()
    root.withdraw()

    directory_path = filedialog.askdirectory(title="Select the directory")

    root.destroy()

    rename_folders(directory_path)

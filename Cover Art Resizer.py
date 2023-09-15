"""
This script is designed to automatically resize image files in a selected folder.
It uses the Python Imaging Library (PIL) to handle image operations.

The script performs the following tasks:
1. Opens a Windows Explorer prompt to allow the user to select a folder.
2. Checks for a subfolder named "resized" within the selected folder. If it doesn't exist, the script creates one.
3. Loops through each image file in the selected folder and resizes it to 500x750 pixels.
4. Saves the resized image in the "resized" subfolder with "_resized" appended to the original filename.
5. Prints the names of the files that have been resized.
6. Prints the total number of files resized at the end.

Supported image formats: JPEG, JPG, PNG, BMP, TIFF, GIF

The script includes a function called 'resize_images' which accepts an 'extension' parameter.
Only images with the provided extension will be resized.
"""

import os
from tkinter import filedialog
from tkinter import Tk
from PIL import Image

import os
from PIL import Image

def resize_images(extension):
    """
    Resizes images with the specified extension.

    Args:
        extension (str): The file extension of the images to be resized.

    Returns:
        None
    """
    # Initialize counter for resized files
    resized_count = 0

    # Loop through each file in the selected folder
    for filename in os.listdir(folder_selected):
        try:
            # Skip files that don't have the specified extension
            if not filename.lower().endswith(extension.lower()):
                continue

            # Generate full file path
            file_path = os.path.join(folder_selected, filename)

            # Generate new file name and save path
            file_name_parts = filename.rsplit('.', 1)
            new_filename = f"{file_name_parts[0]}_resized.{file_name_parts[1]}"
            new_file_path = os.path.join(resized_folder, new_filename)

            # Check if resized file already exists
            if os.path.exists(new_file_path):
                print(f"Skipped: {new_filename} already exists.")
                continue

            # Open image using PIL
            with Image.open(file_path) as image:
                # Check if the image format is supported
                if image.format.upper() in supported_formats:
                    # Resize the image to 500x750
                    resized_image = image.resize((500, 750), Image.ANTIALIAS)

                    # Save the resized image
                    resized_image.save(new_file_path)

                    # Print the name of the resized file
                    print(f"Resized: {new_filename}")

                    # Increment the counter
                    resized_count += 1

        except Exception as e:
            # Print error message if something goes wrong
            print(f"Error resizing {filename}: {e}")

    # Print the total number of resized files
    print(f"Total number of files resized: {resized_count}")

# Initialize the Tkinter window, but don't show it
root = Tk()
root.withdraw()

# Open Windows Explorer prompt to select folder
folder_selected = filedialog.askdirectory()

# Supported image file formats for PIL
supported_formats = ["JPEG", "JPG", "PNG", "BMP", "TIFF", "GIF"]

# Check if there is a folder named "resized" in the directory
resized_folder = os.path.join(folder_selected, "resized")
if not os.path.exists(resized_folder):
    os.makedirs(resized_folder)

# Print selected folder
print(f"Selected folder: {folder_selected}")

# Call the resize_images function and specify the extension you want to filter by, for example ".jpg"
resize_images(".jpg")

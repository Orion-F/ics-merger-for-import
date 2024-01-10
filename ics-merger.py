import tkinter as tk
from tkinter import filedialog
import os
import glob

def merge_ics_files():
    # Set up the root tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Open the folder select dialog
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return "No folder selected."

    # Find all ICS files in the folder
    ics_files = glob.glob(os.path.join(folder_path, '*.ics'))

    # Check if there are ICS files in the folder
    if not ics_files:
        return "No ICS files found in the folder."

    # Start of the ICS file
    merged_content = "BEGIN:VCALENDAR\nVERSION:2.0\n"

    # Iterate over each file and append its content
    for file_path in ics_files:
        with open(file_path, 'r') as file:
            # Skip the first two lines (BEGIN:VCALENDAR and VERSION:2.0) and the last line (END:VCALENDAR)
            content = file.readlines()[2:-1]
            merged_content += ''.join(content)

    # End of the ICS file
    merged_content += "END:VCALENDAR"

    # Create a merged file
    merged_file_name = "_MERGED_" + os.path.basename(folder_path) + ".ics"
    merged_file_path = os.path.join(folder_path, merged_file_name)
    
    with open(merged_file_path, 'w') as merged_file:
        merged_file.write(merged_content)

    return f"Merged ICS file created: {merged_file_path}"

# Run the function
merge_ics_files()
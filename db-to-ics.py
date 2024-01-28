from icalendar import Calendar, Event
from datetime import datetime
import re
import tkinter as tk
from tkinter import filedialog
import pytz

# Function to parse user input
def parse_user_input(user_input):
    date_pattern = r"Verbindung am .+ (\d{2}\.\d{2}\.\d{4})"
    departure_pattern = r"von (.+), Abfahrt (\d{2}:\d{2}) Uhr (.+?) mit (.+)"
    arrival_pattern = r"nach (.+), Ankunft (\d{2}:\d{2}) Uhr (.+?) mit"
    link_pattern = r"Verbindung ansehen: (.+)"
    
    date = re.search(date_pattern, user_input).group(1)
    departure_data = re.search(departure_pattern, user_input)
    arrival_data = re.search(arrival_pattern, user_input)
    link = re.search(link_pattern, user_input).group(1)

    return {
        "date": date,
        "start_station": departure_data.group(1),
        "start_time": departure_data.group(2),
        "start_platform": departure_data.group(3),
        "train_number": departure_data.group(4),
        "end_station": arrival_data.group(1),
        "arrival_time": arrival_data.group(2),
        "end_platform": arrival_data.group(3),
        "link": link
    }

# Collect 4 lines of user input
user_input_lines = []
print("Please enter your travel details (4 lines):")
for _ in range(4):
    line = input()
    user_input_lines.append(line)
user_input = "\n".join(user_input_lines)

# Parse user input
travel_details = parse_user_input(user_input)

# Time zone for Vienna
vienna_tz = pytz.timezone('Europe/Vienna')

# Convert times to datetime objects with Vienna time zone
fmt = "%d.%m.%Y %H:%M"
departure_time = vienna_tz.localize(datetime.strptime(f"{travel_details['date']} {travel_details['start_time']}", fmt))
arrival_time = vienna_tz.localize(datetime.strptime(f"{travel_details['date']} {travel_details['arrival_time']}", fmt))

# Create calendar and event
cal = Calendar()
event = Event()

# Set event details
event.add('summary', f'Train from {travel_details["start_station"]} to {travel_details["end_station"]}')
event.add('dtstart', departure_time)
event.add('dtend', arrival_time)
event.add('location', f'From {travel_details["start_station"]} {travel_details["start_platform"]} to {travel_details["end_station"]} {travel_details["end_platform"]}')
event.add('description', f'Train number: {travel_details["train_number"]}\nView journey: {travel_details["link"]}')

# Add event to calendar
cal.add_component(event)

# Initialize Tkinter root
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open file dialog for the user to choose file location and name
file_path = filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")], title="Save ICS File")

# Check if a file path was selected
if file_path:
    # Write to file
    with open(file_path, 'wb') as f:
        f.write(cal.to_ical())
    print(f'ICS file created: {file_path}')
else:
    print("File save cancelled.")

import requests
import matplotlib.pyplot as plt
import numpy as np

# Function to fetch lap data for a specific driver
def fetch_lap_data(driver_number, session_key=9078):
    url = f"https://api.openf1.org/v1/laps?driver_number={driver_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        lap_numbers = [entry['lap_number'] for entry in data if entry['lap_duration'] is not None]
        lap_durations = [entry['lap_duration'] for entry in data if entry['lap_duration'] is not None]
        lap_numbers = [1] + lap_numbers
        lap_durations = [(data[0]['duration_sector_2'] + data[0]['duration_sector_3'])] + lap_durations
        return lap_numbers, lap_durations
    else:
        print(f"Failed to fetch data for driver {driver_number}. Status code: {response.status_code}")
        return [], []

# Fetch lap data for Driver 1
lap_numbers_driver1, lap_durations_driver1 = fetch_lap_data(driver_number=1)

# Fetch lap data for Driver 2
lap_numbers_driver2, lap_durations_driver2 = fetch_lap_data(driver_number=11)

# Calculate the total lap time for each driver
total_time_driver1 = sum(lap_durations_driver1)
total_time_driver2 = sum(lap_durations_driver2)

# Print total time for each driver
print(f"Total lap time for Driver 1: {total_time_driver1:.2f} seconds")
print(f"Total lap time for Driver 2: {total_time_driver2:.2f} seconds")

# Ensure both drivers have the same number of laps for comparison
common_laps = min(len(lap_numbers_driver1), len(lap_numbers_driver2))

lap_numbers_driver1 = lap_numbers_driver1[:common_laps]
lap_durations_driver1 = lap_durations_driver1[:common_laps]
lap_numbers_driver2 = lap_numbers_driver2[:common_laps]
lap_durations_driver2 = lap_durations_driver2[:common_laps]

# Define the width of the bars
bar_width = 0.35

# Create a figure
plt.figure(figsize=(30, 20))

# Define the position of bars on the X-axis
r1 = np.arange(len(lap_numbers_driver1))
r2 = [x + bar_width for x in r1]

# Create bars for Driver 1
plt.bar(r1, lap_durations_driver1, color='blue', width=bar_width, edgecolor='grey', label='Driver 1')

# Create bars for Driver 2
plt.bar(r2, lap_durations_driver2, color='red', width=bar_width, edgecolor='grey', label='Driver 2')

# Add labels and title
plt.xlabel('Lap Number', fontweight='bold')
plt.ylabel('Lap Duration (seconds)', fontweight='bold')
plt.title('Lap Duration Comparison for Drivers 1 and 2')

# Add a legend
plt.legend()

# Customize the ticks
plt.xticks([r + bar_width/2 for r in range(len(lap_numbers_driver1))], lap_numbers_driver1)

# Add a grid
plt.grid(True, which="both", ls="--")

# Show the plot
plt.tight_layout()
plt.show()

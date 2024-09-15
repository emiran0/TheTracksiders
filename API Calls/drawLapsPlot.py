import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Function to fetch lap data for a specific driver
def fetch_lap_data(driver_number, session_key='latest'):
    url = f"https://api.openf1.org/v1/laps?driver_number={driver_number}&session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        lap_numbers = [entry['lap_number'] for entry in data if type(entry['lap_duration']) is float]
        lap_durations = [entry['lap_duration'] for entry in data if type(entry['lap_duration']) is float]
        return df
    else:
        print(f"Failed to fetch data for driver {driver_number}. Status code: {response.status_code}")
        return [], []

def fetch_compund_data(driver_number, session_key='latest'):
    url = f"https://api.openf1.org/v1/stints?session_key={session_key}&driver_number={driver_number}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Failed to fetch data for driver {driver_number}. Status code: {response.status_code}")
        return []

# Fetch lap data for Driver 1
# lap_numbers_driver1, lap_durations_driver1 = fetch_lap_data(driver_number=11)
# print(lap_numbers_driver1)
driver_num = 44
# drivers = [1,3,4,16,44,55,81,14,63,50,27,18,77,22,43,23,10,24,31,11]
drivers = [81, 16]
total_medium_compound_count = 0
for num in drivers:
    try:
        lap_data_driver1 = fetch_lap_data(driver_number=num)
        print(lap_data_driver1.loc[:, ['driver_number', 'lap_number', 'lap_duration']])

        stint_data_driver1 = fetch_compund_data(driver_number=num)
        # print(stint_data_driver1.loc[:, ['driver_number', 'stint_number', 'compound', 'lap_start', 'lap_end']])

        # Merge the stint data with lap data where the driver number overlaps
        merged_data_driver1 = pd.merge(lap_data_driver1, stint_data_driver1, on='driver_number', how='left')

        # Filter the merged data to include only relevant laps
        merged_data_driver1 = merged_data_driver1[(merged_data_driver1['lap_number'] >= merged_data_driver1['lap_start']) & 
                                                (merged_data_driver1['lap_number'] <= merged_data_driver1['lap_end'])]
        merged_data_driver1 = merged_data_driver1.sort_values(by='lap_duration')
        print(merged_data_driver1.loc[:, ['driver_number', 'lap_number', 'lap_duration', 'stint_number', 'compound']])
        # Count the rows with compound 'MEDIUM'
        total_medium_compound_count += merged_data_driver1[merged_data_driver1['compound'] == 'MEDIUM'].shape[0]
        print(f"Number of laps with 'MEDIUM' compound: {total_medium_compound_count}")
    except:
        continue
print(f"Total number of laps with 'MEDIUM' compound: {total_medium_compound_count}")



# Calculate the total lap time for each driver
# total_time_driver1 = sum(lap_durations_driver1)
# total_time_driver2 = sum(lap_durations_driver2)

# # Print total time for each driver
# print(f"Total lap time for Driver 1: {total_time_driver1:.2f} seconds")
# print(f"Total lap time for Driver 2: {total_time_driver2:.2f} seconds")

# # Ensure both drivers have the same number of laps for comparison
# common_laps = min(len(lap_numbers_driver1), len(lap_numbers_driver2))

# lap_numbers_driver1 = lap_numbers_driver1[:common_laps]
# lap_durations_driver1 = lap_durations_driver1[:common_laps]
# lap_numbers_driver2 = lap_numbers_driver2[:common_laps]
# lap_durations_driver2 = lap_durations_driver2[:common_laps]

# # Define the width of the bars
# bar_width = 0.35

# # Create a figure
# plt.figure(figsize=(30, 20))

# # Define the position of bars on the X-axis
# r1 = np.arange(len(lap_numbers_driver1))
# r2 = [x + bar_width for x in r1]

# # Create bars for Driver 1
# plt.bar(r1, lap_durations_driver1, color='blue', width=bar_width, edgecolor='grey', label='Driver 1')

# # Create bars for Driver 2
# plt.bar(r2, lap_durations_driver2, color='red', width=bar_width, edgecolor='grey', label='Driver 2')

# # Add labels and title
# plt.xlabel('Lap Number', fontweight='bold')
# plt.ylabel('Lap Duration (seconds)', fontweight='bold')
# plt.title('Lap Duration Comparison for Drivers 1 and 2')

# # Add a legend
# plt.legend()

# # Customize the ticks
# plt.xticks([r + bar_width/2 for r in range(len(lap_numbers_driver1))], lap_numbers_driver1)

# # Add a grid
# plt.grid(True, which="both", ls="--")

# # Show the plot
# plt.tight_layout()
# plt.show()

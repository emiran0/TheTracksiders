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
    

driver1_laps = fetch_lap_data(81)
driver2_laps = fetch_lap_data(16)

# Filter out laps with duration higher than 120 seconds
driver1_laps = driver1_laps[driver1_laps['lap_number'] >= 40]
driver2_laps = driver2_laps[driver2_laps['lap_number'] >= 40]

print(driver1_laps)

# Compare the lap durations of the two drivers using a bar plot
bar_width = 0.35
# index = np.arange(len(driver1_laps))
index = driver1_laps['lap_number']
plt.style.use('dark_background')

plt.bar(index, driver1_laps['lap_duration'], bar_width, label='Driver 1', color='orange')
plt.bar(index + bar_width, driver2_laps['lap_duration'], bar_width, label='Driver 2', color='red')

# Calculate average lap durations
avg_driver1 = driver1_laps['lap_duration'].mean()
avg_driver2 = driver2_laps['lap_duration'].mean()

# Plot average lap duration lines
plt.axhline(y=avg_driver1, color='blue', linestyle='--', linewidth=1, label='Avg Driver 1')
plt.axhline(y=avg_driver2, color='orange', linestyle='--', linewidth=1, label='Avg Driver 2')

plt.xlabel('Lap Number')
plt.ylabel('Lap Duration (s)')
plt.title('Lap Durations Comparison')

plt.legend()
plt.show()
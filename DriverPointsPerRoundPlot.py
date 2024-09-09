import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import time
import json

# ff1.Cache.enable_cache('/Users/emiran/Library/Caches/fastf1')

# DriverNums = ['4', '1']
# TeamColors = {'McLaren': (245/255, 118/255, 52/255, 1.0),
#               'RedBull': (0/255, 55/255, 115/255, 1.0)}
# plt_title = 'Speed vs Time Comparison with Sector Pass Points (Qualification)'

# points = {}
# positionPoints = {1: 25, 2: 18, 3: 15, 4: 12, 5: 10, 6: 8, 7: 6, 8: 4, 9: 2, 10: 1}
# for i in range(11, 21):
#     positionPoints[i] = 0
# rounds = []

# schedule = ff1.get_event_schedule(2024)
# gp_list = schedule.loc[1:16,['Location', 'EventName', 'EventFormat']]
# for round, eventName, format in zip(gp_list['Location'], gp_list['EventName'], gp_list['EventFormat']):
    
#     # try:
#     session = ff1.get_session(2024, round, 'R')
#     session.load(weather=False, messages=False)
#     results = session.results
#     result_print = results.loc[:,['Abbreviation','TeamName', 'Points']]
#     print(result_print)
#     for driver, point in zip(results['Abbreviation'], results['Points']):
#         if driver not in points.keys():
#             if type(point) is float:
#                 points[driver] = point
#         else:
#             if type(point) is float:
#                 points[driver] += point
#         # print(f'{driver} - {points}')
#     # time.sleep(2)
#     if format == 'sprint_qualifying':
#         session = ff1.get_session(2024, round, 'S')
#         session.load(weather=False, messages=False)
#         results = session.results
#         result_print = results.loc[:,['Abbreviation','TeamName', 'Points']]
#         print(result_print)
#         for driver, point in zip(results['Abbreviation'], results['Points']):
#             if driver not in points.keys():
#                 if type(point) is float:
#                     points[driver] = point
#             else:
#                 if type(point) is float:
#                     points[driver] += point
#             # print(f'{driver} - {points}')
#     rounds.append(dict(points))


# Write the contents of the rounds data to a .json file
# with open('/Users/emiran/MyDocuments/newTrialTracksider/rounds_data.json', 'w') as file:
#     json.dump(rounds, file)

plt.style.use('dark_background')
plt.rc('ytick', labelsize=22)

# Get the points for the latest round (the last dictionary in the list)
with open('/Users/emiran/MyDocuments/The Tracksiders Gen/rounds_data.json', 'r') as file:
    rounds = json.load(file)

latest_round = rounds[-1]

# Sort drivers based on the total points in the latest round and get the top 10 drivers
top_10_drivers = sorted(latest_round.keys(), key=lambda d: latest_round[d], reverse=True)[:10]

# Create a dictionary to store points for each driver over the rounds (only for top 10 drivers)
driver_points = {driver: [] for driver in top_10_drivers}

# Populate driver points for each round (only for top 10 drivers)
for race_round in rounds:  # Skip the empty first entry
    for driver in top_10_drivers:
        driver_points[driver].append(race_round.get(driver, 0))  # Add 0 if the driver doesn't have points in that round

# Define a color map for the top 10 drivers (can use named colors or hex codes)
driver_colors = {
    'VER': (0/255, 55/255, 115/255, 1.0),
    'PER': (255/255, 204/255, 0/255, 1.0),
    'SAI': (0/255, 165/255, 81/255, 1.0),
    'LEC': (239/255, 26/255, 45/255, 1.0),
    'RUS': (2/255, 115/255, 115/255, 1.0),
    'NOR': (245/255, 118/255, 52/255, 1.0),
    'HAM': (4/255, 191/255, 173/255, 1.0),
    'PIA': (161/255, 221/255, 237/255, 1.0),
    'ALO': (3/255, 89/255, 80/255, 1.0),
    'STR': (255/255, 254/255, 253/255, 1.0)
}

# Plotting
plt.figure(figsize=(10, 6))

# Race rounds (x-axis)
race_rounds = list(range(1, len(rounds) + 1))  # Start from 1 because we skipped the first round

# Plot each driver's total points after each round (only top 10 with colors)
for driver, points in driver_points.items():
    plt.plot(race_rounds, points, marker='o', label=driver, color=driver_colors.get(driver, 'white'), linewidth=6, markersize=10)

plt.xticks(race_rounds)
# Add labels and title
# plt.xlabel('Race Round', fontweight='bold')
plt.ylabel('Total Points', fontweight='bold', fontsize=18)
# plt.title('Total Points for Latest Top 10 Drivers After Each Race Round', fontsize=14, fontweight='bold')

# Add a legend
plt.legend(fontsize=25)

# Add a grid
plt.grid(True, linestyle='--', linewidth=0.3)

# Show the plot
plt.tight_layout()
plt.show()

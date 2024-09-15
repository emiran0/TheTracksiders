import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import ScalarFormatter, FuncFormatter
from fastf1 import plotting
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

session = ff1.get_session(2023, 'Azerbaijan', 'R')
session.load()

ff1.plotting.setup_mpl(mpl_timedelta_support=True)

plot_setup = {
    'driver1': 'HAM',
    'driver2': 'VER',
    'driver3': 'NOR',
    'driver4': 'LEC',
    'driver_nums': [44, 1, 4, 16],
    'driver_abbrv': ['HAM', 'VER', 'NOR', 'LEC']
}


driver1_style1 = plotting.get_driver_style(identifier=plot_setup['driver1'],style=['color'],session=session)
driver2_style1 = plotting.get_driver_style(identifier=plot_setup['driver2'],style=['color'],session=session)
driver3_style1 = plotting.get_driver_style(identifier=plot_setup['driver3'],style=['color'],session=session)
driver4_style1 = plotting.get_driver_style(identifier=plot_setup['driver4'],style=['color'],session=session)

plot_styles = [driver1_style1, driver2_style1, driver3_style1, driver4_style1]

# Load the data
with open ('/Users/emiran/MyDocuments/The Tracksiders Gen/data/Azerbaijan/f1_race_results_3.csv') as f:
    race_0 = pd.read_csv(f)

with open ('/Users/emiran/MyDocuments/The Tracksiders Gen/data/Azerbaijan/f1_race_results_1.csv') as f:
    race_1 = pd.read_csv(f)

with open ('/Users/emiran/MyDocuments/The Tracksiders Gen/data/Azerbaijan/f1_race_results_2.csv') as f:
    race_2 = pd.read_csv(f)

with open ('/Users/emiran/MyDocuments/The Tracksiders Gen/data/Azerbaijan/results.csv') as f:
    race_3 = pd.read_csv(f)

drivers = race_3['No'].tolist()
# Create a dataframe with driver no and position
driver_positions = {2019: [], 2021: [], 2022: [], 2023: []}
appendObject = {}

for index, row in race_0.iterrows():
    appendObject = {'No': row['No'], 'Position': index, 'Points': row['Pts']}
    if appendObject['No'] in drivers:
        driver_positions[2019].append(dict(appendObject))
for index, row in race_1.iterrows():
    appendObject = {'No': row['No'], 'Position': index, 'Points': row['Pts']}
    if appendObject['No'] in drivers:
        driver_positions[2021].append(dict(appendObject))
for index, row in race_2.iterrows():
    appendObject = {'No': row['No'], 'Position': index, 'Points': row['Pts']}
    if appendObject['No'] in drivers:
        driver_positions[2022].append(dict(appendObject))
for index, row in race_3.iterrows():
    appendObject = {'No': row['No'], 'Position': index, 'Points': row['Pts']}
    if appendObject['No'] in drivers:
        driver_positions[2023].append(dict(appendObject))


        # Calculate average points and positions for each driver
average_stats = {}

for driver_no in plot_setup['driver_nums']:
    total_points = 0
    total_positions = 0
    count = 0
    
    for year in driver_positions:
        for record in driver_positions[year]:
            if record['No'] == driver_no:
                total_points += record['Points']
                total_positions += record['Position']
                count += 1
    
    if count > 0:
        average_points = total_points / count
        average_position = total_positions / count
    else:
        average_points = 0
        average_position = 0
    
    average_stats[driver_no] = {
        'average_points': average_points,
        'average_position': average_position
    }

# Print the average statistics
for driver_no, stats in average_stats.items():
    print(f"Driver {driver_no}: Average Points = {stats['average_points']}, Average Position = {stats['average_position']}")

plt.style.use('dark_background')
plt.rc('ytick', labelsize=14)
plt.rc('xtick', labelsize=14)
plt.figure(figsize=(20, 12))

plotting_drivers = {}

for driver_no in plot_setup['driver_nums']:
    points_2019 = [x['Points'] for x in driver_positions[2019] if x['No'] == driver_no]
    points_2021 = [x['Points'] for x in driver_positions[2021] if x['No'] == driver_no]
    points_2022 = [x['Points'] for x in driver_positions[2022] if x['No'] == driver_no]
    points_2023 = [x['Points'] for x in driver_positions[2023] if x['No'] == driver_no]
    plotting_drivers[driver_no] = [points_2019[0], points_2021[0], points_2022[0], points_2023[0]]

# Plot the points for the specified driver number
for idx, num in enumerate(plot_setup['driver_nums']):
    # Plot the points for the specified driver number
    plt.plot([2019, 2021, 2022, 2023], plotting_drivers[num], label=plot_setup['driver_abbrv'][idx], **plot_styles[idx], marker='o', markersize=12, linewidth=3)

plt.xlabel('Year', fontsize=18, fontweight='bold')
plt.ylabel('Points', fontsize=18, fontweight='bold')
plt.grid(True, which="both", ls="--", linewidth=0.2)
plt.legend(fontsize=28)

# Ensure x-axis has integer values
plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
plt.tight_layout()
plt.show()
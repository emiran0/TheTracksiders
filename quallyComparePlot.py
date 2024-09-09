import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker

# Enable cache to speed up loading
# ff1.Cache.enable_cache('/Users/emiran/Library/Caches/fastf1', force_renew=False, use_requests_cache=True)

DriverNums = ['16', '1']
TeamColors = {'McLaren': (245/255, 118/255, 52/255, 1.0),
              'RedBull': (0/255, 55/255, 115/255, 1.0),
              'Ferrari': (239/255, 26/255, 45/255, 1.0)}
plt_title = 'Speed vs Time Comparison with Sector Pass Points (Qualification)'

# Load the session (2024 season, Monza GP, Qualifying session)
session = ff1.get_session(2024, 'Belgium', 'Q')
session.load()

# Function to fetch lap telemetry and sector pass points for a driver
def fetch_lap_telemetry(driver_number):
    # Get the fastest lap for the driver
    lap = session.laps.pick_driver(driver_number).pick_fastest()
    
    # Get the telemetry for the lap
    telemetry = lap.get_telemetry()
    
    # Normalize time to start from 0 and keep it in seconds
    # telemetry['Time'] = telemetry['Date'] - telemetry['Date'].iloc[0]  # Subtract the first timestamp
    # telemetry['Time'] = telemetry['Time'].dt.total_seconds()  # Convert to seconds

    # Get the times for sector pass points
    sector1_end = (lap['Sector1SessionTime'].total_seconds() - lap['LapStartTime'].total_seconds()) * 1e9 # End of sector 1
    sector2_end = (lap['Sector2SessionTime'].total_seconds() - lap['LapStartTime'].total_seconds()) * 1e9 # End of sector 2
    lap_end = lap['LapTime'].total_seconds()  # End of the lap (sector 3 end)

    return telemetry, sector1_end, sector2_end, lap_end

# Fetch telemetry and sector times for Driver 1 (e.g., Verstappen's number is '1')
telemetry_driver1, sector1_end_driver1, sector2_end_driver1, lap_end_driver1 = fetch_lap_telemetry(DriverNums[0])

# Fetch telemetry and sector times for Driver 2 (e.g., Hamilton's number is '44')
telemetry_driver2, sector1_end_driver2, sector2_end_driver2, lap_end_driver2 = fetch_lap_telemetry(DriverNums[1])

# Down-sample telemetry data to reduce the number of points plotted (e.g., take every 5th point)
# downsample_factor = 5
# telemetry_driver1 = telemetry_driver1.iloc[::downsample_factor, :]
# telemetry_driver2 = telemetry_driver2.iloc[::downsample_factor, :]
plt.style.use('dark_background')
plt.rc('ytick', labelsize=14)
plt.rc('xtick', labelsize=14)
plt.figure(figsize=(16, 9))

# Plot Speed vs Time for Driver 1
plt.plot(telemetry_driver1['Time'], telemetry_driver1['Speed'], label='Leclerc', color=TeamColors['Ferrari'], linewidth=3)

# Plot Speed vs Time for Driver 2
plt.plot(telemetry_driver2['Time'], telemetry_driver2['Speed'], label='Verstappen', color='blue', linewidth=3)

plt.axvline(x=sector1_end_driver1, color=TeamColors['Ferrari'], linestyle='--', alpha=0.7, label='Leclerc Sector 1')
plt.axvline(x=sector2_end_driver1, color=TeamColors['Ferrari'], linestyle='-.', alpha=0.7, label='Leclerc Sector 2')

plt.axvline(x=sector1_end_driver2, color='blue', linestyle='--', alpha=0.7, label='Verstappen Sector 1')
plt.axvline(x=sector2_end_driver2, color='blue', linestyle='-.', alpha=0.7, label='Verstappen Sector 2')

# Use a custom x-axis formatter to make the labels more readable without changing the underlying data
def time_formatter(x, pos):
    # Display the time normally but in a reduced format (e.g., 10.2 instead of large numbers)
    return f'{x/1e9:.2f}'  # Keep 1 decimal place

plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(time_formatter))


# Add labels and title
plt.xlabel('Time (s)', fontweight='bold', fontsize=16)
plt.ylabel('Speed (km/h)', fontweight='bold', fontsize=16)
# plt.title('Speed vs Time Comparison with Sector Pass Points (Qualification)', fontsize=14, fontweight='bold')

# Add a legend
plt.legend(fontsize=15)

# Add a grid
plt.grid(True, which="both", ls="--", linewidth=0.2)

# Show the plot
plt.tight_layout()
plt.show()

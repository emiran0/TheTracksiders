import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from fastf1 import plotting

# Your initial plot setup
plot_setup = {
    'driver1': 'PIA',
    'driver2': 'LEC',
    'driver1_num': '81',
    'driver2_num': '16',
    'session_year': 2024,
    'session_round': 'Baku',
    'session_type': 'R',
    'lap_slice_start': 40,
    'lap_slice_end': 51
}

lap_range = range(plot_setup['lap_slice_start'], (plot_setup['lap_slice_end'] + 1))

# Set up matplotlib for FastF1 telemetry data
ff1.plotting.setup_mpl(mpl_timedelta_support=True)
ff1.Cache.offline_mode(enabled=True)

# Load session and drivers' laps
session = ff1.get_session(plot_setup['session_year'], plot_setup['session_round'], plot_setup['session_type'])
session.load()

driver1_laps = session.laps.pick_drivers(plot_setup['driver1'])
driver2_laps = session.laps.pick_drivers(plot_setup['driver2'])

driver1_last_n_laps = driver1_laps.pick_laps(lap_range)
driver2_last_n_laps = driver2_laps.pick_laps(lap_range)

telemetry = driver1_last_n_laps.get_telemetry().add_driver_ahead()
telemetry_data = telemetry.loc[telemetry['DriverAhead'] == plot_setup['driver2_num']]

# Set up the first plot (Distance to driver ahead)
fig1, ax1 = plt.subplots(figsize=(16, 9))
driver1_style1 = plotting.get_driver_style(identifier=plot_setup['driver1'], style=['color'], session=session)

# Initial empty line to be updated during the animation
line1, = ax1.plot([], [], **driver1_style1, label=plot_setup['driver1'], linewidth=3)

# Set axis labels and formatting for the first figure
ax1.set_xlabel('Lap', fontweight='bold', fontsize=16)
ax1.set_ylabel('Distance (m)', fontweight='bold', fontsize=16)
ax1.legend(fontsize=16)
ax1.grid(True, which="both", ls="--", linewidth=0.2)

dist_x_data = np.linspace(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'], num=telemetry_data.shape[0])

# Animation function for the first plot
def animate1(i):
    x_data1 = dist_x_data[:i]
    y_data1 = telemetry_data['DistanceToDriverAhead'][:i]
    line1.set_data(x_data1[:i], y_data1)
    
    ax1.set_xlim(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'])
    ax1.set_ylim(telemetry_data['DistanceToDriverAhead'].min(), telemetry_data['DistanceToDriverAhead'].max())
    
    return line1,

# Set up the first animation
anim1 = FuncAnimation(fig1, animate1, frames=telemetry_data.shape[0], interval=10, blit=True)

# Set up the second plot (Lap times)
fig2, ax2 = plt.subplots(figsize=(16, 9))
driver1_style2 = plotting.get_driver_style(identifier=plot_setup['driver1'], style=['color', 'marker'], session=session)
driver2_style1 = plotting.get_driver_style(identifier=plot_setup['driver2'], style=['color', 'marker'], session=session)

# Initial empty lines for the second figure
line2, = ax2.plot([], [], **driver1_style2, label=plot_setup['driver1'], linewidth=3)
line3, = ax2.plot([], [], **driver2_style1, label=plot_setup['driver2'], linewidth=3)

# Set axis labels and formatting for the second figure
ax2.set_xlabel('Lap', fontweight='bold', fontsize=16)
ax2.set_ylabel('Time (s)', fontweight='bold', fontsize=16)
ax2.legend(fontsize=16)
ax2.grid(True, which="both", ls="--", linewidth=0.2)

# Custom formatter for lap times
def format_lap_time(x, pos):
    formatted_time = mdates.num2date(x).strftime('%M:%S.%f')[:-3]
    return formatted_time

ax2.yaxis.set_major_formatter(plt.FuncFormatter(format_lap_time))

# Animation function for the second plot
def animate2(i):
    lap_range_data = list(lap_range)[:i]
    y_data2 = driver1_last_n_laps['LapTime'][:i]
    y_data3 = driver2_last_n_laps['LapTime'][:i]
    
    line2.set_data(lap_range_data, y_data2)
    line3.set_data(lap_range_data, y_data3)
    
    ax2.set_xlim(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'])
    ax2.set_ylim(min(driver1_last_n_laps['LapTime'].min(), driver2_last_n_laps['LapTime'].min()), 
                 max(driver1_last_n_laps['LapTime'].max(), driver2_last_n_laps['LapTime'].max()))

    return line2, line3

# Set up the second animation
anim2 = FuncAnimation(fig2, animate2, frames=len(lap_range), interval=500, blit=True)

# Display the separate figures
plt.show()


# import fastf1 as ff1
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from matplotlib.ticker import ScalarFormatter, FuncFormatter
# from fastf1 import plotting
# import matplotlib.dates as mdates
# import matplotlib.ticker as ticker

# plot_setup = {
#     'driver1': 'PIA',
#     'driver2': 'LEC',
#     'driver1_num': '81',
#     'driver2_num': '16',
#     'session_year': 2024,
#     'session_round': 16,
#     'session_type': 'R',
#     'lap_slice_start': 40,
#     'lap_slice_end': 53
# }

# lap_range = range(plot_setup['lap_slice_start'], (plot_setup['lap_slice_end'] + 1))

# ff1.plotting.setup_mpl(mpl_timedelta_support=True)

# ff1.Cache.offline_mode(enabled=True)

# session = ff1.get_session(plot_setup['session_year'], plot_setup['session_round'], plot_setup['session_type'])
# session.load()

# driver1_laps = session.laps.pick_drivers(plot_setup['driver1'])
# driver2_laps = session.laps.pick_drivers(plot_setup['driver2'])

# driver1_last_n_laps = driver1_laps.pick_laps(lap_range)
# driver2_last_n_laps = driver2_laps.pick_laps(lap_range)

# telemetry = driver1_last_n_laps.get_telemetry().add_driver_ahead()
# print(telemetry.loc[:,['Time']])

# telemetry_data = telemetry.loc[telemetry['DriverAhead'] == plot_setup['driver2_num']]
# # plt.figure(figsize=(10, 6))
# plt.style.use('dark_background')

# plt.rc('ytick', labelsize=14)
# plt.rc('xtick', labelsize=14)
# plt.figure(figsize=(16, 9))

# driver1_style1 = plotting.get_driver_style(identifier=plot_setup['driver1'],style=['color'],session=session)
# driver1_style2 = plotting.get_driver_style(identifier=plot_setup['driver1'],style=['color', 'marker'],session=session)

# driver2_style1 = plotting.get_driver_style(identifier=plot_setup['driver2'],style=['color', 'marker'],session=session)

# plt.subplot(2, 1, 1)
# plt.plot(np.linspace(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'], num=telemetry_data.shape[0]), telemetry_data['DistanceToDriverAhead'], label=plot_setup['driver1'], **driver1_style1, linewidth=3)
# plt.xticks(
#     ticks=np.linspace(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'], len(lap_range)),  # 14 evenly spaced tick positions for laps 40 to 53
#     labels=lap_range
# )
# plt.xlabel('Lap', fontweight='bold', fontsize=16)
# plt.ylabel('Distance (m)', fontweight='bold', fontsize=16)
# plt.legend(fontsize=16)
# plt.grid(True, which="both", ls="--", linewidth=0.2)

# plt.subplot(2, 1, 2)
# plt.plot(lap_range, driver1_last_n_laps['LapTime'], **driver1_style2, label=plot_setup['driver1'], linewidth=3)
# plt.plot(lap_range, driver2_last_n_laps['LapTime'], **driver2_style1, label=plot_setup['driver2'], linewidth=3)

# def format_lap_time(x, pos):
#     # Convert datetime to string
#     formatted_time = mdates.num2date(x).strftime('%M:%S.%f')[:-3]  # Removes extra milliseconds digits
#     return formatted_time

# # Apply custom formatter to y-axis
# plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
# plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_lap_time))

# # plt.gca().yaxis.set_major_formatter(FuncFormatter(format_lap_time))
# # plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%M:%S.%f'))
# # plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))  
# # plt.plot(last_n_laps.index, last_n_laps['LapTime'], label='Lap Time', color='orange')
# plt.xlabel('Lap', fontweight='bold', fontsize=16)
# plt.ylabel('Time (s)', fontweight='bold', fontsize=16)
# # plt.title('Lap Time')
# # plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
# # plt.gca().ticklabel_format(style='plain', axis='both')
# plt.grid(True, which="both", ls="--", linewidth=0.2)

# plt.legend(fontsize=16)

# plt.tight_layout()
# plt.show()
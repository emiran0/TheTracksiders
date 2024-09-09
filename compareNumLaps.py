import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import ScalarFormatter, FuncFormatter
from fastf1 import plotting
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

plot_setup = {
    'driver1': 'PIA',
    'driver2': 'LEC',
    'driver1_num': '81',
    'driver2_num': '16',
    'session_year': 2024,
    'session_round': 16,
    'session_type': 'R',
    'lap_slice_start': 40,
    'lap_slice_end': 53
}

lap_range = range(plot_setup['lap_slice_start'], (plot_setup['lap_slice_end'] + 1))

ff1.plotting.setup_mpl(mpl_timedelta_support=True)

ff1.Cache.offline_mode(enabled=True)

session = ff1.get_session(plot_setup['session_year'], plot_setup['session_round'], plot_setup['session_type'])
session.load()

driver1_laps = session.laps.pick_drivers(plot_setup['driver1'])
driver2_laps = session.laps.pick_drivers(plot_setup['driver2'])

driver1_last_n_laps = driver1_laps.pick_laps(lap_range)
driver2_last_n_laps = driver2_laps.pick_laps(lap_range)

telemetry = driver1_last_n_laps.get_telemetry().add_driver_ahead()
print(telemetry.loc[:,['Time']])

telemetry_data = telemetry.loc[telemetry['DriverAhead'] == plot_setup['driver2_num']]
# plt.figure(figsize=(10, 6))
plt.style.use('dark_background')

plt.rc('ytick', labelsize=14)
plt.rc('xtick', labelsize=14)
plt.figure(figsize=(16, 9))

driver1_style1 = plotting.get_driver_style(identifier=plot_setup['driver1'],style=['color'],session=session)
driver1_style2 = plotting.get_driver_style(identifier=plot_setup['driver1'],style=['color', 'marker'],session=session)

driver2_style1 = plotting.get_driver_style(identifier=plot_setup['driver2'],style=['color', 'marker'],session=session)

plt.subplot(2, 1, 1)
plt.plot(np.linspace(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'], num=telemetry_data.shape[0]), telemetry_data['DistanceToDriverAhead'], label=plot_setup['driver1'], **driver1_style1, linewidth=3)
plt.xticks(
    ticks=np.linspace(plot_setup['lap_slice_start'], plot_setup['lap_slice_end'], len(lap_range)),  # 14 evenly spaced tick positions for laps 40 to 53
    labels=lap_range
)
plt.xlabel('Lap', fontweight='bold', fontsize=16)
plt.ylabel('Distance (m)', fontweight='bold', fontsize=16)
plt.legend(fontsize=16)
plt.grid(True, which="both", ls="--", linewidth=0.2)

plt.subplot(2, 1, 2)
plt.plot(lap_range, driver1_last_n_laps['LapTime'], **driver1_style2, label=plot_setup['driver1'], linewidth=3)
plt.plot(lap_range, driver2_last_n_laps['LapTime'], **driver2_style1, label=plot_setup['driver2'], linewidth=3)

def format_lap_time(x, pos):
    # Convert datetime to string
    formatted_time = mdates.num2date(x).strftime('%M:%S.%f')[:-3]  # Removes extra milliseconds digits
    return formatted_time

# Apply custom formatter to y-axis
plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(format_lap_time))

# plt.gca().yaxis.set_major_formatter(FuncFormatter(format_lap_time))
# plt.gca().yaxis.set_major_formatter(mdates.DateFormatter('%M:%S.%f'))
# plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))  
# plt.plot(last_n_laps.index, last_n_laps['LapTime'], label='Lap Time', color='orange')
plt.xlabel('Lap', fontweight='bold', fontsize=16)
plt.ylabel('Time (s)', fontweight='bold', fontsize=16)
# plt.title('Lap Time')
# plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
# plt.gca().ticklabel_format(style='plain', axis='both')
plt.grid(True, which="both", ls="--", linewidth=0.2)

plt.legend(fontsize=16)

plt.tight_layout()
plt.show()
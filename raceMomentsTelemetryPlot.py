import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from fastf1 import plotting
import os

plot_setup = {
    'driver1': 'VER',
    'driver1_num': '1',
    'session_year': 2023,
    'sesssion_type': 'S',
    'session_round': 'Baku',
    'moment_lap': 1  
}

session = ff1.get_session(plot_setup['session_year'], plot_setup['session_round'], plot_setup['sesssion_type'])
session.load()

ff1.plotting.setup_mpl(mpl_timedelta_support=True)

driver1_moment_lap = session.laps.pick_drivers(plot_setup['driver1_num']).pick_laps(plot_setup['moment_lap'])
driver1_moment_lap_telemetry = driver1_moment_lap.get_telemetry()

# print(driver1_moment_lap_telemetry.loc[:, ['Time', 'Throttle', 'Brake']])

driver1_style = plotting.get_driver_style(identifier=plot_setup['driver1'], style=['color'], session=session)

time_array = driver1_moment_lap_telemetry['Time'].dt.total_seconds().to_numpy()
throttle_array = driver1_moment_lap_telemetry['Throttle'].to_numpy()
brake_array = driver1_moment_lap_telemetry['Brake'].to_numpy()

data_points = time_array.shape[0]
total_frames = 30 * 110
x_interp = np.interp(np.linspace(0, data_points, total_frames), np.arange(data_points), time_array)
y1_interp = np.interp(np.linspace(0, data_points, total_frames), np.arange(data_points), throttle_array)
y2_interp = np.interp(np.linspace(0, data_points, total_frames), np.arange(data_points), brake_array)

fig, ax = plt.subplots(figsize=(16, 9))

line1, = ax.plot([], [], **driver1_style, label=plot_setup['driver1'] + ' Throttle', linewidth=3)
line2, = ax.plot([], [], color=(255/255, 255/255, 0/255, 1.0), label=plot_setup['driver1'] + ' Brake', linewidth=3)

ax.set_xlim(time_array.min(), time_array.max() + 2)
ax.set_ylim(0, 100)

ax.set_xlabel('Time (s)', fontsize=20, fontweight='bold')
ax.set_ylabel('Throttle/Brake (%)', fontsize=20, fontweight='bold')

def update(frame):
    line1.set_data(x_interp[:frame], y1_interp[:frame])
    line2.set_data(x_interp[:frame], y2_interp[:frame])
    return line1, line2

ani = FuncAnimation(fig, update, frames=total_frames, interval=1000/30, blit=True)
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()






import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from fastf1 import plotting
import os

plot_setup = {
    'driver1': 'LEC',
    'driver1_num': '16',
    'driver2': 'PIA',
    'driver2_num': '81',
    'session_year': 2024,
    'sesssion_type': 'Q',
    'session_round': 'Baku'   
}

session = ff1.get_session(plot_setup['session_year'], plot_setup['session_round'], plot_setup['sesssion_type'])
session.load()

ff1.plotting.setup_mpl(mpl_timedelta_support=True)

driver1_fast_lap = session.laps.pick_driver(plot_setup['driver1_num']).pick_fastest()
driver2_fast_lap = session.laps.pick_driver(plot_setup['driver2_num']).pick_fastest()

driver1_fastlap_telemetry = driver1_fast_lap.get_telemetry()
driver2_fastlap_telemetry = driver2_fast_lap.get_telemetry()

driver1_style = plotting.get_driver_style(identifier=plot_setup['driver1'], style=['color'], session=session)
# driver2_style = plotting.get_driver_style(identifier=plot_setup['driver2'], style=[], session=session)

plt.rc('ytick', labelsize=16)
plt.rc('xtick', labelsize=16)
fig, ax = plt.subplots(figsize=(16, 5))

line1, = ax.plot([], [], **driver1_style, label=plot_setup['driver1'], linewidth=3)
# line2, = ax.plot([], [], color=(255/255, 255/255, 0/255, 1.0), label=plot_setup['driver2'], linewidth=3)

driver1_speed_array = driver1_fastlap_telemetry['Throttle'].to_numpy()
driver1_time_array = driver1_fastlap_telemetry['Time'].dt.total_seconds().to_numpy()
print(driver1_time_array.shape)

driver2_speed_array = driver2_fastlap_telemetry['Brake'].to_numpy()
driver2_time_array = driver2_fastlap_telemetry['Time'].dt.total_seconds().to_numpy()
print(driver2_time_array.shape)

data_points_1 = driver1_time_array.shape[0]
data_points_2 = driver2_time_array.shape[0]
total_frames = 30 * 102
x_interp = np.interp(np.linspace(0, data_points_1, total_frames), np.arange(data_points_1), driver1_time_array)
y1_interp = np.interp(np.linspace(0, data_points_1, total_frames), np.arange(data_points_1), driver1_speed_array)

x2_interp = np.interp(np.linspace(0, data_points_2, total_frames), np.arange(data_points_2), driver2_time_array)
y2_interp = np.interp(np.linspace(0, data_points_2, total_frames), np.arange(data_points_2), driver2_speed_array)

ax.set_xlim(driver1_time_array.min(), driver2_time_array.max())
ax.set_ylim(0, driver1_fastlap_telemetry['Throttle'].max() + 1)

ax.set_xlabel('Time (s)', fontsize=20, fontweight='bold')
ax.set_ylabel('Throttle %', fontsize=20, fontweight='bold')

def animate(i):
    line1.set_data(x_interp[:i], y1_interp[:i])
    # line2.set_data(x2_interp[:i], y2_interp[:i])
    return line1,

anim = FuncAnimation(fig, animate, frames=total_frames, interval=1000/30, blit=True)


plt.legend(fontsize=20)
plt.tight_layout()
# plt.show()

output_dir = os.path.join('data', plot_setup['session_round'])
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

file_path = 'data/' + plot_setup['session_round'] + '/' + str(plot_setup['session_year']) + '_' + plot_setup['session_round'] + '_' + plot_setup['sesssion_type'] + '_' + plot_setup['driver1'] +  '_fastlap_throttle_telemetry.mp4'

anim.save(filename=file_path, writer='ffmpeg', fps=30)

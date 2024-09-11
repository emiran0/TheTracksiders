import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
from fastf1 import plotting

plot_setup = {
    'driver1': 'NOR',
    'driver1_num': '4',
    'driver2': 'SAI',
    'driver2_num': '55',
    'session_year': 2024,
    'sesssion_type': 'Q',
    'session_round': 'Monza'   
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
fig, ax = plt.subplots(figsize=(16, 9))

line1, = ax.plot([], [], **driver1_style, label=plot_setup['driver1'], linewidth=3)
# line2, = ax.plot([], [], color=(255/255, 255/255, 0/255, 1.0), label=plot_setup['driver2'], linewidth=3)

driver1_speed_array = driver1_fastlap_telemetry['Speed'].to_numpy()
driver1_time_array = driver1_fastlap_telemetry['Time'].dt.total_seconds().to_numpy()
print(driver1_time_array.shape)

driver2_speed_array = driver2_fastlap_telemetry['Speed'].to_numpy()
driver2_time_array = driver2_fastlap_telemetry['Time'].dt.total_seconds().to_numpy()
print(driver2_time_array.shape)

data_points = driver1_time_array.shape[0]
total_frames = 30 * 79
x_interp = np.interp(np.linspace(0, data_points, total_frames), np.arange(data_points), driver1_time_array)
y1_interp = np.interp(np.linspace(0, data_points, total_frames), np.arange(data_points), driver1_speed_array)

ax.set_xlim(driver1_time_array.min(), driver2_time_array.max() + 2)
ax.set_ylim(50, driver1_fastlap_telemetry['Speed'].max()+10)

ax.set_xlabel('Time (s)', fontsize=20, fontweight='bold')
ax.set_ylabel('Speed (km/h)', fontsize=20, fontweight='bold')

# print(time_array)

def animate(i):
    line1.set_data(x_interp[:i], y1_interp[:i])
    # line2.set_data(driver2_time_array[:i], driver2_speed_array[:i])
    return line1,

anim = FuncAnimation(fig, animate, frames=total_frames, interval=1000/30, blit=True)

plt.legend(fontsize=20)
plt.tight_layout()
# plt.show()
anim.save('fastlap_animation.mp4', writer='ffmpeg', fps=30)

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
    'session_year': 2023,
    'sesssion_type': 'R',
    'session_round': 'Baku'   
}

session = ff1.get_session(plot_setup['session_year'], plot_setup['session_round'], plot_setup['sesssion_type'])
session.load()

ff1.plotting.setup_mpl(mpl_timedelta_support=True)

driver1_fast_lap = session.laps.pick_drivers(plot_setup['driver1_num'])

print(driver1_fast_lap.loc[:, ['LapNumber', 'Position', 'LapTime', 'Stint', 'Compound', 'TyreLife']])

print(driver1_fast_lap.pick_box_laps().loc[:, ['LapNumber', 'Position', 'LapTime', 'Stint', 'Compound', 'TyreLife']])

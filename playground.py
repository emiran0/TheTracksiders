import fastf1 as ff1
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

# ff1.Cache.offline_mode(enabled=False)
# for i in range(14,23):

# ff1.Cache.offline_mode(enabled=True)

# for year in range(2018,2023):
session = ff1.get_session(2023, 'Baku', 'R')
session.load(laps=True)
results = session.results
result_print = results.loc[:,['DriverNumber','TeamName', 'Points']]

result_print.to_csv('/Users/emiran/MyDocuments/The Tracksiders Gen/data/Azerbaijan/results.csv', index=False)

# driver1_laps = session.laps.pick_drivers('PIA')
# driver2_laps = session.laps.pick_drivers('LEC')

# driver1_last_n_laps = driver1_laps.pick_laps(40)
# driver2_last_n_laps = driver2_laps.pick_laps(40)

# telemetry = driver1_last_n_laps.get_telemetry()
# telemetry2 = driver2_last_n_laps.get_telemetry()

# print(telemetry.loc[:,['SessionTime', 'X', 'Y', 'Z']])
# print(telemetry2.loc[:,['Time', 'SessionTime', 'X', 'Y', 'Z']])

# schedule = ff1.get_event_schedule(2024)
# print(schedule.loc[1:16,['Location', 'EventName', 'EventFormat']])  


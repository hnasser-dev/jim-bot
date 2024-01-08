import numpy as np
import pandas as pd
import matplotlib
from datetime import datetime
from calplot import calplot


def graph_data(start_dt_local, curr_date_dt_local, all_dates_dt_local):
    print("----------")
    start_dt_local_np64 = np.datetime64(start_dt_local)
    print(start_dt_local_np64)
    curr_date_dt_local_np64 = np.datetime64(curr_date_dt_local)
    print(curr_date_dt_local_np64)
    all_dates_dt_local_np64 = [np.datetime64(dt) for dt in all_dates_dt_local]
    print(all_dates_dt_local_np64)




    # start_dt64 = np.datetime64(int(start_unix), "s")
    # start_dt64_local = np.datetime64(timezone_pytz.localize(start_dt64))

    # dates_dt64 = [np.datetime64(int(date_unix[0]), "s") for date_unix in all_dates_unix]
    # curr_dt64 = np.datetime64(int(curr_date_unix), "s")
    # curr_dt64_local = np.datetime64(timezone_pytz.localize(curr_dt64))
    # print(start_dt64_local, curr_dt64_local)

    # # setting a colourmap for the graphs -- red = no gym day, green = gym day
    # colourmap = matplotlib.colors.ListedColormap(['red', 'green']) # colourmap when the person has attended the gym 2+ times
    # """ I had to add this additional version below because the colormap was bugged when the person attended the gym on the same day they started"""
    # colourmap_single = matplotlib.colors.ListedColormap(['green', 'red']) # colourmap when the person has attended the gym once

    # all_dates = pd.date_range(start=curr_dt64_local, end=curr_dt64_local).to_list()
    # print(all_dates)


    ...
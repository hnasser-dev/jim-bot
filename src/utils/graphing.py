import numpy as np
import pandas as pd
import matplotlib
import tempfile
import discord
from calplot import calplot


def graph_data(start_dt_local, curr_date_dt_local, visit_dates_dt_local, user_name):
    # setting a colourmap for the graphs -- red = no gym day, green = gym day
    colourmap = matplotlib.colors.ListedColormap(['red', 'green'])

    start_dt_local_normalised_np64 = np.datetime64(np.datetime64(start_dt_local), "D")
    curr_date_normalised_np64 = np.datetime64(np.datetime64(curr_date_dt_local), "D")
    visit_dates_normalised_np64 = [np.datetime64(np.datetime64(dt), "D") for dt in visit_dates_dt_local]

    # generates a list of dates with times set to 0:00:00 (24 hr incremements starting from a normalised start time)
    all_dates = pd.date_range(start=start_dt_local_normalised_np64, end=curr_date_normalised_np64).to_list()
    # all gym visits
    visits = pd.Series(1, index=visit_dates_normalised_np64)

    # adding the extra dates in which the user did not attend the gym - assigning these values 0
    for date in all_dates:
        if date not in visits.index: # if the date is not in the visits Series
            visits.at[date] = 0 # add it in and assign its value to 0

    fig, _ = calplot(visits, cmap=colourmap, colorbar=False, dropzero=False, suptitle=f"{user_name}'s Gym Attendance", yearascending=True)  
    with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as temp_graph_file:
        fig.savefig(temp_graph_file, bbox_inches='tight', pad_inches=0.3)
        with open(temp_graph_file.name, 'rb') as image_file:
            picture = discord.File(image_file)
            
    return picture
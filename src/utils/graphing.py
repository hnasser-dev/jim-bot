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

    visit_dates_normalised_np64 = [np.datetime64(np.datetime64(dt), "D") for dt in visit_dates_dt_local] # for all visit dates
    all_dates = pd.date_range(start=start_dt_local_normalised_np64, end=curr_date_normalised_np64).to_list()
    all_dates_series = pd.Series(0, index=all_dates) # series representing ALL dates, from start to end

    for visit_date in visit_dates_normalised_np64:
        if visit_date in all_dates_series.index: # if the user visited on this day
            all_dates_series.at[visit_date] = 1 # mark the visit as a "1"

    with open(f"graph_{user_name}.csv", "w", encoding="utf-8") as csv_file:
        csv_file.write(all_dates_series.to_csv())

    fig, _ = calplot(all_dates_series, cmap=colourmap, colorbar=False, dropzero=False, suptitle=f"{user_name}'s Gym Attendance", yearascending=True)

    with tempfile.NamedTemporaryFile(suffix='.png', delete=True) as temp_graph_file:
        fig.savefig(temp_graph_file, bbox_inches='tight', pad_inches=0.3)
        with open(temp_graph_file.name, 'rb') as image_file:
            picture = discord.File(image_file)
            
    return picture
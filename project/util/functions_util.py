import os
import pandas as pd

import plotly
import plotly.graph_objects as go


def get_liczba_oczekujacych_zlecen(start_date, end_date, daty):
    n_oczekujace = pd.DataFrame(columns=['Data', 'Ilość oczekujących'])
    oczekujace_help = pd.DataFrame(columns=['Data przyjęcia', 'Data realizacji'])
    oczekujace = daty[daty['Data przyjęcia'] != daty['Data realizacji']].reset_index(drop=True)
    date_range = pd.date_range(start_date, end_date)
    for date in date_range:
        oczekujace_help = oczekujace_help[oczekujace_help['Data realizacji']!=date]
        niezrealizowane_date = oczekujace[oczekujace['Data przyjęcia']==date]
        oczekujace_help = pd.concat([oczekujace_help, niezrealizowane_date]).reset_index(drop=True)
        n_oczekujace = pd.concat([n_oczekujace, pd.DataFrame({'Data': [date], 'Ilość oczekujących': [oczekujace_help.shape[0]]})]).reset_index(drop=True)
    return n_oczekujace


def save_html(fig: go.Figure, file_name: str):
    if not os.path.exists("images"):
        os.mkdir("images")

    file_path = os.path.join("images", file_name)
    plotly.io.write_html(fig, file=file_path)

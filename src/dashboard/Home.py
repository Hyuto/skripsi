import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

online = False if (Path(__file__).parents[2] / "data").is_dir() else True

# data directory
if not online:
    data_path = (Path(__file__).parents[2] / "data").as_posix()
else:
    data_path = "https://raw.githubusercontent.com/Hyuto/skripsi/master/data"
    st.info(f"Online mode is on accessing data from main repo at: {data_path}", icon="ℹ️")


def get_df_info(df):
    buffer_info = io.StringIO()
    df.info(buf=buffer_info)
    info = buffer_info.getvalue()
    return info


full_data = pd.concat(
    [
        pd.read_csv(data_path + "/" + x)
        for x in [
            "januari-2021.csv",
            "februari-2021.csv",
            "maret-2021.csv",
            "april-2021.csv",
            "mei-2021.csv",
            "juni-2021.csv",
            "juli-2021.csv",
            "agustus-2021.csv",
            "september-2021.csv",
            "oktober-2021.csv",
            "november-2021.csv",
            "desember-2021.csv",
        ]
    ]
)
full_data["date"] = pd.to_datetime(full_data["date"]).dt.tz_localize(None)
full_data.sort_values(["date"], inplace=True)
sample_data = pd.read_csv(data_path + "/sample-data.csv")


st.markdown(
    """
        # Analisis Emosi Opini Masyarakat Pada Sosial Media Twitter Tentang Vaksin Covid-19 Menggunakan Support Vector Machine

        ![love](https://img.shields.io/badge/Made%20with-🖤-white)
        [![Python](https://img.shields.io/badge/Python-≥3.8-green?logo=python)](https://www.python.org/)
    """
)

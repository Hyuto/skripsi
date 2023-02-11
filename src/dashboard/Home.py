import io
from pathlib import Path

import pandas as pd
import streamlit as st

online = False if (Path(__file__).parents[2] / "data").is_dir() else True

# data directory
if not online:
    data_path = (Path(__file__).parents[2] / "data").as_posix()
else:
    data_path = "https://github.com/Hyuto/skripsi/tree/master/data"
    print(f"Online mode is on accessing data from main repo at: {data_path}")

sample_data = pd.read_csv(data_path + "/sample-data.csv")
buffer_info = io.StringIO()
sample_data.info(buf=buffer_info)
info = buffer_info.getvalue()


st.markdown(
    """
        # Analisis Emosi Opini Masyarakat Pada Sosial Media Twitter Tentang Vaksin Covid-19 Menggunakan Support Vector Machine

        ![love](https://img.shields.io/badge/Made%20with-🖤-white)
        [![Python](https://img.shields.io/badge/Python-≥3.8-green?logo=python)](https://www.python.org/)

        ## Dataset

        Dataset adalah data hasil web scraping twitter pada topik `vaksin covid-19` pada tahun 2021 selama
        12 bulan. Library yang digunakan untuk melakukan scraping adalah [`snscrape`](https://github.com/JustAnotherArchivist/snscrape)
        dengan query yang digunakan untuk pencarian adalah `vaksin (covid OR corona)`. Data dapat diakses
        langsung secara online dengan format link berikut:

        ```
        https://raw.githubusercontent.com/Hyuto/skripsi/master/data/<NAMA FILE>
        ```
    """
)


tab1, tab2 = st.tabs(["🗃 Data", "Info"])
tab1.dataframe(sample_data.head())
tab2.text(info)

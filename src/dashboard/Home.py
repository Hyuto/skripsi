from pathlib import Path

import pandas as pd
import streamlit as st

online = False if (Path(__file__).parents[1] / "data").is_dir() else True

# data directory
if not online:
    data_path = (Path(__file__).parents[1] / "data").as_posix()
else:
    data_path = "https://github.com/Hyuto/skripsi/tree/master/data"
    print(f"Online mode is on accessing data from main repo at: {data_path}")

sample_data = pd.read_csv(data_path + "/sample-data.csv")

st.write("Here's our first attempt at using data to create a table:")
st.dataframe(sample_data.head())

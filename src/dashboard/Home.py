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
    data_path = "https://github.com/Hyuto/skripsi/tree/master/data"
    print(f"Online mode is on accessing data from main repo at: {data_path}")


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

        ## Dataset

        Dataset adalah data hasil web scraping twitter pada topik `vaksin covid-19` pada tahun 2021 selama
        12 bulan. Library yang digunakan untuk melakukan scraping adalah 
        [`snscrape`](https://github.com/JustAnotherArchivist/snscrape) dengan query yang digunakan 
        untuk pencarian adalah `vaksin (covid OR corona)`.
    """
)

tab1, tab2 = st.tabs(["🗃 Data", "Info"])
tab1.dataframe(full_data.head(7))
tab2.text(get_df_info(full_data))

st.markdown(
    """
    Dari hasil proses web scraping media sosial Twitter didapatkan data sebanyak 457993 tweet yang 
    terkait dengan vaksin Covid-19 pada kurun waktu 1 tahun pada tahun 2021.
    
    ## EDA
    
    ### Feature Enginering: Engagement
    
    `engagement` adalah variable yang digenerasi dengan menjumlahkan variable - variable seperti 
    `likes`, `retweet`, dan `reply`. Variable ini memberikan informasi tentang jumlah interaksi 
    yang terdapat dalam sebuah tweet. Variable ini juga dapat menunjukan tingkat ketertarikan 
    user/masyarakat terhadap topik atau bahasan yang ada pada sebuah tweet.

    **Best Engagement**
"""
)

full_data["engagement"] = full_data[["likes", "retweet", "reply"]].sum(axis=1).astype(int)

tab3, tab4 = st.tabs(["Tweet", "User"])
tab3.markdown("Melihat tweet dengan jumlah interaksi terbesar pada topik bahasan vaksin Covid-19.")
tab3.dataframe(
    full_data[["user", "content", "engagement"]]
    .sort_values(["engagement"], ascending=False)
    .head(7)
)
tab3.markdown(
    """
    Dapat dilihat pada table diatas tweet dari user `sdenta` memiliki jumlah interaksi terbesar dan 
    terpaut cukup jauh dari tweet dibuat oleh `Rafiq31058861` yang berada pada peringkat ke 2. 
    Dilihat dari tweet tersebut masyarakat cukup tertarik terhadap topik yang berisi teori kospirasi dari vaksin 
    corona yang belum terbukti keaslian infonya.
"""
)

tab4.markdown("Melihat user dengan jumlah interaksi terbanyak pada topik bahasan vaksin Covid-19.")
tab4.dataframe(
    full_data[["user", "engagement"]]
    .groupby(["user"])
    .sum()
    .sort_values(["engagement"], ascending=False)
    .head(7)
)
tab4.markdown(
    """
    Dapat dilihat dari tabel diatas user `jokowi` yang merupakan official account dari Presiden 
    Republik Indonesia Joko Widodo memiliki tingkat interaksi tertinggi, terlampau cukup jauh dari 
    `sdenta` yang berada pada peringkat ke 2.
"""
)

st.markdown(
    """
    ### Frekuensi Sebaran Tweet
    
    Gambar dibawah menunjukkan timeseries plot terhadap frekuensi tweet pada topik vaksin Covid-19 
    selama tahun 2021.
"""
)
tweet_freq = (
    full_data["date"].dt.floor("d").value_counts().rename_axis("date").reset_index(name="count")
)
fig = px.line(tweet_freq, x="date", y="count")
st.plotly_chart(fig)

# plt.figure(figsize=(8, 5))
# sns.lineplot(x="date", y="count", data=tweet_freq)
# plt.xlabel("Tanggal")
# plt.ylabel("Frekuensi")
# plt.show()

# tweet_freq.sort_values("count", ascending=False).head(5)

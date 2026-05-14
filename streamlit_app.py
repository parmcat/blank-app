import streamlit as st


st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

import pandas as pd
import altair as alt
df = pd.read_parquet("./hk_hospital_wait.parquet", engine="pyarrow")

alt.data_transformers.enable('json')

(alt.Chart(df)
 .mark_rect()
 .encode(x='week:O',
         y='wkday_name:O' 
        ,color=alt.Color('mean(max_wait):Q', scale=alt.Scale(scheme='orangered')))
)

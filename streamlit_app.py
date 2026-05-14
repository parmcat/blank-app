import streamlit as st
import pandas as pd
import altair as alt

st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# Load data
df = pd.read_parquet("./hk_hospital_wait.parquet", engine="pyarrow")

# Enable JSON transformer for larger datasets
alt.data_transformers.enable('json')

# Create and display heatmap
chart = (alt.Chart(df)
    .mark_rect()
    .encode(
        x='week:O',
        y='wkday_name:O',
        color=alt.Color('mean(max_wait):Q', scale=alt.Scale(scheme='orangered'))
    )
    .properties(
        title='Hospital Wait Times by Week and Day',
        width=800,
        height=300
    )
)

st.altair_chart(chart, use_container_width=True)

chart_2 = (alt.Chart(df)
 .mark_rect()
 .encode(x='week:O',
         y='wkday_name:O' 
        ,color=alt.Color('mean(max_wait):Q', scale=alt.Scale(scheme='orangered')))

    .properties(
        title='Hospital Wait Times by Year',
        width=800,
        height=300
    )

).facet(
    row="yr"    )

st.altair_chart(chart_2, use_container_width=True)

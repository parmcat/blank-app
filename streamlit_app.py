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


chart_3 = (alt.Chart(df)
 .mark_rect()
 .encode(x='yearmonthdate(hospital_time):O',
         y='hospital_name:N',
         color=alt.Color('mean(max_wait):Q',
                         scale=alt.Scale(scheme='orangered'),
                         legend=alt.Legend(type='symbol')
                        ),
         tooltip=['mean(max_wait)','hospital_name:N'],
         
        )
)
st.altair_chart(chart_3, use_container_width=True)

##################

selection = alt.selection_single(fields=['hospital_name'],name='Random')

color = alt.condition(selection,
                      alt.value('steelblue'),
                      alt.value('lightgray'))

bar=(alt.Chart(df)
 .mark_bar()
 .encode(y='mean(max_wait):Q',
         x=alt.X('hospital_name:N',
         sort=alt.EncodingSortField(field='max_wait', op='mean', 
                            order='descending')),
         color=color
    
        )
).add_selection(selection)

bar.title ="Mean Waiting Time for Hong Kong's Hospital"
bar.encoding.x.title = 'Hospital'
bar.encoding.y.title = 'Average Waiting Time in Hour(s)'
st.altair_chart(bar, use_container_width=True)

#########################

color2 = alt.condition(selection,
                      alt.Color('hospital_name:N'),
#                       alt.value('steelblue'),
                      alt.value('lightgray'))

line1=(alt.Chart(df)
 .mark_line()
 .encode(x=alt.X('hours(hospital_time):T'),
         y='mean(max_wait):Q',
         color=color2
        
    
        )
)

line1.title ="Waiting Time for Hong Kong's Hospital"
line1.encoding.x.title = 'Hour'
line1.encoding.y.title = 'Average Waiting Time in Hour(s)'

#bar | line1
st.altair_chart(bar | line1, use_container_width=True)


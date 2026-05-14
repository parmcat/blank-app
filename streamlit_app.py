import streamlit as st
import pandas as pd
import altair as alt

st.write(
    "Lab 6 Examples")

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

#################################

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
st.altair_chart(bar , use_container_width=True)

#################################

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
st.altair_chart(bar , use_container_width=True)
######################################################

st.write("rest of examples not displayed")

st.write("Assignment")

# chart 1a 
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['wkday_name'] = pd.Categorical(df['wkday_name'], categories=days_order, ordered=True)

# labels
chart1a = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X('week:O', title='Week of Year'),
        y=alt.Y('wkday_name:O', title='Day of Week'),
        color=alt.Color('mean(max_wait):Q', scale=alt.Scale(scheme='orangered'), title='Average Max Wait Time')
    )
    .properties(
        title='Max Wait Time Adjusted'
    )
).configure_view(stroke=None)

# chart 1b
chart1b = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        x=alt.X('week:O', title='Week of the Year'),
        y=alt.Y('wkday_name:O', title='Day of the Week'),
        color=alt.Color('mean(max_wait):Q', scale=alt.Scale(scheme='orangered'), title='Average Max Wait Time')
    )
    .facet(
        row=alt.Row("yr:N", title='Year')
    )
    .properties(
        title='Max Wait Time Adjusted'
    )
).configure_view(stroke=None)
st.altair_chart(chart1a , use_container_width=True)

st.altair_chart(chart1b , use_container_width=True)

###########################

merged_df = df.groupby(['hospital_name', 'hospital_time']).agg({'max_wait': 'mean'}).reset_index()

# merge rows for hospitals and removed hospital name
chart2 = (
    alt.Chart(merged_df)
    .mark_rect()
    .encode(
        x=alt.X('yearmonthdate(hospital_time):O', title='Date'),
        y=alt.Y('hospital_name:N', title='Hospital'),
        color=alt.Color(
            'mean(max_wait):Q',
            scale=alt.Scale(scheme='orangered'),
            title='Average Max Wait Time'
        ),
        tooltip=['mean(max_wait):Q']  
    )
    .properties(
        title='Average Max Wait Time Per Hospital'
    )
    .configure_view(stroke=None)
)

st.altair_chart(chart2 , use_container_width=True)

############################

# 3a, redone for error-handling
# updated section 3 code to use 'use_params' because I was getting errors

selection = alt.selection_point(
    fields=['hospital_name'],
    name='Hospital Selection',
    bind='legend'
)

color = alt.condition(selection,
                      alt.value('steelblue'),
                      alt.value('lightgray'))

bar = (alt.Chart(df)
       .mark_bar()
       .encode(
           y='mean(max_wait):Q',
           x=alt.X('hospital_name:N', 
                    sort=alt.EncodingSortField(field='max_wait', op='mean', order='descending')),
           color=color
       )
       .add_params(selection) 
       .properties(title="Mean Waiting Time for Hong Kong's Hospitals")
)

bar.encoding.x.title = 'Hospital'
bar.encoding.y.title = 'Average Waiting Time in Hour(s)'

# 3b:
color2 = alt.condition(selection,
                       alt.Color('hospital_name:N', scale=alt.Scale(scheme='set1')),
                       alt.value('lightgray'))

line1 = (alt.Chart(df)
         .mark_line()
         .encode(
             x=alt.X('hours(hospital_time):T', title="Hour"),
             y='mean(max_wait):Q',
             color=color2
         )
         .add_params(selection)  
         .properties(title="Waiting Time for Hong Kong's Hospitals")
)

line1.encoding.y.title = 'Average Waiting Time in Hour(s)'

# 3c
line2 = (alt.Chart(df)
         .mark_line()
         .encode(
             x=alt.X('yearmonthdate(hospital_time):T', title='Date'),
             y='mean(max_wait):Q',
             color=color2
         )
         .transform_filter(selection)  # line plot filtered by selection
         .properties(title="Average Waiting Time in 1 Day for Hong Kong's Hospitals")
)

line2.encoding.y.title = 'Average Waiting Time in Hour(s)'

# 3d
final_chart = alt.hconcat(
    bar,
    line1,
    line2,
    spacing=10
).resolve_scale(color='independent')  # color scales

final_chart
st.altair_chart(final_chart , use_container_width=True)

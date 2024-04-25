import pandas as pd
# import string
import streamlit as st
import plotly.express as px

def load_data_yearly():
    penguin_file = st.file_uploader("Select Your Local yearly CSV file")
    if penguin_file is None:
        st.stop()
    # Create a new column 'Name_Count' to store the counts
    year_data = pd.read_csv(penguin_file)
    # col_names = senti_df.columns.tolist()
    # senti_df[col_names[0]] = senti_df[col_names[0]].map(lambda x: x[:3].strip().replace(".","") if x[0].isdigit() else x)
    # print(senti_df[col_names[0]])
    return year_data

year_df = load_data_yearly()

options = st.multiselect(
    'Which question you want to analyze',
    year_df.iloc[:,0].unique().tolist())

year_df_col_names = year_df.columns.tolist()
if options:
    year_df = year_df[year_df[year_df_col_names[0]].isin(options)]
fig = px.line(year_df, x=year_df_col_names[1], y=year_df_col_names[2], color=year_df_col_names[0], title='Daily Average Demand by Location')
fig.update_layout(xaxis_title='Date', yaxis_title='Average Demand')
st.plotly_chart(fig)
# fig.show()
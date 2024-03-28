import pandas as pd
# import string
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def load_data_senti():
    penguin_file = st.file_uploader("Select Your Local sentiment CSV file")
    if penguin_file is None:
        st.stop()
    # Create a new column 'Name_Count' to store the counts
    senti_df = pd.read_csv(penguin_file)
    # col_names = senti_df.columns.tolist()
    # senti_df[col_names[0]] = senti_df[col_names[0]].map(lambda x: x[:3].strip().replace(".","") if x[0].isdigit() else x)
    # print(senti_df[col_names[0]])
    return senti_df

def plotly_bar_senti_func(formated_sent_df,col_names):
    # questions = formated_sent_df[col_names[0]].map(lambda x: x[:3].strip().replace(".","") if x[0].isdigit() else x)
    questions = formated_sent_df.index.tolist()
    print(questions)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=questions,
        hoverinfo = "all",
        y=formated_sent_df[col_names[1]].tolist(),
        name=col_names[1],
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=questions,
        hoverinfo = "all",
        y=formated_sent_df[col_names[2]].tolist(),
        name=col_names[2],
        marker_color='MediumPurple'
    ))
    fig.add_trace(go.Bar(
        x=questions,
        hoverinfo = "all",
        y=formated_sent_df[col_names[3]].tolist(),
        name=col_names[3],
        marker_color='DarkSlateGrey'
    ))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)#,template="plotly_dark")
    return fig

senti_df = load_data_senti()
senti_df_col_names = senti_df.columns.tolist()
if ('sentidf_key' not in st.session_state):# or st.session_state.sentidf_key > 0:
    st.session_state.sentidf_key = 1
# st.session_state.sentidf_key += 1
if st.button("Reset bellow dataframe", type="primary"):
    st.session_state.sentidf_key += 1
    print(f"Session state updated. New key: {st.session_state.sentidf_key}")
tab4, tab5 = st.tabs(["Data Frame Sentiment Analysis","Histogram Chart"])
with tab4:
    senti_edited_data = st.data_editor(senti_df.reset_index(), num_rows="dynamic",key=f'df_{st.session_state.sentidf_key}',use_container_width=st.session_state.use_container_width)
with tab5:
    senti_bar_plt = plotly_bar_senti_func(senti_edited_data,senti_df_col_names)
    st.plotly_chart(senti_bar_plt)
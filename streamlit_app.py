import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime


st.set_page_config(layout='wide', initial_sidebar_state="collapsed")


@st.cache_data(ttl=1800)  # Cache data for 30 min
def load_data():
    data_path = pd.read_excel(f"datasources/output.xlsx")
    df = pd.DataFrame(data_path)
    return df

# Load data
df = load_data()


st.title('Items Movement Data')

# GroupName filter
with st.sidebar.expander("Groups"):
    group_names = df['GroupName'].unique()
    if "group_select_all" not in st.session_state:
        st.session_state.group_select_all = True

    group_select_all = st.checkbox("Select / Unselect All", value=st.session_state.group_select_all, key=1)
    if group_select_all:
        selected_group_names = st.multiselect("", options=group_names, default=group_names)
        st.session_state.group_select_all = True
    else:
        selected_group_names = st.multiselect("", options=group_names)
        st.session_state.group_select_all = False

    filtered_df = df[df['GroupName'].isin(selected_group_names)]

# StoreName filter
with st.sidebar.expander("Stores"):
    store_names = filtered_df['StoreName'].unique()
    if "store_select_all" not in st.session_state:
        st.session_state.store_select_all = True

    store_select_all = st.checkbox("Select / Unselect All", value=st.session_state.store_select_all, key=2)
    if store_select_all:
        selected_store_names = st.multiselect("", options=store_names, default=store_names)
        st.session_state.store_select_all = True
    else:
        selected_store_names = st.multiselect("", options=store_names)
        st.session_state.store_select_all = False

    filtered_df = filtered_df[filtered_df['StoreName'].isin(selected_store_names)]

# Filter by Date Range
date_range = st.sidebar.date_input("Date Range", value=[df['Date'].min().date(), df['Date'].max().date()], key='date_range')
if len(date_range) == 2:
    start_date, end_date = date_range
    # Convert to datetime64 for comparison
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

# Display filtered data
st.dataframe(filtered_df, )

# Use st.table for a static table without sorting options
# st.table(df)

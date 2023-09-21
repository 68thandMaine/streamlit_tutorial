import streamlit as st
import pandas as pd
import numpy as np
from src.constants import DATA_URL, DATE_COLUMN

st.title("Uber pickups in NYC")

@st.cache_data
def load_data(nrows: int):
  data = pd.read_csv(DATA_URL, nrows=nrows)
  lowercase = lambda x: str(x).lower()
  data.rename(lowercase, axis='columns', inplace=True)
  data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
  return data


data_load_state = st.text("loading data")
data = load_data(1000)
data_load_state.text('Done! (using st.cache_data)')

st.subheader('Number of pickups by the hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

st.subheader("Map of all pickups")
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)

st.slider('hour', 0, 23, 17)
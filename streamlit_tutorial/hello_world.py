import streamlit as st
import pandas as pd
import numpy as np

left_column, right_column = st.columns(2)

def highlight_table(data):
    if data is not None:
        st.dataframe(data.style.highlight_max(axis=0))

def draw_tables():
    df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

    st.write("Here's the first attempt at using data to create a table")
    st.write(df)

    st.write("Here's a table using Numpy")
    dataframe = pd.DataFrame(
        np.random.randn(10, 20), columns=[f"col {i}" for i in range(20)]
    )
    st.write(dataframe)

    st.write("Here's a table with highlighted maximum values:")
    highlight_table(dataframe)

def draw_line():
    st.write("Here's the first attempt at using data to create a line chart")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)

def draw_map():
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=["lat", "lon"]
    )
    st.map(map_data)

def draw_slider_widget():
  x = st.slider('x')
  st.write(x, 'squared is', x*x)

def draw_button_widget():
  btn = st.button('I"m a button')
  st.write(btn)
  
def draw_widget_by_key():
  st.text_input("your name", key="name")

def show_data():
  if st.checkbox('show session state'):
    st.session_state


draw_slider_widget()
draw_button_widget()
draw_widget_by_key()
show_data()



with left_column:
  draw_tables()
  
with right_column:
    draw_map()
    draw_line()
Streamlit provides custom widgets that allow users to interact with data. Here are some of the basic widgets:

- `st.slider()`
- `st.button()`
- `st.selectbox()`

After defining your widget, you can use the write method to add it to the DOM.

```bash
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)
```

!!! Remember that every time a user interacts with the widget, Streamlit will rerun the entire python script from top to bottom.

You can add keys to widgets to make them unique and bind them to session state data.

```python
import streamlit as st
st.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name
```

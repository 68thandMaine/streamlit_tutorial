Streamlit has a few API's for building a layout. The most common layout apis are the `st.sidebar()`, the `st.expander()` , and the `st.columns()`.

The sidebar api will create a left aligned vertical space in the DOM. Everything that is passed to `st.sidebar()` will be pinned to the left. `st.expander()` helps us conserve space by hiding large content, and `st.columns()` allows us to place widgets side by side.

```python

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")
```

---

## Layout API

| Description                                      | API             |
| ------------------------------------------------ | --------------- |
| Create a left-aligned vertical space in the DOM. | `st.sidebar()`  |
| Create an expander to hide large content.        | `st.expander()` |
| Create columns to place widgets side by side.    | `st.columns()`  |

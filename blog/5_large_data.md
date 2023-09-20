Oftentimes we will find ourselves needing to manage computationally expensive or long lasting calls to get data. To avoid refetching this data, Streamlit has the concept of caching results. This will allow the app to stay performant when loading data from the web, manipulating large datasets, or performing expensive computations.

To enable caching on a function, Streamlit provides two decorators: `@st.cache_data` and `@st.cache_resource`. Usually we use `@st.cache_data` when we need to cache computations that return data such as loading a DataFrame from CSV, transforming a NumPy array, querying an API, or any other function that returns a serializable data object (str, int, float, DataFrame, array, list, …). `@st.cache_resource` is great for caching global resources such as ML models or database connections. Essentially we use this to cache unserializable objects we don't want to load multiple times.

One tip to improve the UX of long running operations before their results are cached is to use `st.progress()` to display the status of an operation in real time.

```python
'Starting a long computation...'
# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)
```

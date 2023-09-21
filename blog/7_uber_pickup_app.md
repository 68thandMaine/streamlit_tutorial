In this tutorial, we will create an interactive app that allows you to explore the public Uber dataset for pickups and drop-offs in New York City. We'll start by setting up the main infrastructure of the app. This involves creating two essential directories: app/src/ and app/pages. The src directory will contain constant data and utility functions, while the app directory will house our Streamlit code.

Since this tutorial is part of a larger repository dedicated to exploring Streamlit features, we'll organize our app using pages. Let's begin by creating a new file in the pages/ directory and naming it 2_uber_pickups.py. This file will serve as a page in the app's sidebar. Don't forget to activate your Poetry shell and set your IDE interpreter to the Poetry environment for seamless development.

Now, let's give our app a title:

```python
st.title("Uber pickups in NYC")
```

Next, we'll need to fetch the Uber dataset. To do this, we'll require two key components:

1. A file to store constant data.
2. A function to fetch the data.

In your terminal, navigate to the project directory and execute the following command to create a constants.py file under the src/ directory:

```bash
$ touch app/src/constants.py`
```

Then in the `uber_pickup.py` file create a method that will load the data.

```python
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
```

<details>
  <summary> You can open this for a line by line explanation of this function</summary>

1. `data = pd.read_csv(DATA_URL, nrows=nrows)` -This line downloads the dataset from the provided URL. You can use pd.read_csv with either a local path or a URL. It also specifies the number of rows to read, which is essential for handling large files.
2. `lowercase = lambda x: str(x).lower()` - Use a lambda function to convert strings to lowercase. Lambda functions are typically used for simple operations where a full function definition is not required.
3. `data.rename(lowercase, axis='columns', inplace=True)` - This code renames the columns to lowercase for consistency.
4. `data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])` - Convert the date column to a datetime format.
5. Apply the @st.cache_data decorator to the function to instruct Streamlit to cache the results of this API call.

</details>

Now, let's use this method to load the data and store it in a variable called `data`:

```python

data = load_data(1000)
```

The data variable now contains the first 1000 rows of the dataset, thanks to the argument passed to the load_data function.

### Creating Visualizations for the Data

We can display the downloaded data as both a histogram and as a map. The histogram will help us understand the busiest times, while the map will show us the locations with the most pickups in the city.

Creating both of these elements is remarkably straightforward. Streamlit seamlessly integrates with various mapping libraries. In this tutorial, we'll use the Streamlit API st.bar_chart() to build the histogram. First, we need to sort our data. We can use NumPy's histogram function for this:

```python

hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

st.bar_chart(hist_values)
```

To create the map, we'll use the st.map() function to overlay the data on a map of New York City. Based on the histogram, it seems that 10:00 is the busiest time for Uber pickups. Let's create a function to redraw our map and display the concentration of pickups at 10:00:

```python

hour_to_filter = 10
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.map(filtered_data)
```

To make our application more interactive, we'll let users select the busiest pickup hour themselves. We can achieve this by using the st.slider() widget, providing users with a way to manually choose the time:

```python

st.slider('Select Hour', 0, 23, 10)
```

This slider widget enhances user engagement and makes the app more user-friendly.

That's it! In future posts we will enhance this app, but for now you should know enough about the basics of Streamlit to get started.

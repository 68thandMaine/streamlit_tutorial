After setting up our repository for the Streamlit tutorial with Python Poetry there are a few things to learn about Streamlit. The fist is how to run a Streamlit app:

> `poetry run streamlit run your_script.py [-- script args]`

Note that we are using the `poetry run` command to tell Poetry to look to our virtual environment for the dependencies needed to run this command.

Much like a frontend framework, Streamlit has a concept of hotreloading. In a nutshell - Streamlit can detect changes to your code and will rerun the script to update the DOM. It is important to note that anytime something is updated Streamlit will run the entire Python script from top to bottom. This means that the app will be rerun when users interact with widgets within the app.

Streamlit provides several API methods to display data in the DOM. The most common is `st.write()` which can be used to write anything from text to tables! We can also write without calling Streamlit methods directly. This is called a "magic command. Anytime that Streamlit sees a variable or literal on it's own line, it will automatically write the result to the DOM. Along with magic commands, st.write() is Streamlit's "Swiss Army knife". You can pass almost anything to st.write(): text, data, Matplotlib figures, Altair charts, and more.

Here are some popular APIs we can use:

| Description                                 | API               |
| ------------------------------------------- | ----------------- |
| Draw a line chart                           | `st.line_chart()` |
| Plot a map                                  | `st.map()`        |
| Static table generation                     | `st.table()`      |
| Write an interactive table with a dataframe | `st.dataframe()`  |

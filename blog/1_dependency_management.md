There are several dependency management solutions available in the Python environment. Personally, I prefer using [Python Poetry](https://python-poetry.org/) because it closely resembles package management in frontend projects, both in its command-line interface (CLI) and in how it manages dependencies across different environments.

To initiate a repository with Poetry, simply execute the following command:

```bash
poetry new <project_name>
```

This command sets up the fundamental structure of a Poetry project. Most notably, it generates the `pyproject.toml` file, which plays a central role in orchestrating the project and its dependencies.

To add dependencies to a Poetry project, use the following command:

```bash
poetry add <package_name>
```

Since this mini blog follows the Streamlit tutorial, we will install the dependencies required for that tutorial. Start by adding Streamlit:

```bash
poetry add streamlit
```

While Streamlit's documentation suggests using `.venv` to manage virtual environments, there's a slight variation when working with a Poetry project. Both `.venv` and Poetry create virtual environments to isolate project-specific packages from global ones. To execute a script with Poetry, it's necessary to prefix the command with `poetry run`. Poetry can detect and respect existing virtual environments that have been activated, but you can also activate the virtual environment explicitly by running `poetry shell`.

Once the environment has been activated, you no longer need to prefix commands with `poetry run`.

If you are using VSCode, you might need to set your interpreter to the virtual environment that Poetry has created. You can do this by finding the path for the Poetry environment with `poetry env info --path`. Copy the path, use it to point the VSCode python interpreter to the poetry virtual environment.

- Open your project in Visual Studio Code.
- Go to the "File" menu and select "Preferences," then "Settings."
- In the settings, search for "Python Path".

OR if you are on a Mac

- cmd + shift + p
- type Python Select Interpreter

---

## CLI Commands Used

| Command                     | Description                                                                                    |
| --------------------------- | ---------------------------------------------------------------------------------------------- |
| `poetry new <project_name>` | Initializes a new Poetry project by creating the basic project structure and `pyproject.toml`. |
| `poetry add <package_name>` | Adds a Python package as a dependency to your Poetry project.                                  |
| `poetry run`                | Prefixes a command to run it within the context of the Poetry project's virtual environment.   |
| `poetry shell`              | Activates the Poetry project's virtual environment, allowing you to work within it directly.   |

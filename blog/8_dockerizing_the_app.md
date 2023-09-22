[Reference article](https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0)

Docker is a great tool for collaboration and setting up isolated environments for a tool to run. There are many ways to configure your Dockerfile, but oftentimes what you will see in tutorials is simplistic and can lead to large Docker images. This tutorial borrows directly from [this article](https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0) to provide an example of an optimized Dockerfile that works with Poetry.

One of the most annoying things that can happen when automating builds is having a dependency update without your knowledge, and it break your application. Poetry is susceptible to this, so let's start by planning to pin the Poetry version.

> `RUN pip install poetry==1.11.1`

We also will **only need to copy data that is needed to build a production app**. Unfortunately Poetry does not like projects without a `README.md`, so we will create an empty `README.md` in our Docker environment

> `COPY pyproject.toml poetry.lock ./`

> `COPY app/ ./app`

> `RUN touch README.md`

Let's also **aim to avoid installing development dependencies** in our Docker environment. Poetry has a nice way of building projects without development dependencies with the command `poetry install --without dev`

> `RUN poetry install --without dev`

Poetry caches downloaded packages so they can be reused during future install commands. This is not needed in a production Docker build, so we will delete the poetry cache dir.

Before doing this, lets set some environment variables in our Dockerfile.

```docker
ENV POETRY_NO_INTERACTION=1
    POETRY_VIRTUALENVS_IN_PROJECT=1
    POETRY_VIRTUALENVS_CREATE=1
    POETRY_CACHE_DIR=/tmp/poetry_cache
```

What exactly do all these do?

- `POETRY_NO_INTERACTION=1`: Do not ask any interactive question. [link](https://python-poetry.org/docs/configuration/#virtualenvscreate)
- `POETRY_VIRTUALENVS_IN_PROJECT=1`: Create the virtualenv inside the projects root directory. [link](https://python-poetry.org/docs/configuration/#virtualenvsin-project)
- ` POETRY_VIRTUALENVS_CREATE=1`: Create a new virtual environment if one does not already exist. [link](https://python-poetry.org/docs/configuration/#virtualenvscreate)
- `POETRY_CACHE_DIR=/tmp/poetry_cache`: Override the default Poetry cache dir. [link](https://python-poetry.org/docs/configuration/#cache-directory)

> Creating a virtual environment inside a Docker container is purely a preferential task. Doing so will make sure that the poetry environment is as isolated as possible, and the installation of this Dockerfile will not mess with the system version of python or poetry.

Now we can remove any caching in our Docker container after we install poetry:

> `RUN poetry install --without dev && rm -rf $POETRY_CACHE_DIR`

Our Dockerfile copies code needed by Poetry to install the project before we issue the command `RUN poetry install`. Due to Docker's layer caching everytime the `COPY` layer is invalidated we have to rebuild the subsequent layers.

> Docker layer caching (DLC) is beneficial if building Docker images is a regular part of your CI/CD process. DLC saves Docker image layers created within your jobs, and caches them to be reused during future builds.

We can provide Poetry with just enough information to build the virtual environment and copy our codebase later by using the `--no-root` flag. This flag tells Poetry to skip installing the current project into the virtual environment.

We also will move the `COPY` command to be run **after** we run `poetry install`.

```docker
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY app/ ./app
```

We can also add an optional command to install the project in the virtual environment.

```docker
...

COPY app/ ./app

RUN poetry install --without dev
```

At this point we have a Dockerfile that results in fast builds, but the size of the image is rather large. We can continue to optimize this by adding multi-stage builds. Essentially we select different base images for different jobs in the Docker container.

One approach is to use larger images that have development dependencies to install virtual environments, and smaller images to simply run the application. We can pass information from one stage to another in multi-stage builds.

Is Poetry needed at runtime? Not really because it's a dependency management tool so we can simply copy the virtual environment from the build step into our runtime.

---

#### Putting it all together, here's our Dockerfile looks like this:

```Docker
# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

RUN pip install poetry==1.11.1

ENV POETRY_NO_INTERACTION=1
    POETRY_VIRTUALENVS_IN_PROJECT=1
    POETRY_VIRTUALENVS_CREATE=1
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY app/ ./app

ENTRYPOINT ["poetry", "run", "streamlit", 'run', "app/Streamlit_Tutorial.py"]

```

<details>
  <summary>Line by line breakdown of Dockerfile (AI Generated)</summary>

| Code                                                                            | Explanation                                                                                                                                 | WHY (Developer's Perspective)                                                                       |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `FROM python:3.11-buster as builder`                                            | Specifies the base image for the builder stage, which will be used to build the virtual environment.                                        | Starting with a Python base image sets up our development environment.                              |
| `RUN pip install poetry==1.11.1`                                                | Installs Poetry version 1.11.1 using pip in the builder stage.                                                                              | We need Poetry to manage our project's dependencies and virtual environments.                       |
| `ENV POETRY_NO_INTERACTION=1`                                                   | Sets the environment variable `POETRY_NO_INTERACTION` to `1`, indicating non-interactive mode for Poetry.                                   | Avoids prompts during dependency resolution; it's automated for CI/CD.                              |
| `POETRY_VIRTUALENVS_IN_PROJECT=1`                                               | Sets the environment variable `POETRY_VIRTUALENVS_IN_PROJECT` to `1`, enabling virtual environments within the project.                     | Ensures that virtual environments are created within our project directory.                         |
| `POETRY_VIRTUALENVS_CREATE=1`                                                   | Sets the environment variable `POETRY_VIRTUALENVS_CREATE` to `1`, allowing Poetry to create virtual environments.                           | Grants Poetry the ability to generate isolated environments for our project.                        |
| `POETRY_CACHE_DIR=/tmp/poetry_cache`                                            | Sets the path for Poetry's cache directory to `/tmp/poetry_cache`.                                                                          | Poetry uses this cache for faster dependency resolution; we can clear it later to save space.       |
| `WORKDIR /app`                                                                  | Sets the working directory inside the container to `/app`.                                                                                  | Our project's source code and files will be managed within this directory.                          |
| `COPY pyproject.toml poetry.lock ./`                                            | Copies the `pyproject.toml` and `poetry.lock` files from the host into the container's `/app` directory.                                    | We're adding our project's dependency configuration to the container.                               |
| `RUN touch README.md`                                                           | Creates an empty `README.md` file in the container's working directory.                                                                     | A placeholder for our project's documentation; we can add content later.                            |
| `RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR`        | Uses Poetry to install project dependencies (excluding development dependencies) and then removes the Poetry cache to reduce image size.    | It's like setting up our project's library, and we're tidying up afterward to keep the image small. |
| `FROM python:3.11-slim-buster as runtime`                                       | Specifies the base image for the runtime stage, which will be used to run the code with the virtual environment.                            | Preparing a lightweight environment to execute our application.                                     |
| `ENV VIRTUAL_ENV=/app/.venv`                                                    | Sets the path to the virtual environment directory within the `/app` directory.                                                             | This is where our Python environment will reside, isolated from the host system.                    |
| `PATH="/app/.venv/bin:$PATH"`                                                   | Adds the virtual environment's bin directory to the `PATH` environment variable.                                                            | Makes sure our Python interpreter and dependencies are accessible.                                  |
| `COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}`                             | Copies the virtual environment from the builder stage to the runtime stage.                                                                 | We're transferring the isolated Python environment we built earlier.                                |
| `COPY app/ ./app`                                                               | Copies the contents of the `app/` directory from the host into the container's `/app` directory.                                            | Bringing in our application code and assets for execution.                                          |
| `ENTRYPOINT ["poetry", "run", "streamlit", 'run', "app/Streamlit_Tutorial.py"]` | Sets the entry point command for the container, which runs the specified Streamlit application using Poetry within the virtual environment. | This is where our application kicks off, leveraging Poetry and Streamlit for execution.             |

</details>

---

## Docker build mantras

- Keep layers small, minimizing the amount of stuff you copy and install in it
- Exploit Docker layer caching and reduce cache misses as much as possible
- Slow-changing things (project dependencies) must be built before fast-changing things (application code)
- Use Docker multi-stage builds to make your runtime image as slim as possible

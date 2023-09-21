Streamlit can parse a directory structure for specific names. One of the directory names is
called `pages/` and any `.py` file listed within this directory will be added as a new page
in the app. The new pages are accessible via options in the sidebar

To create a multipage app we need a single "entrypoint". The entrypoint file will appear as the
topmost page in the sidebar. After that, we can add `.py` files to the `pages/` directory and
the rest is up to you.

Here are some tips and tricks for creating pages:

- Filenames are composed of four different parts:

  1. A number — if the file is prefixed with a number.
  2. A separator — could be \_, -, space, or any combination thereof.
  3. A label — which is everything up to, but not including, .py.
  4. The extension — which is always .py.

- Use capitalized filenames so they appear capitalized in the sidebar.

It's important to note that Pages share the same Python modules globally and the same session state.

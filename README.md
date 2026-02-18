# ACStreamlit

A demo and template project for building **Streamlit apps** that run directly inside **Archicad** – powered by [Tapir](https://github.com/ENZYME-APD/tapir-archicad-automation).

The app is rendered in a standalone native window via [pywebview](https://pywebview.flowrl.com/) and communicates with Archicad through the Tapir interface.

---

## Features

- **Modular architecture** – Each module lives in its own folder under `modules/` with its own Streamlit UI.
- **Easy to extend** – Create a new module folder, copy and adjust the `entry_point.py` – done.
- **Native GUI** – Streamlit runs in the background; the UI is displayed in a native window via pywebview.
- **Archicad integration** – Execute Tapir commands directly from your Streamlit app through `ac_funcs/aclib`.

---

## Project Structure

```
ACStreamlit/
├── entry_point.py              # Entry point – launches a specific module
├── run_module.py               # Launcher: Streamlit server + pywebview window
├── config_example.json         # Example Tapir configuration
├── pyproject.toml
├── LICENSE                     # MIT
│
├── ac_funcs/                   # Helper functions for Archicad communication
│   ├── aclib/                  # Tapir / Archicad JSON Command API
│   └── get_selected_elements.py
│
└── modules/
    └── MyModule/               # Example module
        ├── __init__.py
        └── ui.py               # Streamlit UI for this module
```

---

## Prerequisites

- **Python ≥ 3.13**
- **Archicad** with the [Tapir Add-On](https://github.com/ENZYME-APD/tapir-archicad-automation) installed
- Dependencies (managed via `pyproject.toml`):
  - `streamlit`
  - `pywebview`
  - `archicad`
  - `watchdog`

---

## Installation

```bash
# Clone the repository
git clone https://github.com/fertegi/ACStreamlit.git
cd ACStreamlit

# Create a virtual environment & install dependencies (e.g. with uv)
uv sync
```

---

## Usage

### Running a Module

Each module has its own `entry_point.py`. To run the included example module:

```bash
python entry_point.py
```

This starts a Streamlit server in the background and opens a pywebview window displaying the app. When the window is closed, the server is automatically shut down.

### Creating Your Own Module

1. **Create a new folder** under `modules/`, e.g. `modules/MyNewModule/`.
2. **Add a `ui.py`** in the new folder – this is the Streamlit UI:

   ```python
   import streamlit as st
   from ac_funcs.get_selected_elements import get_selected_elements

   st.header("My New Module")

   if st.button("Get Elements"):
       elements = get_selected_elements()
       for elem in elements:
           st.write(elem)
   ```

3. **Copy `entry_point.py`** (or create a new one) and point it to your module:

   ```python
   import run_module
   from pathlib import Path

   st_filepath = Path(__file__).parent / "modules/MyNewModule/ui.py"
   st_port = 8501
   window_config = {
       "window_title": "My New Module",
       "url": f"http://localhost:{st_port}",
       "width": 400,
       "height": 800,
       "on_top": True,
       "resizable": True,
       "streamlit_file": str(st_filepath),
       "streamlit_port": st_port,
   }

   run_module.main(**window_config)
   ```

4. **Run it** with `python entry_point.py` (or your new entry point).

---

## Dependency Management
Dependencies are managed via `pyproject.toml` using [uv](https://pypi.org/project/uv/). But in some cases you might want to use inline declarations in the entry_point files. In that case, make sure to also add the dependencies to `pyproject.toml` to keep everything in sync.

```
# /// script
# requires-python = ">=3.13"
# dependencies = [
#    "archicad>=28.3000",
#    "pywebview>=5.4",
#    "streamlit>=1.47",
# ]
# ///
```

## Configuration (Tapir)

The file `config_example.json` shows how to register a module with Tapir:

```json
{
    "repositories": [
        {
            "repoOwner": "fertegi",
            "repoName": "ACStreamlit",
            "relativeLoc": "",
            "displayName": "MyModule",
            "includePattern": "entry_point",
            "excludePattern": "",
            "excludeFromDownloadPattern": ""
        }
    ],
    "askUpdatingAddOnBeforeEachExecution": true
}
```

---

## Contributing

Pull requests from the community are welcome! Whether it's bug fixes, or improvements – feel free to open a PR.

---

## License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

**No warranty.** The software is provided "as is", without warranty of any kind.

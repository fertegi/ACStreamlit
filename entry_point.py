# /// script
# requires-python = ">=3.13"
# dependencies = [
#    "archicad>=28.3000",
#    "pywebview>=5.4",
#    "streamlit>=1.47",
# ]
# ///
import run_module
from pathlib import Path

st_filepath = Path(__file__).parent / "modules/MyModule/ui.py"
st_port = 8501
window_config = {
    "window_title": "My Streamlit App",
    "url": f"http://localhost:{st_port}",
    "width": 400,
    "height": 800,
    "on_top": True,
    "resizable": True,
    "streamlit_file": str(st_filepath),
    "streamlit_port": st_port,
}

run_module.main(**window_config)

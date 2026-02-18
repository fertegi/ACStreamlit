from typing import Any, Dict, List
import streamlit as st
from ac_funcs.get_selected_elements import get_selected_elements

st.set_page_config(
    page_title="My Streamlit App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("Welcome to My Module")
st.write("""
         Hello, this small app demonstrates the capabilities of a Archicad - Tapir - Streamlit - Workflow!
         """)


def on_click() -> List[Dict[str, Any]]:
    ac_elements = get_selected_elements()
    return ac_elements


AC_ELEMENTS = []

btn = st.button("Get Selected Elements",
                type="primary", width="stretch")
if btn:
    AC_ELEMENTS = get_selected_elements()
    st.write("Selected Elements:")
    for elem in AC_ELEMENTS:
        st.write(f"- :green[{elem.get("elementId").get("guid")}]")

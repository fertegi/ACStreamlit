from typing import Any, Dict, List
import streamlit as st
from ac_funcs.utils import get_selected_elements, get_property_values, set_aclib_port


ELEMENT_ID_PROP_ID = {
    "propertyId": {
        "guid": "7E221F33-829B-4FBC-A670-E74DABCE6289"
    }
}

st.set_page_config(
    page_title="My Streamlit App",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("Welcome to My Module")
st.write("""
         Hello, this small app demonstrates the capabilities of a Archicad - Tapir - Streamlit - Workflow!
         """)


selected_port = st.text_input("Enter your port number. Default is 19723",
                              value="19723", key="port_input", help="In order to communicate with Archicad we need to specify the correct port number. You can get the port number, if you click on 'About Tapir' in the Tapir menu in Archicad.")

set_aclib_port(int(selected_port))

AC_ELEMENTS = []

get_selected_elements_btn = st.button("Get Selected Elements",
                                      type="primary", width="stretch")
if get_selected_elements_btn:
    AC_ELEMENTS = get_selected_elements()
    st.write("Selected Elements:")
    guids = [g.get("elementId", {}).get("guid") for g in AC_ELEMENTS]
    st.table({"Guids": guids})


get_elementIds_btn = st.button(
    "Get Element IDs", type="primary", width="stretch")
if get_elementIds_btn:
    AC_ELEMENTS = get_selected_elements()
    if not AC_ELEMENTS:
        st.warning(
            "No elements selected. Please select some elements in Archicad and try again.")
    else:
        st.write("Element IDs for the following elements:")
        values = get_property_values(AC_ELEMENTS, [ELEMENT_ID_PROP_ID])
        guids = [g.get("elementId", {}).get("guid") for g in AC_ELEMENTS]
        values = [v.get("propertyValues", [])[0].get(
            "propertyValue", {}).get("value") for v in values]
        values = {"Element ID": values, "Guids": guids}
        st.write("**Element IDs as table:**")
        st.table(values)
        st.write("**Element IDs as json:**")
        st.json(values)

import streamlit as st
import json


def json_uploader():
    st.subheader("Upload Meta Data in JSON Format")
    with st.form("Upload JSON"):
        uploaded_file = st.file_uploader("Upload JSON", type=["json"])
        submit_button = st.form_submit_button("Submit")

        if uploaded_file is not None and submit_button:
            try:
                file_contents = uploaded_file.read()
                return file_contents
            except json.JSONDecodeError:
                st.error("Invalid JSON file. Please upload a valid JSON file.")

    return None

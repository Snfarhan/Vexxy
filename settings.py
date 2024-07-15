import streamlit as st
from streamlit_faker import get_streamlit_faker


def settings_page():
    st.title('Settings')
    st.divider()
    
    fake = get_streamlit_faker(seed=42)


    
import streamlit as st
from streamlit_faker import get_streamlit_faker


def notif_page():
    st.title('Notification')
    st.divider()
    
    fake = get_streamlit_faker(seed=42)

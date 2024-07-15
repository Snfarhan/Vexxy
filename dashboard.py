import streamlit as st
from streamlit_faker import get_streamlit_faker


def dashboard_page():
    st.title('Dashboard ')
    st.text('Below is the analysis from noon, amazon and shopify platform')
    st.divider()
    
    fake = get_streamlit_faker(seed=42)
    fake.dataframe(use_container_width = True)
    fake.line_chart()

    st.divider()


    
    
    
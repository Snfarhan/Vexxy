import streamlit as st
from streamlit_faker import get_streamlit_faker

def analysis_page():
    st.title('Analysis')
    st.text('Below is the analysis from noon, amazon and shopify platform')
    st.divider()
    
    fake = get_streamlit_faker(seed=42)
    fake.dataframe(use_container_width = True)
    fake.line_chart()
  

    fake.dataframe(use_container_width = True)
    fake.dataframe(use_container_width = True)

    fake.dataframe(use_container_width = True)

    st.divider()
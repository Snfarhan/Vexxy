import streamlit as st
from pymongo import MongoClient
import bcrypt
import pandas as pd
import duckdb as db
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from streamlit_option_menu import option_menu
from noon import noon_page
from amazon import amazon_page
from shopify import shopify_page
from dashboard import dashboard_page
from analysis import analysis_page
from notification import notif_page
from settings import settings_page

st.set_page_config(layout="wide")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db1 = client['user_auth_db']
users_collection = db1['users']

# Hashing function
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Verify password function
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)

# Login function
def login_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and verify_password(user['password'], password):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password")

# Dashboard function
def dashboard():
    st.sidebar.header(f"Hello, {st.session_state['username']}!")
    with st.sidebar:
        selected = option_menu(None,["Dashboard", "Analysis","Noon","Amazon","Shopify","Notification","Settings"], 
                               icons=['house-door-fill','bar-chart-line-fill','cart-fill','amazon','bag-fill','bell-fill','gear-fill'],
                               orientation="vertical",
                               styles={"container":{"background-color":"#282434"}})

        
    page_names_to_funcs = {
        "Dashboard" : dashboard_page,
        "Analysis" : analysis_page,
        "Noon": noon_page,
        "Amazon" : amazon_page,
        "Shopify" : shopify_page,
        "Notification" : notif_page,
        "Settings" : settings_page
    }

    page_names_to_funcs[selected]()
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False   
# Main app
def main():
    st.logo("vextera_logo.png")  # Replace with an image if desired

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        dashboard()
    else:
        st.subheader("Login")

        username = st.text_input("Email Address")
        password = st.text_input("Password", type="password")

        if st.button("Log in"):
            login_user(username, password)
            if st.session_state['logged_in']:
                return

if __name__ == '__main__':
    main()
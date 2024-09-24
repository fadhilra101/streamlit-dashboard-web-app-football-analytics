import streamlit as st
from layouts.navigation import sidebar_navigation
from session import save_selections_to_session  # Import your session management functions
from main import main_page
from shot_analysis import shot_analysis_page  # Import your other pages

# Initialize session state variables if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'main_page'  # Default page

# Initialize selected items
selected_items = {}

# Load the selected page dynamically
if st.session_state.page == 'main_page':
    selected_items = main_page()  # Assume main_page returns selected_items
elif st.session_state.page == 'shot_analysis_page':
    shot_analysis_page()  # Adjust as necessary

# Sidebar navigation with selected_items passed
sidebar_navigation(selected_items)

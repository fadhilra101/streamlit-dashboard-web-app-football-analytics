import streamlit as st
from main import save_selections_to_session

def navigation():
    # Sidebar for navigation
    st.sidebar.title('Navigation')

    # Check the page state
    if 'page' not in st.session_state:
        st.session_state.page = 'main_page'  # Default page

    # Buttons to navigate
    if st.sidebar.button('Main Page'):
        save_selections_to_session()  # Save selections when navigating away
        st.session_state.page = 'main_page'
        st.rerun()

    if st.sidebar.button('Shot Analysis'):
        save_selections_to_session()  # Save selections when navigating away
        st.session_state.page = 'shot_analysis_page'
        st.rerun()

    # Return the selected page
    return st.session_state.page

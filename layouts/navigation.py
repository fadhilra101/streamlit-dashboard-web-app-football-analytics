import streamlit as st
from session import save_selections_to_session

def sidebar_navigation(selected_items):
    st.sidebar.title("Navigation")

    # Create a dictionary to map page names to function names
    pages = {
        "Main Page": "main_page",
        "Shot Analysis": "shot_analysis_page",
        # Add more pages as needed
    }

    # Iterate through the pages and create a button for each
    for page_name, page_key in pages.items():
        if st.sidebar.button(page_name):
            # Check if the selected page is different from the current page
            if 'page' not in st.session_state or st.session_state.page != page_key:
                # Save selections to session state
                save_selections_to_session(selected_items)

            # Set the selected page in session state
            st.session_state.page = page_key
            st.rerun()  # Refresh the app to navigate to the new page

    return st.session_state.page

import streamlit as st
from main import main_page
from shot_analysis import shot_analysis_page

def routing():
    # Cek state halaman
    if 'page' not in st.session_state:
        st.session_state.page = 'main_page'
    
    # Route ke halaman yang sesuai
    if st.session_state.page == 'main_page':
        main_page()
    elif st.session_state.page == 'shot_analysis_page':
        shot_analysis_page()

if __name__ == "__main__":
    routing()

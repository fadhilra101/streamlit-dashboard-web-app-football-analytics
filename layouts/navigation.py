import streamlit as st

def navigation():
    # Atur sidebar untuk navigasi
    st.sidebar.title('Navigation')

    # Cek state halaman
    if 'page' not in st.session_state:
        st.session_state.page = 'main_page'  # Default page

    # Gunakan tombol untuk mengubah halaman
    if st.sidebar.button('Main Page'):
        st.session_state.page = 'main_page'
        st.rerun()
    if st.sidebar.button('Shot Analysis'):
        st.session_state.page = 'shot_analysis_page'
        st.rerun()

    # Return halaman yang terpilih
    return st.session_state.page



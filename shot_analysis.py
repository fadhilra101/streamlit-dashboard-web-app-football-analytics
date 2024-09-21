import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsbombpy import sb
from components.football_pitch import draw_pitch
from main import save_selections_to_session

def shot_analysis_page():
    if st.button('Back'):
        save_selections_to_session()
        st.session_state.page = 'main_page'
        st.rerun()

    st.title('Shot Analysis')

    if 'filtered_df' in st.session_state:
        df = st.session_state.filtered_df
        st.dataframe(df, use_container_width=True)
        # Memanggil fungsi draw_pitch dengan shot scatter
        draw_pitch(df, switch_axes=True)
    else:
        # upload data
        st.write("Your data must be on csv format with this following data: - location (json type with coordinate data)")

        st.write("Upload data:")
        uploaded_file = st.file_uploader("Choose a file")

    
    
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsbombpy import sb
from components.football_pitch import draw_pitch

def shot_analysis_page():
    if st.button('Back'):
        st.session_state.page = 'main_page'
        st.rerun()

    st.title('Shot Analysis')

    if 'filtered_df' in st.session_state:
        df = st.session_state.filtered_df.reset_index(drop=True)
        st.dataframe(df, use_container_width=True)
        # Memanggil fungsi draw_pitch dengan shot scatter
        st.write(st.session_state.selected_fixture_index)
        draw_pitch(df, switch_axes=True)
    else:
        # upload data
        st.write("Your data must be on csv format with this following data: - location (json type with coordinate data)")

        st.write("Upload data:")
        uploaded_file = st.file_uploader("Choose a file")

    
    
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsbombpy import sb
from components.football_pitch import shot_pitch

def shot_analysis_page():
    if st.button('Back'):
        st.session_state.page = 'main_page'
        st.rerun()

    st.title('Shot Analysis')

    if 'filtered_df' in st.session_state:
        df = st.session_state.filtered_df.reset_index(drop=True)
        st.dataframe(df, use_container_width=True)
        # Memanggil fungsi shot_pitch_pitch dengan shot scatter
        st.write(st.session_state.selected_fixture_index)
        shot_pitch(df, switch_axes=True)
    else:
        # upload data
        st.write("Your data must be on ***CSV*** format with this following data: \n - location (json type with coordinate data) / or x and y data \n - shot_end_location (json type with coordinate data) \n - type (string type with shot data)")

        st.warning("*Naming must be the same as the example above or use a similar naming convention.*")

        st.write("Upload data:")
        uploaded_file = st.file_uploader("Choose a file")

    
    
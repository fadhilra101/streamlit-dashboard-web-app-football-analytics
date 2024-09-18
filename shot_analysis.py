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

    filtered_df = st.session_state.filtered_df

    st.dataframe(filtered_df, use_container_width=True)

    # Draw the pitch
    bg_color = '#0E1117'
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(bg_color)
    draw_pitch(pitch_color=bg_color, line_color='lightgrey', ax=ax)
    st.pyplot(fig)
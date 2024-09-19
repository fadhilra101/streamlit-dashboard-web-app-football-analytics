import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
from matplotlib.patches import Arc

def draw_pitch():
    # Membuat figure dan ax untuk pitch
    fig, ax = plt.subplots(figsize=(12, 6))

    # Mengatur warna background figure
    fig.set_facecolor('black')

    # Menggunakan pitch dari mplsoccer
    pitch = VerticalPitch(pitch_color='grass', line_color='white', stripe=True, half=True)  # pitch dengan garis putih dan stripes
    pitch.draw(ax=ax)  # Menggambar pitch di ax

    # Menampilkan plot dengan Streamlit, pastikan untuk memberikan fig sebagai argumen
    st.pyplot(fig)
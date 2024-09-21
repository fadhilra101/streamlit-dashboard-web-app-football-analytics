import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mplsoccer import Pitch, VerticalPitch
from matplotlib.patches import Arc

def process_shot_data(df):
    # Mengonversi kolom menjadi string
    df['location'] = df['location'].astype(str)
    df['shot_end_location'] = df['shot_end_location'].astype(str)

    # Memisahkan x dan y dari 'location'
    def extract_coordinates(loc):
        try:
            # Menghapus karakter tambahan dan memisahkan
            coordinates = loc.strip('[]').split(',')
            return float(coordinates[0]), float(coordinates[1])
        except (ValueError, IndexError):
            return None, None

    df[['x_shot', 'y_shot']] = df['location'].apply(lambda loc: pd.Series(extract_coordinates(loc)))
    df[['x_shot_end', 'y_shot_end']] = df['shot_end_location'].apply(lambda loc: pd.Series(extract_coordinates(loc)))

    # Mengembalikan DataFrame yang sudah diproses
    return df[['x_shot', 'y_shot', 'x_shot_end', 'y_shot_end']]

def draw_pitch(df, shot_color='red', shot_end_color='green', switch_axes=False):

    if ('location' not in df.columns or 
            'shot_end_location' not in df.columns or 
            not (df['type'] == 'Shot').any()):
        st.write('Check Your Data. It Must Be On CSV Format With This Following Data: - location (json type with coordinate data) - shot_end_location (json type with coordinate data) - type (string type with shot data)')

    if ('x_shot' not in df.columns or df['x_shot'].isnull().any() or 
        'y_shot' not in df.columns or df['y_shot'].isnull().any() or 
        'x_shot_end' not in df.columns or df['x_shot_end'].isnull().any() or 
        'y_shot_end' not in df.columns or df['y_shot_end'].isnull().any()):
        process_shot_data(df)


    x_shot = df['x_shot']
    y_shot = df['y_shot']
    x_shot_end = df['x_shot_end']
    y_shot_end = df['y_shot_end']

    # Periksa apakah sumbu perlu diswitch
    if switch_axes:
        x_shot, y_shot = y_shot, x_shot  # Switch axes
        x_shot_end, y_shot_end = y_shot_end, x_shot_end  # Switch axes
        
    # Membuat figure dan ax untuk pitch
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Menggunakan pitch dari mplsoccer
    pitch = VerticalPitch(pitch_type='statsbomb', 
                          pitch_color='grass', line_color='white', 
                          stripe=True, half=True,)
    pitch.draw(ax=ax)

    # Menambahkan scatter plot ke lapangan berdasarkan shot x dan y
    ax.scatter(x_shot, y_shot, color=shot_color, edgecolors='black', zorder=3, label='Shot')
    ax.scatter(x_shot_end, y_shot_end, color=shot_end_color, edgecolors='black', zorder=3, label='Shot End')

    # Menambahkan legend agar lebih jelas
    ax.legend(loc='upper left')
    
    st.pyplot(fig)

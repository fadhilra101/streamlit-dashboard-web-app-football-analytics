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

def shot_pitch(df, shot_color='blue', switch_axes=False):

    if ('location' not in df.columns or 
            'shot_end_location' not in df.columns or 
            not (df['type'] == 'Shot').any()):
        st.write('Check Your Data. It Must Be On CSV Format With This Following Data: - location (json type with coordinate data) - shot_end_location (json type with coordinate data) - type (string type with shot data)')

    if ('x_shot' not in df.columns or df['x_shot'].isnull().any() or 
        'y_shot' not in df.columns or df['y_shot'].isnull().any() or 
        'x_shot_end' not in df.columns or df['x_shot_end'].isnull().any() or 
        'y_shot_end' not in df.columns or df['y_shot_end'].isnull().any()):
        process_shot_data(df)

    # Check for alternative column names
    alternative_columns = [
        ('x', 'y', 'x_end', 'y_end'),
        ('shot_x', 'shot_y', 'shot_end_x', 'shot_end_y'),
        ('start_x', 'start_y', 'end_x', 'end_y')
    ]

    for alt_cols in alternative_columns:
        if all(col in df.columns for col in alt_cols):
            df['x_shot'] = df[alt_cols[0]]
            df['y_shot'] = df[alt_cols[1]]
            df['x_shot_end'] = df[alt_cols[2]]
            df['y_shot_end'] = df[alt_cols[3]]
            break

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
                          stripe=True, half=True)
    pitch.draw(ax=ax)

    # Menambahkan scatter plot ke lapangan berdasarkan shot x dan y
    ax.scatter(x_shot, y_shot, color=shot_color, edgecolors='black', zorder=3, label='Shot', s=200)

    # Menambahkan garis dari shot ke shot_end dan pewarnaan berdasarkan shot_outcome
    if 'shot_outcome' in df.columns:
        for i in range(len(x_shot)):
            outcome = df['shot_outcome'].iloc[i]  # Ambil shot_outcome per baris
            if outcome == 'Goal':
                line_color = '#00FF00'  # Hijau terang
                scatter_color = '#00FF00'  # Hijau terang
            elif outcome == 'Post':
                line_color = 'yellow'
                scatter_color = 'yellow'
            else:
                line_color = 'red'
                scatter_color = 'red'

            # Plot garis dan scatter shot_end sesuai outcome
            ax.plot([x_shot.iloc[i], x_shot_end.iloc[i]], [y_shot.iloc[i], y_shot_end.iloc[i]], 
                    color=line_color, zorder=2, linewidth=3)
            ax.scatter(x_shot_end.iloc[i], y_shot_end.iloc[i], color=scatter_color, edgecolors='black', zorder=3, s=200)
            
            # Jika kolom player ada, tambahkan nama pemain di bawah titik shot
            if 'player' in df.columns:
                player_name = df['player'].iloc[i]
                ax.text(x_shot.iloc[i], y_shot.iloc[i] - 0.025 * max(y_shot), player_name, fontsize=10, color='black', ha='center', zorder=1)

    else:
        # Jika tidak ada shot_outcome, gunakan warna default
        ax.scatter(x_shot_end, y_shot_end, color='red', edgecolors='black', zorder=3, label='Shot End', s=200)
        for i in range(len(x_shot)):
            ax.plot([x_shot.iloc[i], x_shot_end.iloc[i]], [y_shot.iloc[i], y_shot_end.iloc[i]], 
                    color='red', zorder=2, linewidth=3)
            
            # Jika kolom player ada, tambahkan nama pemain di bawah titik shot
            if 'player' in df.columns:
                player_name = df['player'].iloc[i]
                ax.text(x_shot.iloc[i], y_shot.iloc[i] - 0.025 * max(y_shot), player_name, fontsize=10, color='black', ha='center', zorder=1)



    # Menambahkan legend agar lebih jelas
    ax.legend(loc='upper left')
    
    st.pyplot(fig)


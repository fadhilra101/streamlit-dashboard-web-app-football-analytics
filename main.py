import streamlit as st
import numpy as np
import pandas as pd
import time
from statsbombpy import sb

def main_page():
    st.title('Streamlit Web App')
    st.header('Football Match Data from StatsBomb API')

    data = sb.competitions()

    competition_dict = dict(zip(data['competition_name'], data['competition_id']))
    season_dict = dict(zip(data['season_name'], data['season_id']))

    # Seleksi kompetisi
    selected_competition_name = st.selectbox('Select Competition', data['competition_name'].unique(), index=None)
    selected_competition_id = competition_dict.get(selected_competition_name) if selected_competition_name else None

    if selected_competition_id:
        filtered_seasons = data[data['competition_id'] == selected_competition_id]['season_name'].unique()
        selected_season_name = st.selectbox('Select Season', filtered_seasons, index=None)
        selected_season_id = season_dict.get(selected_season_name) if selected_season_name else None

        if selected_season_id:
            # Ambil data pertandingan berdasarkan competition_id dan season_id yang dipilih
            df = sb.matches(competition_id=selected_competition_id, season_id=selected_season_id)
            st.dataframe(df, use_container_width=True)

            # Daftar singkatan yang ingin dipertahankan
            acronyms = ['LFC', 'WFC']

            # Fungsi untuk mengubah format judul, tapi mempertahankan singkatan
            def custom_title_case(word):
                if word.upper() in acronyms:
                    return word.upper()
                return word.title()

            def format_team_name(name):
                return ' '.join(custom_title_case(word) for word in name.split())

            # Terapkan fungsi format_team_name untuk setiap elemen di kolom home_team dan away_team
            fixture_list = df[['home_team', 'away_team']].applymap(format_team_name)

            # Ubah DataFrame menjadi list of tuples
            fixture_list = fixture_list.values.tolist()

            # Tambahkan 'vs' di antara home_team dan away_team
            formatted_fixture_list = [f'{home} vs {away}' for home, away in fixture_list]

            # Buat dictionary untuk menghubungkan fixture dengan match_id
            fixture_dict = {f'{home} vs {away}': match_id for (home, away), match_id in zip(fixture_list, df['match_id'])}

            # Menampilkan selectbox untuk memilih fixture
            selected_fixture = st.selectbox('Select Fixture', formatted_fixture_list, index=None)
            selected_match_id = fixture_dict.get(selected_fixture)

            if selected_match_id:
                # Ambil data pertandingan berdasarkan match_id yang dipilih
                df = sb.events(match_id=selected_match_id)
                
                # Dapatkan semua kolom yang ada di DataFrame
                columns = df.columns.tolist()
                
                # Gunakan multiselect untuk memilih kolom, default semua kolom terpilih
                selected_columns = st.multiselect('Select columns to display:', columns, default=columns)

                # Filter DataFrame berdasarkan kolom yang dipilih
                filtered_df = df[selected_columns]

                # Jika kolom 'player' dipilih, buat selectbox untuk memfilter berdasarkan player
                if 'player' in selected_columns:
                    unique_players = df['player'].dropna().unique().tolist()
                    selected_player = st.selectbox('Select Player', ['All'] + unique_players, index=0)
                    if selected_player != 'All':
                        filtered_df = filtered_df[filtered_df['player'] == selected_player]

                # Jika kolom 'team' dipilih, buat selectbox untuk memfilter berdasarkan team
                if 'team' in selected_columns:
                    unique_teams = df['team'].dropna().unique().tolist()
                    selected_team = st.selectbox('Select Team', ['All'] + unique_teams, index=0)
                    if selected_team != 'All':
                        filtered_df = filtered_df[filtered_df['team'] == selected_team]
                
                # Jika kolom 'type' dipilih, buat selectbox untuk memfilter berdasarkan type
                if 'type' in selected_columns:
                    unique_types = df['type'].dropna().unique().tolist()
                    selected_type = st.selectbox('Select Type', ['All'] + unique_types, index=0)
                    if selected_type != 'All':
                        filtered_df = filtered_df[filtered_df['type'] == selected_type]
                        
                        # Jika type yang dipilih adalah "Shot", tambahkan filter untuk shot_technique dan shot_outcome
                        if selected_type == 'Shot':
                            # Jika kolom 'shot_technique' dipilih, buat selectbox untuk memfilter berdasarkan shot_technique
                            if 'shot_technique' in selected_columns:
                                unique_techniques = df['shot_technique'].dropna().unique().tolist()
                                selected_technique = st.selectbox('Select Shot Technique', ['All'] + unique_techniques, index=0)
                                if selected_technique != 'All':
                                    filtered_df = filtered_df[filtered_df['shot_technique'] == selected_technique]
                            
                            # Jika kolom 'shot_outcome' dipilih, buat selectbox untuk memfilter berdasarkan shot_outcome
                            if 'shot_outcome' in selected_columns:
                                unique_outcomes = df['shot_outcome'].dropna().unique().tolist()
                                selected_outcome = st.selectbox('Select Shot Outcome', ['All'] + unique_outcomes, index=0)
                                if selected_outcome != 'All':
                                    filtered_df = filtered_df[filtered_df['shot_outcome'] == selected_outcome]

                # Tampilkan DataFrame yang sudah difilter
                st.dataframe(filtered_df, use_container_width=True)

      
  
def shot_analysis_page():
  st.title('Shot Analysis')



if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Sidebar untuk navigasi
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Main Page", "Shot Analysis"])

# Tampilkan halaman berdasarkan pilihan
if page == "Main Page":
    main_page()
elif page == "Shot Analysis":
    shot_analysis_page()
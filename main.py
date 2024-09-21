import streamlit as st
import numpy as np
import pandas as pd
from statsbombpy import sb

def save_selections_to_session():
    # Save selections to session state when navigating to another page
    st.session_state.selected_columns = st.session_state.get('temp_selected_columns', [])
    st.session_state.selected_competition_index = st.session_state.get('selected_competition_index', 0)
    st.session_state.selected_season_index = st.session_state.get('selected_season_index', 0)
    st.session_state.selected_fixture_index = st.session_state.get('selected_fixture_index', 0)
    st.session_state.selected_player_index = st.session_state.get('selected_player_index', 0)
    st.session_state.selected_team_index = st.session_state.get('selected_team_index', 0)
    st.session_state.selected_type_index = st.session_state.get('selected_type_index', 0)
    st.session_state.selected_technique_index = st.session_state.get('selected_technique_index', 0)
    st.session_state.selected_outcome_index = st.session_state.get('selected_outcome_index', 0)

def main_page():
    st.title('Streamlit Web App')
    st.header('Football Match Data from StatsBomb API')

    data = sb.competitions()
    competition_dict = dict(zip(data['competition_name'], data['competition_id']))
    season_dict = dict(zip(data['season_name'], data['season_id']))

    # Select competition
    selected_competition_name = st.selectbox('Select Competition', data['competition_name'].unique(), 
                                               index=st.session_state.get('selected_competition_index', 0))

    if selected_competition_name:
        selected_competition_id = competition_dict.get(selected_competition_name)
        st.session_state.selected_competition_index = data['competition_name'].tolist().index(selected_competition_name)

        if selected_competition_id:
            filtered_seasons = data[data['competition_id'] == selected_competition_id]['season_name'].unique()
            selected_season_name = st.selectbox('Select Season', filtered_seasons, 
                                                 index=st.session_state.get('selected_season_index', 0))
            selected_season_id = season_dict.get(selected_season_name) if selected_season_name else None
            st.session_state.selected_season_index = filtered_seasons.tolist().index(selected_season_name)

            if selected_season_id:
                df = sb.matches(competition_id=selected_competition_id, season_id=selected_season_id)
                st.dataframe(df, use_container_width=True)

                # Format fixture list
                fixture_list = df[['home_team', 'away_team']].apply(lambda x: f"{x['home_team']} vs {x['away_team']}", axis=1)
                fixture_dict = {fixture: match_id for fixture, match_id in zip(fixture_list, df['match_id'])}
                selected_fixture = st.selectbox('Select Fixture', fixture_list, 
                                                  index=st.session_state.get('selected_fixture_index', 0))
                selected_match_id = fixture_dict.get(selected_fixture)
                st.session_state.selected_fixture_index = fixture_list.tolist().index(selected_fixture)

                if selected_match_id:
                    df = sb.events(match_id=selected_match_id)
                    columns = df.columns.tolist()
                    st.session_state.temp_selected_columns = st.multiselect(
                        'Select columns to display:', 
                        columns, 
                        default=st.session_state.get('selected_columns', [])
                    )

                    filtered_df = df[st.session_state.temp_selected_columns]

                    # Temporary variables for selections
                    if 'player' in st.session_state.temp_selected_columns:
                        selected_player = st.selectbox('Select Player', 
                                                        ['All'] + df['player'].dropna().unique().tolist(), 
                                                        index=st.session_state.get('selected_player_index', 0))
                        if selected_player != 'All':
                            filtered_df = filtered_df[filtered_df['player'] == selected_player]

                    if 'team' in st.session_state.temp_selected_columns:
                        selected_team = st.selectbox('Select Team', 
                                                    ['All'] + df['team'].dropna().unique().tolist(), 
                                                    index=st.session_state.get('selected_team_index', 0))
                        if selected_team != 'All':
                            filtered_df = filtered_df[filtered_df['team'] == selected_team]

                    if 'type' in st.session_state.temp_selected_columns:
                        selected_type = st.selectbox('Select Type', 
                                                    ['All'] + df['type'].dropna().unique().tolist(), 
                                                    index=st.session_state.get('selected_type_index', 0))
                        if selected_type != 'All':
                            filtered_df = filtered_df[filtered_df['type'] == selected_type]

                        # After filtering the DataFrame and handling player and team selections
                        if selected_type == 'Shot':
                            # Check if 'shot_technique' is in the selected columns
                            if 'shot_technique' in st.session_state.temp_selected_columns:
                                selected_technique = st.selectbox('Select Shot Technique', 
                                                                ['All'] + df['shot_technique'].dropna().unique().tolist(), 
                                                                index=st.session_state.get('selected_technique_index', 0))
                                if selected_technique != 'All':
                                    filtered_df = filtered_df[filtered_df['shot_technique'] == selected_technique]

                            # Check if 'shot_outcome' is in the selected columns
                            if 'shot_outcome' in st.session_state.temp_selected_columns:
                                selected_outcome = st.selectbox('Select Shot Outcome', 
                                                                ['All'] + df['shot_outcome'].dropna().unique().tolist(), 
                                                                index=st.session_state.get('selected_outcome_index', 0))
                                if selected_outcome != 'All':
                                    filtered_df = filtered_df[filtered_df['shot_outcome'] == selected_outcome]

                    # Display filtered data
                    st.dataframe(filtered_df, use_container_width=True)

                    # Save selections when navigating to Shot Analysis
                    if st.button('Go to Shot Analysis'):
                        save_selections_to_session()  # Save selections before navigation
                        st.session_state.filtered_df = filtered_df
                        st.session_state.page = 'shot_analysis_page'
                        st.rerun()  # Refresh to the next page

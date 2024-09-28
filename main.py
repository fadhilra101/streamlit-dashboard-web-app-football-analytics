import streamlit as st
import numpy as np
import pandas as pd
from statsbombpy import sb
from session import save_selections_to_session, reset_session_state

def main_page():
    selected_items = {}

    data = sb.competitions()
    competition_dict = dict(zip(data['competition_name'], data['competition_id']))
    season_dict = dict(zip(data['season_name'], data['season_id']))

    st.title('Streamlit Web App')
    st.header('Football Match Data from StatsBomb API')

    # Select competition
    competition_list = data['competition_name'].unique().tolist()
    selected_competition_name = st.selectbox('Select Competition', competition_list, index=st.session_state.get('selected_competition_index', None))

    if selected_competition_name:
        selected_competition_id = competition_dict.get(selected_competition_name)
        if selected_competition_name in competition_list:
            selected_items['competition'] = competition_list.index(selected_competition_name)

        if selected_competition_id:
            filtered_seasons = data[data['competition_id'] == selected_competition_id]['season_name'].unique().tolist()
            selected_season_name = st.selectbox('Select Season', filtered_seasons, 
                                                 index=st.session_state.get('selected_season_index', None))
            selected_season_id = season_dict.get(selected_season_name) if selected_season_name else None
            if selected_season_name in filtered_seasons:
                selected_items['season'] = filtered_seasons.index(selected_season_name)

            if selected_season_id:
                df = sb.matches(competition_id=selected_competition_id, season_id=selected_season_id)
                st.dataframe(df, use_container_width=True)

                # Format fixture list
                fixture_list = df[['home_team', 'away_team']].apply(lambda x: f"{x['home_team']} vs {x['away_team']}", axis=1).tolist()
                fixture_dict = {fixture: match_id for fixture, match_id in zip(fixture_list, df['match_id'])}
                selected_fixture = st.selectbox('Select Fixture', fixture_list, 
                                                  index=st.session_state.get('selected_fixture_index', None))
                selected_match_id = fixture_dict.get(selected_fixture)
                if selected_fixture in fixture_list:
                    selected_items['fixture'] = fixture_list.index(selected_fixture)

                if selected_match_id:
                    df = sb.events(match_id=selected_match_id)
                    columns = df.columns.tolist()
                    st.session_state.temp_selected_columns = st.multiselect(
                        'Select columns to display:', 
                        columns, 
                        default=st.session_state.get('selected_columns', [])
                    )

                    filtered_df = df[st.session_state.temp_selected_columns]

                    # Check for required columns to access Shot Analysis page
                    required_shots = ['type', 'location', 'shot_end_location']
                    missing_columns = [col for col in required_shots if col not in st.session_state.temp_selected_columns]

                    if missing_columns:
                        st.warning("To access the **Shot Analysis** page, please select the following columns:\n" + "\n".join(f"- {col}" for col in missing_columns))

                    # Temporary variables for selections
                    
                    if 'player' in st.session_state.temp_selected_columns:
                        players = ['All'] + df['player'].dropna().unique().tolist()
                        selected_player = st.selectbox('Select Player', 
                                                        players, 
                                                        index=st.session_state.get('selected_player_index', 0))
                        selected_items['player'] = players.index(selected_player)

                        if selected_player != 'All':
                            filtered_df = filtered_df[filtered_df['player'] == selected_player]

                    if 'team' in st.session_state.temp_selected_columns:
                        teams = ['All'] + df['team'].dropna().unique().tolist()
                        selected_team = st.selectbox('Select Team', 
                                                    teams, 
                                                    index=st.session_state.get('selected_team_index', 0))
                        selected_items['team'] = teams.index(selected_team)
                        
                        if selected_team != 'All':
                            filtered_df = filtered_df[filtered_df['team'] == selected_team]

                    if 'type' in st.session_state.temp_selected_columns:
                        types = ['All'] + df['type'].dropna().unique().tolist()
                        selected_type = st.selectbox('Select Type', 
                                                    types, 
                                                    index=st.session_state.get('selected_type_index', 0))
                        selected_items['type'] = types.index(selected_type)

                        if selected_type != 'All':
                            filtered_df = filtered_df[filtered_df['type'] == selected_type]

                        # After filtering the DataFrame and handling player and team selections
                        if selected_type == 'Shot':
                            # Check if 'shot_technique' is in the selected columns
                            if 'shot_technique' in st.session_state.temp_selected_columns:
                                techniques = ['All'] + df['shot_technique'].dropna().unique().tolist()
                                selected_technique = st.selectbox('Select Shot Technique', 
                                                                techniques, 
                                                                index=st.session_state.get('selected_shot_technique_index', 0))

                                selected_items['shot_technique'] = techniques.index(selected_technique)

                                if selected_technique != 'All':
                                    filtered_df = filtered_df[filtered_df['shot_technique'] == selected_technique]

                            # Check if 'shot_outcome' is in the selected columns
                            if 'shot_outcome' in st.session_state.temp_selected_columns:
                                outcomes = ['All'] + df['shot_outcome'].dropna().unique().tolist()
                                selected_outcome = st.selectbox('Select Shot Outcome', 
                                                                outcomes, 
                                                                index=st.session_state.get('selected_shot_outcome_index', 0))
                                
                                selected_items['shot_outcome'] = outcomes.index(selected_outcome)

                                if selected_outcome != 'All':
                                    filtered_df = filtered_df[filtered_df['shot_outcome'] == selected_outcome]
                        else:
                            st.warning('You need to select Shot type to access Shot Analysis page.')


                    # Display filtered data
                    st.dataframe(filtered_df, use_container_width=True)

                    # Save selections when navigating to Shot Analysis
                    if st.button('Go to Shot Analysis'):
                        save_selections_to_session(selected_items)
                        st.session_state.filtered_df = filtered_df
                        st.session_state.page = 'shot_analysis_page'
                        st.rerun()  # Refresh to the next page

                if st.button('Reset All'):
                    reset_session_state()
                    st.session_state.page = 'main_page'
                    st.rerun()

    return selected_items
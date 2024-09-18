import streamlit as st
import numpy as np
import pandas as pd
import time
from statsbombpy import sb

st.title('Streamlit Web App')

st.header('Football Match Data from StatsBomb API')

data = sb.competitions()

competition_dict = dict(zip(data['competition_name'], data['competition_id']))
season_dict = dict(zip(data['season_name'], data['season_id']))

selected_competition_name = st.selectbox('Select Competition', data['competition_name'].unique(), index=None)

if selected_competition_name == None:
  st.write('Please select a competition name')
else:
  selected_competition_id = competition_dict[selected_competition_name]
  filtered_seasons = data[data['competition_id'] == selected_competition_id]['season_name'].unique()
  selected_season_name = st.selectbox('Select Season', filtered_seasons, index=None)
  if selected_season_name == None:
    st.write('Please select a season name')
  else:
    selected_season_id = season_dict[selected_season_name]

if (selected_competition_name != None) and (selected_season_name != None):
  st.dataframe(sb.matches(competition_id=selected_competition_id, season_id=selected_season_id), use_container_width=True)
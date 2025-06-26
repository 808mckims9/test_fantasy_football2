import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import plotly.express as px
import plotly.graph_objects as go
import random

# Set page config
st.set_page_config(
    page_title="Fantasy Football Draft Assistant",
    page_icon="🏈",
    layout="wide"
)

# Title and description
st.title("Fantasy Football Draft Assistant 2025 🏈")
st.markdown("""
This app helps you make optimal draft picks using machine learning predictions based on historical NFL and college statistics.
""")

# Initialize session state for teams if not exists
if 'teams' not in st.session_state:
    st.session_state.teams = {
        f'Team {i+1}': [] for i in range(12)  # Default to 12 teams
    }
    st.session_state.current_pick = 1
    st.session_state.current_round = 1

# Update create_sample_data function to track drafted players
if 'drafted_players' not in st.session_state:
    st.session_state.drafted_players = set()

# Update lineup requirements to include K and DST
LINEUP_REQUIREMENTS = {
    'QB': {'starters': 1, 'max': 2},  # 1 starter, max 2 total
    'RB': {'starters': 2, 'max': 5},  # 2 starters + 1 possible flex, max 5 total
    'WR': {'starters': 2, 'max': 6},  # 2 starters + 1 possible flex, max 6 total
    'TE': {'starters': 1, 'max': 2},  # 1 starter + 1 possible flex, max 2 total
    'K': {'starters': 1, 'max': 1},   # 1 kicker
    'DST': {'starters': 1, 'max': 1}  # 1 defense/special teams
}

# Add auto-draft to session state
if 'auto_draft' not in st.session_state:
    st.session_state.auto_draft = False

# Add draft completion status
if 'draft_complete' not in st.session_state:
    st.session_state.draft_complete = False 
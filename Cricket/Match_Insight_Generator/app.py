# app.py
import streamlit as st
import pandas as pd
from match_insights import generate_insights, load_and_clean_data
import os

# ----------------------------
# 1️⃣ Load data and preprocess
# ----------------------------
st.title("🏏 IPL Match Insights Dashboard")

# Load your CSV (ball-by-ball data)
ball_by_ball_path = os.path.join("data","ipl_ball_by_ball.csv")
df, batting_stats_unique, bowling_stats_unique = load_and_clean_data(ball_by_ball_path)

# ----------------------------
# 2️⃣ User input: Season, Teams, Date
# ----------------------------
season = st.selectbox("Select Season", sorted(df['season'].unique()))

# Filter matches for selected season
season_matches = df[df['season']==season][['match_id','batting_team','bowling_team','date']].drop_duplicates()

team1 = st.selectbox("Select Team 1", sorted(season_matches['batting_team'].unique()))
team1_matches = season_matches[(season_matches['batting_team']==team1) | (season_matches['bowling_team']==team1)]

team2_options = pd.unique(team1_matches[['batting_team','bowling_team']].values.ravel())
team2_options = sorted([t for t in team2_options if t != team1])
team2 = st.selectbox("Select Team 2", team2_options)
team2_matches = team1_matches[((team1_matches['batting_team']==team2) | (team1_matches['bowling_team']==team2))]

match_date = st.selectbox("Select Match Date", sorted(team2_matches['date'].unique()))
match_row = team2_matches[team2_matches['date']==match_date].iloc[0]
match_id = match_row['match_id']

st.markdown(f"### Match: {team1} vs {team2} on {match_date}")

# ----------------------------
# 3️⃣ Generate insights
# ----------------------------
insights, batting_phase, bowling_phase, batting_merge, bowling_merge = generate_insights(
    df, batting_stats_unique, bowling_stats_unique, match_id
)

# ----------------------------
# 4️⃣ Show PPI explanation
# ----------------------------
st.markdown("""
**Player Performance Index (PPI)** measures the overall impact of a player in a match:  
- Batters: Runs, Strike Rate, Dot Balls  
- Bowlers: Wickets, Economy, Dot Balls  
Higher PPI = better performance
""")

# ----------------------------
# 5️⃣ Display Batting stats sorted by PPI
# ----------------------------
st.subheader("🏏 Batting Performance (Top by PPI)")
st.dataframe(
    batting_merge.sort_values('PPI', ascending=False)[
        ['striker','runs_match','strike_rate_match','dot_ball_pct_match','PPI']
    ]
)

# ----------------------------
# 6️⃣ Display Bowling stats sorted by PPI
# ----------------------------
st.subheader("🎯 Bowling Performance (Top by PPI)")
st.dataframe(
    bowling_merge.sort_values('PPI', ascending=False)[
        ['bowler','match_wickets','economy','dot_balls','PPI']
    ]
)

# ----------------------------
# 7️⃣ Phase-wise stats
# ----------------------------
st.subheader("⚡ Batting Performance by Phase")
st.dataframe(
    batting_phase.sort_values(['phase','runs_phase'], ascending=[True,False])
)

st.subheader("⚡ Bowling Performance by Phase")
st.dataframe(
    bowling_phase.sort_values(['phase','wickets_phase'], ascending=[True,False])
)

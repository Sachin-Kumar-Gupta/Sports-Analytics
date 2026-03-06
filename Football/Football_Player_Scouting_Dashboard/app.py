import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import euclidean_distances
import plotly.express as px

# ----------------------------
# Load preprocessed data
# ----------------------------
@st.cache_data
def load_data():
    lineups_df = pd.read_csv("processed_data/lineups_clean.csv")
    season_stats = pd.read_csv("processed_data/season_stats_clean.csv")
    player_clusters = pd.read_csv("processed_data/player_clusters.csv")
    return lineups_df, season_stats, player_clusters

lineups_df, season_stats, player_clusters = load_data()

# ----------------------------
# Sidebar - Filters
# ----------------------------
st.sidebar.title("Player Scouting Dashboard")

# Get unique positions from lineups_df
all_positions = lineups_df['position'].explode().dropna().unique().tolist()
position_filter = st.sidebar.selectbox("Select Position", ["All"] + all_positions)

# Filter players by position
if position_filter != "All":
    filtered_players = lineups_df[
        lineups_df['position'].astype(str).str.contains(position_filter)
    ]
    filtered_ids = filtered_players['player_id'].unique()
    filtered_stats = season_stats[season_stats['player_id'].isin(filtered_ids)]
else:
    filtered_stats = season_stats.copy()

# Player selection
player_names = filtered_stats['player_name'].unique().tolist()
selected_player = st.sidebar.selectbox("Select Player", player_names)

# Radar stats columns
radar_stats = [
    'pass_total_per90',
    'carry_total_per90',
    'ball_recovery_total_per90',
    'under_pressure_per90',
    'shot_total_per90'
]

# ----------------------------
# Helper functions
# ----------------------------
def plot_radar_players(players_df, stats_columns, title="Radar Chart"):
    """Interactive radar chart for multiple players with different colors."""
    # Ensure DataFrame
    if isinstance(players_df, pd.Series):
        players_df = players_df.to_frame().T
    
    fig = go.Figure()
    
    # Generate unique colors
    colors = px.colors.qualitative.Plotly
    num_colors = len(colors)
    
    for i, (_, row) in enumerate(players_df.iterrows()):
        values = row[stats_columns].values.tolist()
        values += values[:1]  # Close the loop
        theta = stats_columns + [stats_columns[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=theta,
            fill='toself',
            name=row['player_name'],
            line=dict(color=colors[i % num_colors])
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title=title
    )
    return fig

def find_similar_players(df, player_name, stats_columns, top_n=5):
    """Find top N similar players using Euclidean distance."""
    df_numeric = df[['player_id','player_name'] + stats_columns].set_index('player_id')
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df_numeric[stats_columns])
    
    player_idx = df_numeric.index[df_numeric['player_name'] == player_name][0]
    distances = euclidean_distances(df_scaled, [df_scaled[df_numeric.index.get_loc(player_idx)]])
    df_numeric['distance'] = distances
    similar = df_numeric.sort_values('distance').iloc[1:top_n+1].reset_index()
    return similar[['player_name'] + stats_columns + ['distance']]

# ----------------------------
# Main Dashboard
# ----------------------------
st.title("Football Player Scouting Dashboard")

# Selected player stats
player_row = filtered_stats[filtered_stats['player_name'] == selected_player]
if isinstance(player_row, pd.Series):
    player_row = player_row.to_frame().T  # convert to single-row DataFrame

# Radar chart
st.subheader("Player Radar Chart")
radar_fig = plot_radar_players(player_row, radar_stats)
st.plotly_chart(radar_fig, use_container_width=True)

# Similar players
st.subheader(f"Top 5 Similar Players to {selected_player}")
similar_players = find_similar_players(filtered_stats, selected_player, radar_stats, top_n=5)
st.dataframe(similar_players)

# ----------------------------
# Radar chart with similar players
# ----------------------------
st.subheader(f"Radar Chart: {selected_player} vs Top 5 Similar Players")

# Get top 5 similar players
similar_players_df = find_similar_players(filtered_stats, selected_player, radar_stats, top_n=5)

# Combine selected player + similar players
players_to_plot = pd.concat([player_row, similar_players_df], ignore_index=True)

# Plot combined radar chart
combined_radar_fig = plot_radar_players(players_to_plot, radar_stats,
                                        title=f"{selected_player} and Similar Players")
st.plotly_chart(combined_radar_fig, use_container_width=True)

# ----------------------------
# Cluster visualization
# ----------------------------
st.subheader("Player Clusters (KMeans example)")
from sklearn.cluster import KMeans

X = filtered_stats[radar_stats].fillna(0)
kmeans = KMeans(n_clusters=4, random_state=42).fit(X)
filtered_stats['cluster'] = kmeans.labels_

st.write("Players colored by cluster:")
st.dataframe(filtered_stats[['player_name','cluster'] + radar_stats])
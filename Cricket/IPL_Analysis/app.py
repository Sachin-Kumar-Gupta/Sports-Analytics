import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import base64
import zipfile
import os

zip_path = "data/ipl_phase_dataset.zip"
if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("data")
else:
    st.warning("Dataset ZIP not found — loading pre-extracted files.")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(CURRENT_DIR, 'images', 'welcome.png')

# Page configuration for wide layout and custom title
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for compact, no-scroll design
st.markdown("""
    <div style='background:linear-gradient(90deg,#1e3a8a,#3b82f6); padding:1.5rem; border-radius:14px; text-align:center; margin-bottom:30px;'>
        <h1 style='color:white; margin:0; font-size:2rem;'>🏏 IPL Analytics Dashboard ⚾</h1>
    </div>
    """, unsafe_allow_html=True)    

# ---- Data Loaders ----
@st.cache_data
def load_team_batting_stats():
    return pd.read_csv('Cricket/IPL_Analysis/season_team_batting_phase.csv')

@st.cache_data
def load_team_bowling_stats():
    return pd.read_csv('Cricket/IPL_Analysis/season_team_bowling_phase.csv')

@st.cache_data
def load_team_stats():
    return pd.read_csv('Cricket/IPL_Analysis/ipl_phase_dataset.csv')

@st.cache_data
def load_player_batting():
    return pd.read_csv('Cricket/IPL_Analysis/player_batting_20_25.csv')

@st.cache_data
def load_player_bowling():
    return pd.read_csv('Cricket/IPL_Analysis/player_bowling_20_25.csv')

@st.cache_data
def load_batting_stats():
    return pd.read_csv('Cricket/IPL_Analysis/season_phase_batting_df.csv')

@st.cache_data
def load_bowling_stats():
    return pd.read_csv('Cricket/IPL_Analysis/season_phase_bowling_df.csv')

# ---- Main App ----
analytics_option = {"Select" : "Select",
    "Team Batting": "🏏 Team Batting",
    "Team Bowling": "🎯 Team Bowling",
    "Player Batting": "👤🏏 Player Batting",
    "Player Bowling": "👤🎯 Player Bowling",
    "Purple Cap" : "🟣 Purple Cap (Most Wickets)",
    "Orange Cap" : "🔥 Orange Cap (Most Runs)",
    "Top Player Batting": "🌟🏏 Top Batters",
    "Top Player Bowling": "🌟🎯 Top Bowlers",
    "Scouting Recommendation" : "🔍 Scouting Perspective"}

selected_label = st.sidebar.selectbox("Select Analysis Type", list(analytics_option.values()))
analysis_type = [k for k, v in analytics_option.items() if v == selected_label][0]

# Custom CSS for styling the selectbox
st.markdown("""
    <style>
    div[data-baseweb="select"] {
        background-color: #1e1e2f;
        border-radius: 8px;
        border: 2px solid #FFD700;
        padding: 6px;
        font-weight: bold;
        color: white;
    }
    .stSelectbox label {
        color: white;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Image for home page
# -------
with open(IMAGE_PATH, "rb") as f:
    data = f.read()
    img_base64 = base64.b64encode(data).decode()
    
if analysis_type == 'Select':
    #img_base64 = get_base64_image("Cricket/IPL_Analysis/images/welcome.png")
    st.markdown(f"""
    <div style='text-align:center; margin-top:40px;'>
        <img src="images/welcome.png" width="90" style="margin-bottom:10px;">
        <h2 style='color:#FFD700; margin-bottom:0;'>Welcome to IPL Analytics</h2>
        <p style='color:#FFD700;'>Select Analysis type to explore detailed performance insights for:</p>
        <div style="display:flex; justify-content:center; gap:15px; flex-wrap:wrap; margin-top:15px;">
            <div style="background:#FF6B6B;padding:10px 16px;border-radius:8px;color:white;">Powerplay</div>
            <div style="background:#4ECDC4;padding:10px 16px;border-radius:8px;color:white;">Middle Overs</div>
            <div style="background:#FFD700;padding:10px 16px;border-radius:8px;color:#20232a;">Death Overs</div>
            <div style="background:#DC143C;padding:10px 16px;border-radius:8px;color:white;">Top Performers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
# ------
team_images = {
    "CSK": "Cricket/IPL_Analysis/images/CSK.png",
    "DC" : "Cricket/IPL_Analysis/images/DC.png",
    "DD" : "Cricket/IPL_Analysis/images/DD.png",
    "GL" : "Cricket/IPL_Analysis/images/GL.png",
    "GT" : "Cricket/IPL_Analysis/images/GT.png",
    'KKR' : "Cricket/IPL_Analysis/images/KKR.png",
    'PBKS' : "Cricket/IPL_Analysis/images/PBKS.png",
    'RR' : "Cricket/IPL_Analysis/images/RR.png",
    'Kochi Tuskers Kerala' : "Cricket/IPL_Analysis/images/KTK.png",
    'Pune Warriors' : "Cricket/IPL_Analysis/images/PWI.png", 
    'Rising Pune Supergiants' : "Cricket/IPL_Analysis/images/RPS.png",
    'LSG' : "Cricket/IPL_Analysis/images/LSG.png",
    "MI": "Cricket/IPL_Analysis/images/MI.png",
    "RCB": "Cricket/IPL_Analysis/images/RCB.png",
    "SRH": "Cricket/IPL_Analysis/images/SRH.png"}

# -------------------------
# 1. Define Plotting Functions at the Top of Script
# -------------------------

def plot_team_batting(df,team, metric, by):
    filtered_df = df[df['cleaned_team_batting'] == team]
    fig = px.line(filtered_df,x='season',y= metric,color= by,
                  title=f'📈 Evolution of {metric} Across IPL Seasons', 
                  labels={ 'run_rate' : 'Run Rate (RPO)','wickets' : 'Total Wickets', 'season': 'IPL Season'}, 
                  color_discrete_map={'Powerplay': '#FF6B6B','Middle': '#4ECDC4','Death': '#45B7D1'})
    # Enhanced styling
    hover_labels = {'run_rate': 'Run Rate','wickets': 'Wickets'}
    label = hover_labels.get(metric, metric.replace('_', ' ').title())
    fig.update_traces(mode='lines+markers',line=dict(width=4),marker=dict(size=8), 
                      hovertemplate='<b>%{fullData.name}</b><br>' +
                      'Season: %{x}<br>' +
                      f'{label} : ' +'%{y:.2f} <extra></extra>')

    fig.update_layout(title_font_size=18,title_x = 0.3,height=500, 
                      hovermode='x unified',legend=dict(orientation="h",
                                                        yanchor="bottom", 
                                                        y=1,
                                                        xanchor="center",
                                                        x=0.5))
    return fig

def plot_team_bowling(df,team, metric,by): 
    filtered_df = df[df['cleaned_team_bowling'] == team]
    fig = px.line(filtered_df,x='season',y= metric,color= by, 
                  title = f'📈 Evolution of {metric} Across IPL Seasons',
                  labels={ 'economy_rate' : 'Economy Rate (RPO)','wickets' : 'Total Wickets', 'season': 'IPL Season'},
                  color_discrete_map={'Powerplay': '#FF6B6B','Middle': '#4ECDC4','Death': '#45B7D1'})
    # Enhanced styling
    hover_labels = {'run_rate': 'Run Rate','wickets': 'Wickets'}
    label = hover_labels.get(metric, metric.replace('_', ' ').title())
    fig.update_traces(mode='lines+markers',line=dict(width=4),marker=dict(size=8),
                        hovertemplate='<b>%{fullData.name}</b><br>' +
                        'Season: %{x}<br>' +
                        f'{label} : ' +'%{y:.2f} <extra></extra>')
    
    fig.update_layout(title_font_size=18,title_x=0.3,height=500,
                        hovermode='x unified',legend=dict(orientation="h",
                                                          yanchor="bottom",
                                                          y=1,xanchor="center",
                                                          x=0.5))
    return fig
    pass


def plot_player_batting(df, player, metric,by):
    
    # Filter data for selected player
    player_df = df[df['striker'] == player]

    # Retrieve the latest or overall performance index
    performance_idx = player_df['performance_index'].mean()  # or use latest season

    fig = px.line(player_df,x='season',y= metric,color= by, 
                  title = f'📈 Evolution of {metric} Across IPL Seasons',
                  labels={ 'run_rate' : 'Run Rate (RPO)','runs' : 'Total Runs', 'season': 'IPL Season'},
                  color_discrete_map={'Powerplay': '#FF6B6B','Middle': '#4ECDC4','Death': '#45B7D1'})
    # Enhanced styling
    hover_labels = {'run_rate': 'Run Rate','wickets': 'Wickets'}
    label = hover_labels.get(metric, metric.replace('_', ' ').title())
    fig.update_traces(mode='lines+markers',line=dict(width=4),marker=dict(size=8),
                        hovertemplate='<b>%{fullData.name}</b><br>' +
                        'Season: %{x}<br>' +
                        f'{label} : ' +'%{y:.2f} <extra></extra>')
    
    fig.update_layout(title_font_size=18,title_x=0.3,height=500,
                        hovermode='x unified',legend=dict(orientation="h",
                                                          yanchor="bottom",
                                                          y=1,xanchor="center",
                                                          x=0.5))

    # Optionally, annotate best season/metric
    max_season = player_df.loc[player_df[metric].idxmax(), 'season']
    max_value = player_df[metric].max()
    fig.add_annotation(
        x=max_season, y=max_value,
        text=f'Best: {max_value:.2f} in {max_season}',
        showarrow=True, arrowhead=2, ax=0, ay=-40,
        font=dict(size=12, color="green")
    )

    return fig

def plot_player_bowling(df, player, metric,by):
    
    # Filter data for selected player
    player_df = df[df['bowler'] == player]

    # Retrieve the latest or overall performance index
    performance_idx = player_df['performance_index'].mean()  # or use latest season

    fig = px.line(player_df,x='season',y= metric,color= by, 
                  title = f'📈 Evolution of {metric} Across IPL Seasons',
                  labels={ 'economy_rate' : 'Economy Rate (RPO)','wickets' : 'Total Wickets', 'season': 'IPL Season'},
                  color_discrete_map={'Powerplay': '#FF6B6B','Middle': '#4ECDC4','Death': '#45B7D1'})
    # Enhanced styling
    hover_labels = {'run_rate': 'Run Rate','wickets': 'Wickets'}
    label = hover_labels.get(metric, metric.replace('_', ' ').title())
    fig.update_traces(mode='lines+markers',line=dict(width=4),marker=dict(size=8),
                        hovertemplate='<b>%{fullData.name}</b><br>' +
                        'Season: %{x}<br>' +
                        f'{label} : ' +'%{y:.2f} <extra></extra>')
    
    fig.update_layout(title_font_size=18,title_x=0.3,height=500,
                        hovermode='x unified',legend=dict(orientation="h",
                                                          yanchor="bottom",
                                                          y=1,xanchor="center",
                                                          x=0.5))
    #Optionally, annotate best season/metric
    max_season = player_df.loc[player_df[metric].idxmax(), 'season']
    max_value = player_df[metric].max()
    fig.add_annotation(
        x=max_season, y=max_value,
        text=f'Best: {max_value:.2f} in {max_season}',
        showarrow=True, arrowhead=2, ax=0, ay=-40,
        font=dict(size=12, color="green")
    )

    return fig

# -------------------------
# 2. In Streamlit App Logic: Use IF/ELSE To Select and Call Functions
# -------------------------

if analysis_type == 'Team Batting':
    df = load_team_batting_stats()
    team = st.sidebar.selectbox("🏆 Team", sorted(df['cleaned_team_batting'].unique()))
    metric = st.sidebar.selectbox("⚡ Metric", ['run_rate', 'total_runs','boundaries','fours','sixes'])
    st.sidebar.markdown("""
        <style>
        /* Change sidebar section title and label text color */
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #FFD700 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    if team in team_images:
        st.sidebar.image(team_images[team], caption=f"{team} Logo", width=150)
    else:
        st.sitebar.write("Logo not found for selected team.")
        
    fig = plot_team_batting(df,team, metric, 'phase')   # <--- call function here
    st.plotly_chart(fig)
    
    insights = {
        'CSK': "CSK: \n\nLegendary death-over finishing; boosting Powerplay aggression could elevate totals.",
        'MI': "MI:\n\n Deadly death overs and steady middle. A more explosive Powerplay can lift match totals.",
        'DC': "DC: \n\nStrong middle-overs, improving death-overs. Consistent Powerplay acceleration is key.",
        'SRH': "SRH:\n\n Balanced order, strong middle and death. Powerplay explosiveness would boost competitiveness.",
        'GT':"GT: \n\nPerformed really well in power-play as compared to last year jumped from 7.35 to 8.95 RPO. \n\nOther phases are also well balanced but improved very little as compared to last year",
        'KKR' : "KKR :\n\nIn current season KKR struggled in Middle order, for scoring high they heavily depend on Openers and specially on Finishers",
        'LSG' : "LSG:\n\n Steady Death-over muscle (≈10 RPO every year) underpins their totals, while Powerplay acceleration has jumped 30% in two seasons, signalling a shift from consolidating starts to all-phase aggression.",
        'PBKS' : "PBKS:\n\nDeath-overs run-rate has surged to a franchise-best 12 RPO, yet Powerplay scoring still hovers near 9 RPO—so PBKS rely on end-overs fireworks to offset sluggish starts.",
        'RR' : "RR :\n\nMiddle over still fluctuates around 8 to 9 RPO, but since 2020 both Powerplay-overs and Death-overs rates climb past 10 RPO, showing Rajasthan’s ability to explode after the first six overs and finish games with late fireworks.",
        'RCB' : "RCB : \n\nRoyal Challengers Bengaluru translated all-phase consistency into silverware: sustaining ≈9.5 RPO across Powerplay, Middle and Death overs gave RCB the balanced scoring profile that underpinned their title-winning campaign."
    }
    if team in insights:
        st.info(insights[team])
        
    # ---- Recommendations (Optional) ----
    if st.checkbox("Show General Recommendations"):
        st.markdown("""
        **Recommendations:**
        - Strengthen Powerplay aggression (recruit openers/finishers).
        - Maintain middle-overs control with spin-seam options.
        - Optimize death-over matchups using analytics.
        """)

elif analysis_type == 'Team Bowling':
    df = load_team_bowling_stats()
    team = st.sidebar.selectbox("🏆 Team", sorted(df['cleaned_team_bowling'].unique()))
    metric = st.sidebar.selectbox("⚡ Metric", ['economy_rate', 'total_runs','boundaries','fours','sixes'])
    st.sidebar.markdown("""
        <style>
        /* Change sidebar section title and label text color */
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #FFD700 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    insights = {
        'CSK': "CSK: \n\nDeath-over containment remains Chennai’s trademark—despite a recent uptick, they still sit under 10 RPO while rivals push 11 +.\n\nPowerplay and Middle overs hover in the mid-7s, giving CSK the IPL’s most evenly frugal attack and keeping chase demands manageable.",
        'MI': "MI:\n\nMumbai’s once-stingy attack is heading the wrong way: since 2022, economy has climbed from 7 RPO to 8.5 RPO in Powerplay./n/n At the death over,they really improved their economy rate and came from 11 RPO to 9.5 RPO.",
        'DC': "DC: \n\n The attack has tightened its middle-over screws—economy falling to the mid-8 RPO range—yet both Powerplay and Death overs have drifted above 9 RPO since 2023, underscoring DC’s need for new-ball breakthroughs and end-overs control to complement the increasingly miserly middle spell.",
        'SRH': "SRH:\n\nThe Sunrisers keep things relatively controlled up front and in the middle, but leakage balloons past 10 RPO at the death—underscoring that closing overs remain their biggest defensive gap.",
        'GT':"GT: \n\nEconomy rates dipped steadily to 7.5 RPO by 2022, but a sharp rise in both Powerplay and Death overs saw figures rebound above 9 RPO in 2024-25—highlighting the Titans’ new-ball and slog-over leakiness despite mid-innings control.",
        'KKR' : "KKR :\n\n Kolkata’s attack has become increasingly back-loaded: Middle-over economy now sits just under 8 RPO, but Death-over leakage has climbed beyond 11 RPO in recent years—highlighting strong middle control yet a pressing need for reliable finishers.",
        'LSG' : "LSG:\n\n after debut-season discipline (7.5 RPO in 2023), all three phases have loosened—Powerplay and Death overs now hover near 10 RPO, while Middle overs creep above 9 RPO—signalling a unit that urgently needs both new-ball penetration and reliable finishers to avoid leak-prone totals.",
        'PBKS' : "PBKS:\n\n Economy rate has drifted upward across the board—Death overs now sit above 10 RPO and even Powerplay containment has pushed past 9 RPO—highlighting a unit that leaks in every phase and urgently needs tighter new-ball plans and end-overs discipline.",
        'RR' : "RR :\n\nDeath-over leakage sits above 10 RPO almost last 5 season, while both Powerplay and Middle phases hover near 9 RPO—pointing to a consistently expensive finish and a need for sharper execution across all 20 overs.",
        'RCB' : "RCB : \n\nEconomy rates climb on both middle and back ends—Powerplay approaches improved from last year 9.35 to 8.33 RPO and Death overs stay above 10 RPO—signalling that Bengaluru must sharpen middle over deliveries accuracy and death-over execution to stem late run-leakage."
    }

    if team in team_images:
        st.sidebar.image(team_images[team], caption=f"{team} Logo", width=200)
    else:
        st.sitebar.write("Logo not found for selected team.")
    
    fig = plot_team_bowling(df, team, metric, 'phase')   # <--- call function here
    st.plotly_chart(fig)

    if team in insights:
        st.info(insights[team])
        
    # ---- Recommendations (Optional) ----
    if st.checkbox("Show General Recommendations"):
        st.markdown("""
        **Recommendations:**
        - Prioritise new-ball specialists who swing or seam at pace..
        - Encourage rapid over-rate and field-rotation drills to keep pressure constant; dot-ball clusters lower economy faster than sporadic wickets.
        - Make yorker execution measurable: set in-nets targets (≥60% yorker accuracy under simulated crowd noise).
        """)

elif analysis_type == 'Orange Cap':
    df = load_team_stats()
    legal = df[~df["extras_type"].isin(["wide"])]
    season = st.sidebar.selectbox('Season', sorted(df['season'].unique()))
    agg = legal.groupby(['season','striker']).agg(
        runs = ('batsman_runs','sum'),
        balls_faced = ('ball','count'),
        lost_wicket=('player_dismissed', lambda x: x.notna().sum()),
        dot_balls = ('batsman_runs',lambda x: (x==0).sum()),
        boundaries=('batsman_runs', lambda x: ((x==4)| (x ==6)).sum()),
        fours = ('is_four','sum'),
        sixes = ('is_six','sum')).reset_index()
    # Filter on min_balls per phase
    agg['strike_rate'] = (agg['runs'] / agg['balls_faced'] *100).round(2)
    agg['balls_per_dismissal'] = (agg.apply(lambda row: row['balls_faced'] / row['lost_wicket']
                                             if row['lost_wicket'] > 0 else np.nan,axis=1)).round(2)
    agg['batting_avg'] = (agg.apply(lambda row: row['runs'] / row['lost_wicket']
                                             if row['lost_wicket'] > 0 else np.nan,axis=1)).round(2)
    agg['dot_ball_pct'] = (agg['dot_balls'] / agg['balls_faced']).round(2)
    agg['dismissal_rate'] = (agg['lost_wicket'] / agg['balls_faced']).round(2)
    # --- 3. Sort and take Top N ------------------------------------
    top_n = 10   # change as you like
    orange_top = (agg[agg['season']==season].sort_values('runs', ascending=False).head(top_n).reset_index(drop=True))
    if "season" in orange_top.columns:
        orange_top = orange_top.drop(columns="season")

    # --- 4. Display -------------------------------------------------
    st.subheader(f"🏏🟠 Top Orange-Cap Performers for {season}")
    st.dataframe(orange_top, hide_index=True)

elif analysis_type == 'Purple Cap':
    df = load_team_stats()
    season = st.sidebar.selectbox('Season', sorted(df['season'].unique()))
    bowler_dismissals = {"caught","bowled","lbw","caught and bowled","stumped","hit wicket"}
    df['bowler_wicket'] = df['wicket_type'].isin(bowler_dismissals)
    agg = df.groupby(['season','bowler']).agg(
        wickets=('bowler_wicket', 'sum'),
        runs_conceded = ('total_runs','sum'),
        balls_bowled = ('ball','count'),
        dot_balls = ('batsman_runs',lambda x: (x==0).sum()),
        boundaries=('batsman_runs', lambda x: ((x==4)| (x ==6)).sum()),
        fours = ('is_four','sum'),
        sixes = ('is_six','sum')).reset_index()
    # Filter on min_balls per phase
    agg['economy_rate'] = (agg['runs_conceded'] / (agg['balls_bowled']/6)).round(2)
    agg['balls_per_wicket'] = (agg.apply(lambda row: row['balls_bowled'] / row['wickets']
                                         if row['wickets'] > 0 else np.nan,axis=1)).round(2)
    agg['bowling_avg'] = (agg.apply(lambda row: row['runs_conceded'] / row['wickets']
                                         if row['wickets'] > 0 else np.nan,axis=1)).round(2)
    agg['dot_ball_pct'] = (agg['dot_balls'] / agg['balls_bowled']).round(2)
    agg['boundary_pct'] = (agg['boundaries'] / agg['balls_bowled']).round(2)
    agg['six_pct'] = (agg['sixes'] / agg['balls_bowled']).round(2)
    # --- 3. Sort and take Top N ------------------------------------
    top_n = 10   # change as you like
    purple_top = (agg[agg['season']==season].sort_values('wickets', ascending=False).head(top_n).reset_index(drop=True))
    if "season" in purple_top.columns:
        purple_top = purple_top.drop(columns="season")

    # --- 4. Display -------------------------------------------------
    st.subheader(f"🏏🟣 Top Purple-Cap Performers for {season}")
    st.dataframe(purple_top, hide_index=True)
    
elif analysis_type == 'Player Batting':
    df = load_batting_stats()
    recent = df[df['season'] > 2020].copy()
    st.markdown(f"### 📊 Season-wise Player batting Performance")
    name = st.sidebar.selectbox('Player Name', sorted(recent['striker'].unique()))
    metric = st.sidebar.selectbox("Select Metric for Ranking",
                                  ['strike_rate','runs', 'sixes', 'fours', 'boundaries', 
                                   'performance_index'])
    fig = plot_player_batting(df,name, metric, 'phase')   # <--- call function here
    st.plotly_chart(fig)
    
elif analysis_type == 'Player Bowling':
    df = load_bowling_stats()
    recent = df[df['season'] > 2020].copy()
    st.markdown(f"### 📊 Season-wise Player bowling Performance")
    name = st.sidebar.selectbox('Player Name', sorted(recent['bowler'].unique()))
    metric = st.sidebar.selectbox("Select Metric for Ranking",
                                  ['economy_rate','runs_conceded','wickets', 'sixes', 'fours', 'boundaries', 
                                   'performance_index'])

    fig = plot_player_bowling(df,name, metric, 'phase')   # <--- call function here
    st.plotly_chart(fig)
    
elif analysis_type == 'Top Player Batting':
    df = load_player_batting()
    st.markdown(f"### 📊 Ranking based on Last 5 Season Performance and min balls played 120")
    # For Top 5 Batting Players
    phase = st.sidebar.selectbox("Select Phase",['Powerplay','Middle','Death'])
    metric = st.sidebar.selectbox("Select Metric for Ranking",
                                  ['strike_rate','runs', 'sixes', 'fours', 'boundaries', 
                                   'performance_index'])
    player = st.sidebar.number_input("Top N Player", min_value=1, step=1)
    st.sidebar.markdown("""
        <style>
        /* Change sidebar section title and label text color */
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #FFD700 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    filtered_df = df[df['phase'] == phase]
    player_stats = filtered_df.groupby('striker')[metric].sum().reset_index()
    top5_batsmen = player_stats.sort_values(by=metric, ascending=False).head(player)

    st.subheader("Top Batsmen")
    st.dataframe(top5_batsmen, hide_index=True)
    
elif analysis_type == 'Top Player Bowling':
    df = load_player_bowling()
    st.markdown(f"### 📊 Ranking based on Last 5 Season Performance and min balls bowled 120")
    # For Top 5 Bowling Players
    phase = st.sidebar.selectbox("Select Phase",['Powerplay','Middle','Death'])
    metric = st.sidebar.selectbox("Select Metric for Ranking",
                                  ['economy_rate','runs_conceded', 'sixes', 'fours', 'boundaries', 
                                   'performance_index'])
    player = st.sidebar.number_input("Top N Player", min_value=1, step=1)
    
    filtered_df = df[df['phase'] == phase]
    player_stats = filtered_df.groupby('bowler')[metric].sum().reset_index()
    st.sidebar.markdown("""
        <style>
        /* Change sidebar section title and label text color */
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #FFD700 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    if metric != 'performance_index':
        top5_bowler = player_stats.sort_values(by=metric, ascending=True).head(player)
    else :
        top5_bowler = player_stats.sort_values(by=metric, ascending=False).head(player)

    st.subheader("Top Bowler")
    st.dataframe(top5_bowler, hide_index=True)
    
elif analysis_type == 'Scouting Recommendation':
    recommended = {
    "Openers"      : ["KL Rahul", "Faf du Plessis",'Rishab Pant','Klaasen'],
    "Middle Order" : ["Ishan Kishan", "Quinton de Kock","Suryakumar Yadav"],
    "Bowlers"      : ["Washington Sundar","Shivam Dubey", "T Natarajan",'C Sakaria','Ferguson']}
    with st.container():
        st.markdown("### 🔍 Recommended Players")
        # Nice subtle line below the header
        st.markdown("<hr style='margin-top:0; margin-bottom:0'>", unsafe_allow_html=True)

    for section, names in recommended.items():
        # Bold sub-heading
        st.markdown(f"**{section}**")
        # Bullet list of names
        st.markdown("• " + " • ".join(names))
        st.write("")

st.markdown("---\n*Created by Sachin Kumar Gupta — IPL Phase Portfolio*")














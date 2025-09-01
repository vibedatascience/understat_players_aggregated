import pandas as pd
import numpy as np
import json
from datetime import datetime

# Load the complete dataset
df = pd.read_csv('/Users/rchaudhary/Downloads/understat_data/understat_players_aggregated_2014_td.csv')

# Filter for EPL only
epl_df = df[df['league'] == 'EPL'].copy()

print("EPL Dataset Overview:")
print(f"Total records: {len(epl_df)}")
print(f"Seasons covered: {sorted(epl_df['season'].unique())}")
print(f"Unique players: {epl_df['id'].nunique()}")
print(f"Teams: {len(epl_df['team_title'].unique())}")

# Top scorers by season
top_scorers_by_season = []
for season in sorted(epl_df['season'].unique()):
    season_data = epl_df[epl_df['season'] == season]
    top_scorer = season_data.loc[season_data['goals'].idxmax()]
    top_scorers_by_season.append({
        'season': season,
        'player': top_scorer['player_name'],
        'team': top_scorer['team_title'],
        'goals': int(top_scorer['goals']),
        'xG': round(float(top_scorer['xG']), 2)
    })

# xG vs Goals scatter data (current season)
current_season = epl_df['season'].max()
current_data = epl_df[(epl_df['season'] == current_season) & (epl_df['games'] >= 5)]

xg_vs_goals = []
for _, player in current_data.iterrows():
    xg_vs_goals.append({
        'name': player['player_name'],
        'team': player['team_title'],
        'goals': int(player['goals']),
        'xG': round(float(player['xG']), 2),
        'games': int(player['games'])
    })

# Team performance over time
team_performance = []
for season in sorted(epl_df['season'].unique()):
    season_data = epl_df[epl_df['season'] == season]
    team_stats = season_data.groupby('team_title').agg({
        'goals': 'sum',
        'xG': 'sum',
        'assists': 'sum',
        'games': 'sum'
    }).reset_index()
    
    for _, team in team_stats.iterrows():
        team_performance.append({
            'season': season,
            'team': team['team_title'],
            'total_goals': int(team['goals']),
            'total_xG': round(float(team['xG']), 2),
            'total_assists': int(team['assists'])
        })

# Position analysis
position_stats = epl_df.groupby('primary_position').agg({
    'goals': 'mean',
    'xG': 'mean',
    'assists': 'mean',
    'key_passes': 'mean',
    'shots': 'mean'
}).round(2).reset_index()

position_data = []
for _, pos in position_stats.iterrows():
    if not pd.isna(pos['primary_position']):
        position_data.append({
            'position': pos['primary_position'],
            'avg_goals': round(float(pos['goals']), 2),
            'avg_xG': round(float(pos['xG']), 2),
            'avg_assists': round(float(pos['assists']), 2),
            'avg_key_passes': round(float(pos['key_passes']), 2),
            'avg_shots': round(float(pos['shots']), 2)
        })

# Export data for web page
web_data = {
    'overview': {
        'total_records': len(epl_df),
        'seasons_covered': sorted(epl_df['season'].unique()),
        'unique_players': int(epl_df['id'].nunique()),
        'teams_count': int(epl_df['team_title'].nunique()),
        'current_season': current_season,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    },
    'top_scorers_by_season': top_scorers_by_season,
    'xg_vs_goals_current': xg_vs_goals[:50],  # Top 50 players with most games
    'team_performance': team_performance,
    'position_analysis': position_data
}

# Save to JSON file
with open('/Users/rchaudhary/Downloads/understat_data/epl_analysis_data.json', 'w') as f:
    json.dump(web_data, f, indent=2)

print(f"\nData exported to JSON successfully!")
print(f"Top scorers sample: {top_scorers_by_season[-3:]}")
print(f"Position analysis sample: {position_data}")
import requests
import pandas as pd
import time
from datetime import datetime
import os

def get_current_season():
    """Determine current season based on date
    Football seasons run August to May
    Sept 2025 = 2025/26 season = "2025" in Understat
    """
    now = datetime.now()
    year = now.year
    month = now.month
    
    if month >= 8:
        return str(year)
    else:
        return str(year - 1)

leagues = {
    'EPL': 'EPL',
    'La_Liga': 'La_liga', 
    'Bundesliga': 'Bundesliga',
    'Serie_A': 'Serie_A',
    'Ligue_1': 'Ligue_1',
    'RFPL': 'RFPL'
}

ALL_COLUMNS = ['assists', 'games', 'goals', 'id', 'key_passes', 'npg', 'npxG', 
               'player_name', 'position', 'red_cards', 'shots', 'team_title', 
               'time', 'xA', 'xG', 'xGBuildup', 'xGChain', 'yellow_cards']

def extract_primary_position(pos):
    """Extract primary position from position string"""
    allowed = {'M', 'D', 'S', 'F', 'GK'}
    if pd.isna(pos):
        return pd.NA
    for tok in str(pos).split():
        if tok in allowed:
            return tok
    return pd.NA

def scrape_understat(league, season, max_retries=3):
    """Scrape player data from Understat"""
    url = 'https://understat.com/main/getPlayersStats/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
    }
    payload = {'league': league, 'season': season}
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['response']['players']
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return []

current_season = get_current_season()
all_data = []

for league_name, league_code in leagues.items():
    players = scrape_understat(league_code, current_season)
    
    if players:
        df = pd.DataFrame(players)
        
        for col in ALL_COLUMNS:
            if col not in df.columns:
                df[col] = None
        
        df['league'] = league_name
        df['year'] = int(current_season)
        df['season'] = f"{current_season}/{str(int(current_season)+1)[2:]}"
        df = df[ALL_COLUMNS + ['league', 'year', 'season']]
        
        all_data.append(df)
    
    time.sleep(1.5)

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    
    numeric_cols = ['assists', 'games', 'goals', 'key_passes', 'npg', 'npxG',
                   'red_cards', 'shots', 'time', 'xA', 'xG', 'xGBuildup', 
                   'xGChain', 'yellow_cards']
    
    for col in numeric_cols:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
    
    # Convert id to string to ensure consistency
    final_df['id'] = final_df['id'].astype(str)
    
    final_df['position'] = final_df['position'].astype(str).str.strip()
    final_df['team_title'] = final_df['team_title'].astype(str).str.strip()
    final_df['player_name'] = final_df['player_name'].astype(str).str.strip()
    
    final_df['primary_position'] = final_df['position'].apply(extract_primary_position)
    
    final_df['scrape_timestamp'] = datetime.now().isoformat()
    
    filename = f'understat_players_aggregated_{current_season}_latest.parquet'
    final_df.to_parquet(filename, compression='snappy', index=False)
    
    csv_filename = f'understat_players_aggregated_{current_season}_latest.csv'
    final_df.to_csv(csv_filename, index=False)
    
    # Append to historical data if it exists
    historical_file = 'understat_players_aggregated_2014_2024.csv'
    if os.path.exists(historical_file):
        historical_df = pd.read_csv(historical_file, low_memory=False)
        
        # Ensure id column is string in historical data too
        historical_df['id'] = historical_df['id'].astype(str)
        
        # Combine historical with current season
        combined_df = pd.concat([historical_df, final_df], ignore_index=True)
        
        # Save combined data
        combined_csv = 'understat_players_aggregated_2014_td.csv'
        combined_parquet = 'understat_players_aggregated_2014_td.parquet'
        
        combined_df.to_csv(combined_csv, index=False)
        combined_df.to_parquet(combined_parquet, compression='snappy', index=False)
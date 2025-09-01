# Understat Football Player Statistics Dataset

## Overview
Comprehensive football player statistics from Europe's top 6 leagues, sourced from Understat.com. Contains detailed performance metrics including goals, expected goals (xG), assists, and advanced analytics.

## Files

| File | Coverage | Description |
|------|----------|-------------|
| `understat_players_aggregated_2014_2024.csv` | 2014/15 - 2024/25 | Historical data for 11 complete seasons |
| `understat_players_aggregated_2025_latest.csv` | 2025/26 only | Current season in progress (updated daily) |
| `understat_players_aggregated_2014_td.csv` | 2014/15 - current | Complete dataset including latest matches (updated daily) |

*Parquet versions also available for all files (70% smaller, faster loading)*

## Quick Start

### Load Data Directly from GitHub

```python
import pandas as pd

# For historical analysis (complete seasons only)
historical = pd.read_csv('https://raw.githubusercontent.com/vibedatascience/understat_players_aggregated/main/understat_players_aggregated_2014_2024.csv')

# For current season tracking
current = pd.read_csv('https://raw.githubusercontent.com/vibedatascience/understat_players_aggregated/main/understat_players_aggregated_2025_latest.csv')

# For complete dataset
full = pd.read_csv('https://raw.githubusercontent.com/vibedatascience/understat_players_aggregated/main/understat_players_aggregated_2014_td.csv')
```

### Load Local Files

```python
import pandas as pd

# For historical analysis (complete seasons only)
historical = pd.read_csv('understat_players_aggregated_2014_2024.csv')

# For current season tracking
current = pd.read_csv('understat_players_aggregated_2025_latest.csv')

# For complete dataset
full = pd.read_csv('understat_players_aggregated_2014_td.csv')
```

## Coverage Details

### League Codes
- **EPL** - English Premier League
- **La_Liga** - Spanish La Liga  
- **Bundesliga** - German Bundesliga
- **Serie_A** - Italian Serie A
- **Ligue_1** - French Ligue 1
- **RFPL** - Russian Premier League

### Seasons
- **Historical**: 2014/15 through 2024/25 (11 complete seasons)
- **Current**: 2025/26 (in progress)
- **Records**: ~37,000 player-season combinations
- **Unique Players**: ~10,700 individuals

## Data Dictionary

### Core Columns

| Column | Type | Description |
|--------|------|-------------|
| `id` | int | Unique player ID (critical for tracking) |
| `player_name` | str | Player full name |
| `team_title` | str | Club name |
| `league` | str | League code (see league codes above) |
| `year` | int | Season start year (e.g., 2024 for 2024/25) |
| `season` | str | Display format (e.g., "2024/25") |

### Performance Metrics

| Column | Type | Description | Range |
|--------|------|-------------|-------|
| `goals` | int | Goals scored | 0-48 |
| `xG` | float | Expected goals | 0-39.31 |
| `npg` | int | Non-penalty goals | 0-44 |
| `npxG` | float | Non-penalty xG | 0-35.2 |
| `assists` | int | Assists | 0-20 |
| `xA` | float | Expected assists | 0-20.62 |
| `shots` | int | Total shots | 0-227 |
| `key_passes` | int | Passes leading to shots | 0-146 |

### Playing Time & Position

| Column | Type | Description |
|--------|------|-------------|
| `games` | int | Matches played (max 38 in most leagues) |
| `time` | int | Minutes played |
| `position` | str | Raw position data (e.g., "F M S") |
| `primary_position` | str | Clean position (F/M/D/GK/S) |

### Advanced & Disciplinary

| Column | Type | Description |
|--------|------|-------------|
| `xGChain` | float | xG from possession chains |
| `xGBuildup` | float | xG from buildup play |
| `yellow_cards` | int | Yellow cards |
| `red_cards` | int | Red cards |
| `scrape_timestamp` | str | Data collection time |

## Critical Usage Guidelines

### Player Identification

**Important**: Multiple players can share the same name. Always use the `id` column for accurate player tracking.

```python
# CORRECT - Use player ID to identify specific player
player_data = df[df['id'] == 2371]
player_name = player_data['player_name'].iloc[0]  # Get name after finding by ID

# WRONG - Multiple different players may be named "Gabriel" 
# player_data = df[df['player_name'] == 'Gabriel']  # Don't do this
```

### Mid-Season Transfers

Players who transferred during a season have separate records for each club. Their stats are split across multiple rows with the same player `id` and `year`.

```python
# Example: Player with id=1234 in 2020 
# May have 2 rows: one for Manchester United, one for Inter Milan
# Each row shows stats for that specific club only
```

To get full season totals for transferred players, aggregate by `id` and `year`.

## Data Quality Notes

1. **Current Season**: 2025/26 data is partial (season in progress)
2. **Player IDs**: Essential for accurate tracking due to ~200 name duplicate cases
3. **Transfer Records**: ~850 players per season have multiple club records
4. **Missing Values**: Dataset is complete with no nulls

## File Formats

All datasets are available in both CSV and Parquet formats:
- **CSV**: Universal compatibility, human-readable
- **Parquet**: 70% smaller file size, faster loading with pandas

## Data Source

Data sourced from [Understat.com](https://understat.com/), a leading football analytics platform providing expected goals (xG) and other advanced metrics.
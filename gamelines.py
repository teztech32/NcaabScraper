import requests  # Fixed typo (was 'request')
from bs4 import BeautifulSoup
from typing import List, Dict

# List of D1 conferences (you might want to populate this)
d1_conferences = [
    "ACC", "Big Ten", "Big 12", "Pac-12", "SEC", 
    "American Athletic", "Conference USA", 
    "Mid-American", "Mountain West", "Sun Belt"
]

def get_gamelines(max_lines: int = 50) -> List[Dict]:
    """
    Scrape game line data from DraftKings sportsbook
    Returns a list of dictionaries containing game information
    
    Args:
        max_lines (int): Maximum number of game lines to return
        
    Returns:
        List of dictionaries with game data
    """
    url = "https://sportsbook.draftkings.com/leagues/football/college-football"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        games = []
        
        # Find game elements - this selector might need adjustment based on DraftKings' HTML structure
        game_elements = soup.select('.sportsbook-event-holder')[:max_lines]
        
        for game in game_elements:
            try:
                teams = [team.text.strip() for team in game.select('.event-cell-participant')]
                if len(teams) != 2:
                    continue
                    
                spread = game.select_one('.sportsbook-outcome-cell-label').text.strip()
                total = game.select_one('.sportsbook-outcome-cell-total').text.strip()
                moneyline = game.select_one('.sportsbook-outcome-moneyline').text.strip()
                
                games.append({
                    'team1': teams[0],
                    'team2': teams[1],
                    'spread': spread,
                    'total': total,
                    'moneyline': moneyline,
                    'conference': get_conference(teams[0])  # Determine conference
                })
            except Exception as e:
                print(f"Error parsing game: {e}")
                continue
                
        return games
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def get_conference(team_name: str) -> str:
    """
    Determine which conference a team belongs to
    (This would need to be implemented with actual team-conference mappings)
    """
    # This is a placeholder - you'd need actual team-conference data
    for conference in d1_conferences:
        # Simple example - would need actual team lists per conference
        if conference.lower() in team_name.lower():
            return conference
    return "Unknown"

# Example usage
if __name__ == "__main__":
    game_lines = get_gamelines(10)
    for game in game_lines:
        print(f"{game['team1']} vs {game['team2']} | Spread: {game['spread']}")

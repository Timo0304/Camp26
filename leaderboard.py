"""
Leaderboard system for Bible Quiz Game
Stores scores and resets weekly
"""

import json
import os
from datetime import datetime, timedelta
import pandas as pd

LEADERBOARD_FILE = "quiz_leaderboard.json"

def get_current_week():
    """Get current week number (based on Monday as start of week)"""
    today = datetime.now()
    # Get Monday of current week
    start_of_week = today - timedelta(days=today.weekday())
    week_key = start_of_week.strftime("%Y-W%W")
    return week_key, start_of_week

def load_leaderboard():
    """Load leaderboard data from file with error handling"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r") as f:
                content = f.read()
                if content.strip():  # Check if file is not empty
                    return json.loads(content)
                else:
                    # Empty file, return default structure
                    return {"current_week": None, "scores": {}}
        except (json.JSONDecodeError, ValueError) as e:
            # If file is corrupted, create a new one
            print(f"Error reading leaderboard file: {e}. Creating new file.")
            return {"current_week": None, "scores": {}}
    return {"current_week": None, "scores": {}}

def save_leaderboard(data):
    """Save leaderboard data to file"""
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving leaderboard: {e}")

def check_and_reset_week():
    """Check if week has changed and reset leaderboard if needed"""
    try:
        data = load_leaderboard()
        current_week, start_date = get_current_week()
        
        if data.get("current_week") != current_week:
            # New week - reset leaderboard
            data["current_week"] = current_week
            data["scores"] = {}
            data["week_start"] = start_date.strftime("%Y-%m-%d")
            data["week_end"] = (start_date + timedelta(days=6)).strftime("%Y-%m-%d")
            save_leaderboard(data)
            return True  # Reset happened
        return False  # No reset
    except Exception as e:
        print(f"Error in check_and_reset_week: {e}")
        return False

def add_score(player_name, score, level, total_questions=5):
    """Add a player's score to the leaderboard (only keeps highest score per player)"""
    if not player_name or player_name.strip() == "":
        return False
    
    try:
        check_and_reset_week()
        data = load_leaderboard()
        
        player_name = player_name.strip()
        percentage = int((score / total_questions) * 100)
        
        # Only update if this is a higher score than before
        if player_name not in data["scores"] or score > data["scores"][player_name]["score"]:
            data["scores"][player_name] = {
                "name": player_name,
                "score": score,
                "percentage": percentage,
                "level": level,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_leaderboard(data)
            return True
        return False
    except Exception as e:
        print(f"Error in add_score: {e}")
        return False

def get_leaderboard():
    """Get sorted leaderboard for current week"""
    try:
        check_and_reset_week()
        data = load_leaderboard()
        
        if not data.get("scores"):
            return pd.DataFrame(), None
        
        # Convert to list and sort by score (highest first)
        scores_list = list(data["scores"].values())
        scores_list.sort(key=lambda x: x["score"], reverse=True)
        
        df = pd.DataFrame(scores_list)
        week_info = {
            "week_start": data.get("week_start", "Unknown"),
            "week_end": data.get("week_end", "Unknown")
        }
        return df, week_info
    except Exception as e:
        print(f"Error in get_leaderboard: {e}")
        return pd.DataFrame(), None

def get_top_scores(limit=10):
    """Get top N scores for leaderboard"""
    try:
        df, week_info = get_leaderboard()
        if df.empty:
            return [], week_info
        return df.head(limit).to_dict('records'), week_info
    except Exception as e:
        print(f"Error in get_top_scores: {e}")
        return [], None

def get_player_rank(player_name):
    """Get a player's rank in the leaderboard"""
    try:
        df, _ = get_leaderboard()
        if df.empty:
            return None
        
        # Find player's position
        for idx, row in df.iterrows():
            if row["name"].lower() == player_name.lower():
                return idx + 1  # 1-based rank
        return None
    except Exception as e:
        print(f"Error in get_player_rank: {e}")
        return None

def get_weekly_stats():
    """Get statistics for the current week"""
    try:
        df, week_info = get_leaderboard()
        if df.empty:
            return {
                "total_players": 0,
                "average_score": 0,
                "highest_score": 0,
                "perfect_scores": 0,
                "week_start": week_info.get("week_start", "N/A") if week_info else "N/A",
                "week_end": week_info.get("week_end", "N/A") if week_info else "N/A"
            }
        
        return {
            "total_players": len(df),
            "average_score": round(df["score"].mean(), 1),
            "highest_score": df["score"].max(),
            "perfect_scores": len(df[df["score"] == 5]),
            "week_start": week_info.get("week_start", "N/A") if week_info else "N/A",
            "week_end": week_info.get("week_end", "N/A") if week_info else "N/A"
        }
    except Exception as e:
        print(f"Error in get_weekly_stats: {e}")
        return {
            "total_players": 0,
            "average_score": 0,
            "highest_score": 0,
            "perfect_scores": 0,
            "week_start": "N/A",
            "week_end": "N/A"
        }

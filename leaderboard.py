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
    """Load leaderboard data from file"""
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return {"current_week": None, "scores": {}}

def save_leaderboard(data):
    """Save leaderboard data to file"""
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)

def check_and_reset_week():
    """Check if week has changed and reset leaderboard if needed"""
    data = load_leaderboard()
    current_week, start_date = get_current_week()
    
    if data["current_week"] != current_week:
        # New week - reset leaderboard
        data["current_week"] = current_week
        data["scores"] = {}
        data["week_start"] = start_date.strftime("%Y-%m-%d")
        data["week_end"] = (start_date + timedelta(days=6)).strftime("%Y-%m-%d")
        save_leaderboard(data)
        return True  # Reset happened
    return False  # No reset

def add_score(player_name, score, level, total_questions=5):
    """Add a player's score to the leaderboard (only keeps highest score per player)"""
    if not player_name or player_name.strip() == "":
        return False
    
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

def get_leaderboard():
    """Get sorted leaderboard for current week"""
    check_and_reset_week()
    data = load_leaderboard()
    
    if not data["scores"]:
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

def get_top_scores(limit=10):
    """Get top N scores for leaderboard"""
    df, week_info = get_leaderboard()
    if df.empty:
        return [], week_info
    return df.head(limit).to_dict('records'), week_info

def get_player_rank(player_name):
    """Get a player's rank in the leaderboard"""
    df, _ = get_leaderboard()
    if df.empty:
        return None
    
    # Find player's position
    for idx, row in df.iterrows():
        if row["name"].lower() == player_name.lower():
            return idx + 1  # 1-based rank
    return None

def get_weekly_stats():
    """Get statistics for the current week"""
    df, week_info = get_leaderboard()
    if df.empty:
        return {
            "total_players": 0,
            "average_score": 0,
            "highest_score": 0,
            "perfect_scores": 0,
            **week_info
        }
    
    return {
        "total_players": len(df),
        "average_score": round(df["score"].mean(), 1),
        "highest_score": df["score"].max(),
        "perfect_scores": len(df[df["score"] == 5]),
        **week_info
    }

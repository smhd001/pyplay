from find import *
import os
import json

video_dir = "/home/mohammad/Videos/series"
hist_path = "/home/mohammad/projects/PP/python/play/.history"
os.chdir(video_dir)


def load_history(ser_name: str) -> (int, int):
    ser_name = find_dir(ser_name)
    with open(hist_path, "r") as f:
        history = json.load(f)
    if ser_name in history:
        season = history[ser_name]["season"]
        episode = history[ser_name]["episode"]
    else:
        season = 1
        episode = 1
    return season, episode


def save_history(ser_name: str, season: int, episode: int) -> None:
    ser_name = find_dir(ser_name)
    with open(hist_path, "r") as f:
        history = json.load(f)
    history[ser_name] = {"season": season, "episode": episode}
    with open(hist_path, "w") as f:
        json.dump(history, f, indent=4)


def play_form_history(ser_name: str) -> None:
    ser_name = find_dir(ser_name)
    season, episode = load_history(ser_name)
    # play.play(ser_name, season, episode)
    print("playing: ", ser_name, "ep", episode, "season", season)
    save_history(ser_name, season, episode + 1)

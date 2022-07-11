from find import *
import os
import json
import play
video_dir = "/home/mohammad/Videos/series"
hist_path = "/home/mohammad/projects/PP/python/play/.history"
os.chdir(video_dir)
def load_history():
    with open(hist_path, "r") as f:
        return json.load(f)
def save_history(ser_name : str, season : int, episode : int):
    history = load_history()
    history[ser_name] = {"season" : season, "episode" : episode}
    with open(hist_path, "w") as f:
        json.dump(history, f , indent = 4)
def play_form_history(ser_name : str):
    history = load_history()
    ser_name = find_dir(ser_name)
    if ser_name in history:
        season = history[ser_name]["season"]
        episode = history[ser_name]["episode"]
        episode += 1
    else:
        season = 1
        episode = 1
    # play.play(ser_name, season, episode)
    print("playing: ", ser_name,"ep",episode,"season",season)
    save_history(ser_name, season, episode)
    



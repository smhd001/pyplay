from typing import Tuple
from find import find_dir
from pathlib import Path
import json
import os

hist_path = os.path.dirname(__file__) + "/" + ".history"
path = Path(hist_path)
if not path.exists():
    path.touch()
    path.write_text("{}")


def form_history(ser_name: str) -> Tuple[int, int]:
    ser_name = find_dir(ser_name)
    season, episode = load_history(ser_name)
    return season, episode


def load_history(ser_name: str) -> Tuple[int, int]:
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
    history["LAST_SER"] = ser_name
    with open(hist_path, "w") as f:
        json.dump(history, f, indent=4)


def get_last_ser() -> str:
    with open(hist_path, "r") as f:
        history = json.load(f)
    name = history["LAST_SER"]
    return name

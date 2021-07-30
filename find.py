import os
import re
from glob import glob
from os.path import isdir
from typing import Dict


def is_played_before(s_name: str, series:list[Dict] ) -> bool or str:
    for s in series:
        if s_name in s["name"]:
            return s
    return False


def find_dir(name: str) -> str:
    for path in glob("**", recursive=True):
        if name in path and isdir(path):
            name = path
            break
    return name


def find_ep(directory: str,season : int, episode: int) -> str:
    a = []
    print(directory)
    for ep in glob(directory + "/**"):
        if f"{episode:02d}" in ep and is_S_and_E_match(ep,season,episode) and is_video(ep):
            a.append(ep)
    if len(a) == 1:
        return a[0]
    max_c = 0
    s = a[0]
    for ep in a:
        if ep.count(f"{episode:02d}") > max_c:
            max_c = ep.count(f"{episode:02d}")
            s = ep
    return s


def find_path(name: str, season: int, episode: int) -> str:
    directory = find_dir(name)
    if season:
        directory = directory + "/" + "season" + f"{season:02d}"
    return find_ep(directory,season, episode)


def find_sub(name: str, season: int, episode: int) -> list:
    directory = find_dir(name)
    return [x for x in glob(directory + "/" + "**", recursive=True) if is_s_match(name, season) and
            is_sub_file(x) and is_S_and_E_match(x, season, episode)]

    # TODO a better condition like: season01/20.faln.720.srt vs 1.flan.720.str
    # return [x for x in glob(directory + "/" + "**",recursive=True) if is_sub_file(x) and
    #       (x.count(f"{season:02d}") + x.count(f"{episode:02d}")) > 1]


def is_video(name: str) -> bool:
    return (name.endswith(".mkv") or name.endswith(".mp4")) and os.path.isfile(name)


def is_sub_file(name: str) -> bool:
    return name.endswith(".srt") and os.path.isfile(name)


def is_S_and_E_match(name: str, season: int, episode: int) -> bool:
    if s_e := re.findall("[sS]\d+[eE]\d+", name):
        s_e = re.findall("\d+", s_e[0])
        if int(s_e[0]) != season or int(s_e[1]) != episode:
            return False
    return True


def is_s_match(name: str, season: int) -> bool:
    if s := re.findall("[sS]eason\d+", name):
        s = re.findall("\d+", s[0])
        if int(s[0]) != season:
            return False
    return True

import os
import re
from glob import glob
from os.path import isdir

"""
patern of sub

patern s01e02 S1E3 or s01-e02
regex "[sS]\d+-?[eE]\d+"

patern 02x01 
regex \d+x\d+

dir patern 
  s01/  and season01/ season1/ 
"""
"""
TODO
def is_played_before(s_name: str, series:list[Dict] ) -> bool or str:
    for s in series:
        if s_name in s["name"]:
            return s
    return False
"""


def find_dir(name: str) -> str:
    for path in glob("**", recursive=True):
        if name in path.lower() and isdir(path):
            name = path
            break
    return name


def find_ep(directory: str, season: int, episode: int) -> str:
    a = []
    # print(directory)
    for ep in glob(directory + "/**"):
        if (
            f"{episode:02d}" in ep
            and is_S_and_E_match(ep, season, episode)
            and is_video(ep)
        ):
            a.append(ep)
    if len(a) == 1:
        return a[0]
    if len(a) == 0:
        return ""
    max_c = 0
    s = a[0]
    for ep in a:
        if ep.count(f"{episode:02d}") > max_c:
            max_c = ep.count(f"{episode:02d}")
            s = ep
    return s


def find_path(name: str, season: int, episode: int) -> str:
    directory = find_dir(name)
    ep = find_ep(directory + "/" + "season" + f"{season:02d}", season, episode)
    if ep == "":
        ep = find_ep(directory, season, episode)
    if ep is "":
        ep = find_ep(directory + "/" + "season" + f"{season}", season, episode)
    return ep


def find_sub(
    name: str, season: int, episode: int, inc_p: list[str], ex_p: list[str]
) -> list:
    directory = find_dir(name)
    subs = []
    for x in glob(directory + "/" + "**", recursive=True):
        if (
            is_s_match(x, season)
            and is_sub_file(x)
            and is_S_and_E_match(x, season, episode)
        ):
            if not any(p in x.lower() for p in ex_p):
                if all(p in x.lower() for p in inc_p):
                    subs.append(x)
    return subs


def is_video(name: str) -> bool:
    return (name.endswith(".mkv") or name.endswith(".mp4")) and os.path.isfile(name)


def is_sub_file(name: str) -> bool:
    return (
        name.lower().endswith(".srt") or name.lower().endswith(".ass")
    ) and os.path.isfile(name)


def is_S_and_E_match(name: str, season: int, episode: int) -> bool:
    if s_e := re.findall("[sS]\d+-?[eE]\d+", name):
        s_e = re.findall("\d+", s_e[0])
        if int(s_e[0]) != season or int(s_e[1]) != episode:
            return False

    if s_e := re.findall("\d+x\d+", name):
        s_e = re.findall("\d+", s_e[0])
        if int(s_e[0]) != season or int(s_e[1]) != episode:
            return False

    return True


def is_s_match(name: str, season: int) -> bool:
    if s := re.findall("[sS]eason\d+", name):
        s = re.findall("\d+", s[0])
        if int(s[0]) != season:
            return False
    for dirs in name.split("/"):
        if s_e := re.findall("^[sS]\d+", dirs):
            s_e = re.findall("\d+", s_e[0])
            if int(s_e[0]) != season:
                return False
    return True
    # if s_e := re.findall("[sS]\d+", name):
    #     s_e = re.findall("\d+", s_e[0])
    #     if int(s_e[0]) != season :
    #         return False

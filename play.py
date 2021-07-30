import json
import os
import subprocess
import sys
from os.path import expanduser
from find import find_path, find_sub


def dmenu_chose(s: list) -> str:
    subs = ""
    for i in s:
        subs += i
        subs += "\n"
    a = os.popen("echo " + "\"" + subs[:-1] + "\"" + "|" + "dmenu")
    return a.read()[:-1]


def play(name: str, season: int, episode: int):
    path = find_path(name, season, episode)
    print(path)
    # path = find_path(name, 0, int(sys.argv[2]))
    if is_sub:
        sub_list = find_sub(name, season, episode)
        if sub_list:
            if len(sub_list) > 1:
                sub_list[0] = dmenu_chose(sub_list)
            subprocess.run([player, path,*options, "--sub-file=" + sub_list[0]])
            return
    subprocess.run([player,path,*options])


def main():
    print(sys.argv[0][:-7])
    play(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))


if __name__ == "__main__":
    with open(sys.argv[0][:-7] + ".data.json") as f:
        data = json.load(f)
    conf = data["conf"]
    print(conf)
    video_dir = expanduser(conf["video_dir"])
    os.chdir(video_dir)
    player = conf["player"]
    options = conf["options"]
    if conf["is_full_screen"]:
       options.append("--fs")
    print(options)
    is_sub = conf["open_sub"]
    main()

#!/bin/python3
import json
import os
import subprocess
import sys
from os.path import expanduser
from typing import Tuple
from find import find_path, find_sub
from history import form_history, save_history, get_last_ser

debug = True
# TODO
"""
    1. add sub_inc
    2. add sub_exc
    3. add history
    4. add overriding config with args
    5. sub_exc and sub_exc should be case insensitive
"""


# bug  pl office 7 23
def menu_chose(s: list) -> str:
    subs = ""
    for i in s:
        subs += i
        subs += "\n"
    ans = os.popen(
        "echo " + '"' + subs[:-1] + '"' + "|" + menu_program + " " + menu_args
    )
    return ans.read()[:-1]


def print_info(path: str, sub: str = "no sub") -> None:
    print()
    print("#####***************************************#####")
    print()
    print()
    print("playing: ", path)
    print()
    print("sub:", sub)
    print()
    print("options:", options)
    print()
    print()
    print("#####***************************************#####")
    print()


def arg_parse(args: list[str]) -> Tuple[str, int, int, list[str], list[str]]:
    global options
    if "-ex" in args:
        ex = args[args.index("-ex") + 1]
        ex = ex.split(",")
        del args[args.index("-ex") : args.index("-ex") + 2]
    else:
        ex = []
    if "-inc" in args:
        inc = args[args.index("-inc") + 1]
        inc = inc.split(",")
        inc = [s.lower() for s in inc]
        del args[args.index("-inc") : args.index("-inc") + 2]
    else:
        inc = []
    if "-p" in args:
        previous = True
        del args[args.index("-p")]
    else:
        previous = False
    if "-n" in args:
        next = True
        del args[args.index("-n")]
    else:
        next = False
    if "-ns" in args:
        next_season = True
        del args[args.index("-ns")]
    else:
        next_season = False
    if "--" in args:
        options += args[args.index("--") + 1 :]
        del args[args.index("--") :]
    if len(args) <= 1:
        name = get_last_ser()
        print("-------------------------------------------------")
        print("#")
        print("# play last played serie: ", name)
        print("#")
    else:
        name = args[1]
    if len(args) <= 2:
        season, episode = form_history(name)
        if previous:
            episode -= 1
        if next:
            episode += 1
        if next_season:
            season += 1
            episode = 1
        print("-------------------------------------------------")
        print("#")
        print(f"# playing from history: {episode = } {season = }")
        print("#")
    else:
        season, episode = int(args[2]), int(args[3])
    return name, season, episode, inc, ex


def play(
    name: str, season: int, episode: int, inc_p: list[str], ex_p: list[str]
) -> subprocess.CompletedProcess[bytes]:
    path = find_path(name, season, episode)
    if path == "":
        print(f"tried to fiind {name=} {season=} {episode=}")
        raise FileNotFoundError("file not found")
    if is_sub:
        sub_list = find_sub(name, season, episode, inc_p, ex_p)
        if sub_list:
            if len(sub_list) > 1 and chose_sub:
                sub_list[0] = menu_chose(sub_list)
            if sub_list[0]:
                print_info(path, sub_list[0])
                return subprocess.run(
                    [player, path, *options, "--sub-file=" + sub_list[0]],
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
    print_info(path)
    return subprocess.run(
        [player, path, *options],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )


def main():
    name, season, episode, inc, ex = arg_parse(sys.argv)
    process = play(name, season, episode, inc, ex)
    std_out = process.stdout.decode("utf-8")
    print(std_out)
    exit_status = std_out.split("\n")[-2]
    if exit_status == "Exiting... (End of file)":
        save_history(name, season, episode + 1)
    else:
        save_history(name, season, episode)


if __name__ == "__main__":
    # open config file
    with open(os.path.dirname(__file__) + "/conf.json") as f:
        data = json.load(f)
    conf = data["conf"]
    print(conf)
    video_dir = expanduser(conf["video_dir"])
    os.chdir(video_dir)
    player = conf["player"]
    options = conf["options"]
    if conf["is_full_screen"]:
        options.append("--fs")
    is_sub = conf["open_sub"]
    chose_sub = conf["chose_sub"]
    menu_args = " ".join(conf["menu_options"])
    menu_program = conf["menu_program"]
    main()

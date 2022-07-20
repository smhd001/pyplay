#!/bin/python3
import json
import os
import subprocess
import sys
from os.path import expanduser
from find import find_path, find_sub
from history import form_history, save_history

debug = False
# TODO
"""
    1. add sub_inc
    2. add sub_exc
    3. add history
    4. add overiding config witth args
"""

# bug  pl office 7 23
def menu_chose(s: list) -> str:
    subs = ""
    for i in s:
        subs += i
        subs += "\n"
    a = os.popen("echo " + '"' + subs[:-1] + '"' + "|" + m_program + " " + m_args)
    return a.read()[:-1]


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


def play(
    name: str, season: int, episode: int, inc_p: list[str], ex_p: list[str]
) -> None:
    path = find_path(name, season, episode)
    if path == "":
        raise FileNotFoundError("file not found")
    if is_sub:
        sub_list = find_sub(name, season, episode, inc_p, ex_p)
        # print(sub_list)
        if sub_list:
            if len(sub_list) > 1:
                if is_chose_sub:
                    sub_list[0] = menu_chose(sub_list)
                if not sub_list[0]:
                    print_info(path)
                    subprocess.run([player, path, *options])
                    return
            print_info(path, sub_list[0])
            subprocess.run([player, path, *options, "--sub-file=" + sub_list[0]])
            return
    print_info(path)
    subprocess.run([player, path, *options])


def main():
    try:
        if "-ex" in sys.argv:
            ex = sys.argv[sys.argv.index("-ex") + 1]
            ex = ex.split(",")
            del sys.argv[sys.argv.index("-ex") : sys.argv.index("-ex") + 2]
        else:
            ex = ""
        if "-inc" in sys.argv:
            inc = sys.argv[sys.argv.index("-inc") + 1]
            inc = inc.split(",")
            del sys.argv[sys.argv.index("-inc") : sys.argv.index("-inc") + 2]
        else:
            inc = ""
        if "-r" in sys.argv:
            replay = True
            del sys.argv[sys.argv.index("-r")]
        else:
            replay = False
        if len(sys.argv) <= 2:
            season, episode = form_history(sys.argv[1], replay)
        else:
            season, episode = int(sys.argv[2]), int(sys.argv[3])
        play(sys.argv[1], season, episode, inc, ex)
        save_history(sys.argv[1], season, episode)
    except FileNotFoundError as e:
        if debug:
            import traceback

            traceback.print_exc()
            print(e)
        print("file not found")
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(e)


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
    print(options)
    is_sub = conf["open_sub"]
    is_chose_sub = conf["is_chose_sub"]
    m_args = " ".join(conf["menu_options"])
    m_program = conf["menu_program"]
    main()

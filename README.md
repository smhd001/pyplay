# pyplay
This script search through your disk and find episode you want and play it with mpv,
it also searches for subtitle 
## usage:
``./play.py frin 1 10``
play 10th episode of 1th season of friends

if there is multiple matching subtitle it open dmenu to choose which one to display

``./play.py offi 5 5 -exc blueray -inc 1080`` 
(exclude every subtitles with bluray in it's name and only include subtitles with 1080 in their name)
### history:
pyplay remember last episode for each series

``./play.py fir`` plays last played episode of friends

``./play.py`` (plays last episode of last palyed series)

If you reach end of file pyplay will & play next episod next time
## install
clone this repo
set directory to seach in conf.json
set other config options as you desire
creat empety .history file

``ecoh {} > .history``
## to do
- [ ] better doc and readme
- [ ] Add Features,Demo sections
- [ ] Standalone builds (release section ...)

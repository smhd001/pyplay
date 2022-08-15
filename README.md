# pyplay
this script seach through your disk and find episod you want and play it with mpv
it also search for subtitle 
## usage:
``./play.py frin 1 10``
play 10th episod of 1th season of frinds

if there is multiple matching subtitle it open dmenu to chose which one to display
``./play.py offi 5 5 -exc blueray -inc 1080`` 
(exclude every subtitles with bluray in it's name and only include subtitles with 1080 in their name)
### history:
pyplay rember last episod for each seri

``./play.py fir`` played last played episod of friends

``./play.py`` (play last episod of last palyed serie)

if you reach end of file pyplay will & play next episod next time
## install
clone this repo
set directory to seach in conf.json
set other config options as you desire
creat empety .history file

``ecoh {} > .history``
## to do
- [ ] better doc and readme

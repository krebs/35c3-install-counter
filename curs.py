#!/usr/bin/env nix-shell
#!nix-shell -p python3Packages.matrix-client python3Packages.pyfiglet python3Packages.pyserial python3Packages.docopt -i python3
""" usage: curs [options]

Options:
    --input=MODE  input mode (serial|space) [Default: serial]
    --device=DEV  input device for serial [Default: /dev/ttyUSB0]
    --font=font   font to use for the "thank you" [Default: standard]
    --token=TOKEN   matrix.org access token, if unset no announce will be performed
    --room=CHAN  matrix.org channel to write to [Default: #freenode_#krebsbots:matrix.org]
"""
from curses import wrapper,curs_set
from time import sleep
import serial, json
from pyfiglet import Figlet
from docopt import docopt
from random import choice
# from makefu/events-publisher
def announce(text, token, room=None):
    from matrix_client.api import MatrixHttpApi
    matrix = MatrixHttpApi("https://matrix.org",token=token)
    matrix.sync()
    roomid = matrix.get_room_id(room)
    matrix.join_room(roomid)
    matrix.send_message(roomid,text)


def printlogo(scr):
    height,width = scr.getmaxyx()
    logosize = 120
    center = int((width-logosize)/2)
    indent = " "*center
    scr.addstr(0,0,f'''
{indent}         sMMm.    :NMMM+   yMMd`
{indent}         +MMMN:    -mMMMs`dMMMh`
{indent}          :NMMM/    `dMMMMMMMs
{indent}     -mmmmmNMMMMmmmmmddMMMMM+    `/            `ddd+          dd/    --                      ./osyso/.         :+syyys+.
{indent}    /MMMMMMMMMMMMMMMMMmhMMMN-   -mMy           .MMMMy        `MM+   +MMy                   /dMNhsosyNMmo`    +NMmsoooymo
{indent}    ``````-hddd+````````/MMMM/ :NMMM:          .MMsNMd.      `MM+    ::`                 `hMN+       :mMm.  +MMo
{indent}         -NMMMo          -NMMNsMMMN:           .MM/.dMN:     `MM+   .ss- `oss`     /ss.  yMN-         `mMm  yMM-
{indent}`+++++++oMMMM/            .mmdMMMMyoooo-       .MM/ `yMMo    `MM+   :MM+  .dMm-   sMN:  .MMs           :MM/ -NMNo.
{indent}hMMMMMMMMMMN/              .dMMMMMMMMMMN`      .MM/   +MMy`  `MM+   :MM+    sMM/`dMh`   :MM/           `MMs  `omMMNho-
{indent}`+++ooNMMMmdM/            .mMMMy+++++++-       .MM/    -NMm. `MM+   :MM+     /NMNMo     -MM+           -MMo     `:odMMd-
{indent}    `dMMMhhMMMo          :NMMM+                .MM/     `dMN:`MM+   :MM+     .mMMm-      mMd           sMM.         :MMm
{indent}   `mMMMs .dMMMy`.......:dmmm+......           .MM/       sMM/MM+   :MM+    /NM+oMM+     :MMy         +MMo          `NMm
{indent}    :NM+   `hMMMmdMMMMMMMMMMMMMMMMMs           .MM/        /MMMM+   :MM+   sMN-  /NMy`    -dMmo-` `-+dMN/  -y+-.``-+mMm-
{indent}     -:    -mMMMMNhmmmmmNMMMMmmmmm+            `mm:         -dmm/   -mm/ `ymh.    .dmh`     :sdMMMMMmy/    -ymNMMMNmy/
{indent}          :NMMMMMMN:    .mMMMy                                                                  ```             `
{indent}         oMMMN::NMMM+    `hMMMh`
{indent}         oMMm.  .mMMMy     yMMd`''')
def buttonPressed(ser):
    data = ser.read(1024).decode()
    return "HIGH" in data

def incrementCounter(count):
    with open("installcounter","w+") as f:
        json.dump({"count":count + 1},f)
        return count + 1

def loadInstallCount():
    try:
        with open("installcounter") as f:
            return json.load(f)["count"]
    except:
        return 0

def thankYou(scr,count,font='standard',extra=""):
    height, width = scr.getmaxyx()
    text = Figlet(font,width=width,justify="center").renderText(f"Congratulations !\nInstallation Number {count} !\n\n{extra}")
    twidth = max([len(l) for l in text.splitlines()])
    theight = len(text.splitlines())
    scr.addstr(int((height - theight)/2), 0, text)
    pass

def main(scr):
    # Clear screen
    args = docopt(__doc__)
    font = args['--font']
    input = args['--input']
    device = args['--device']
    token = args['--token']
    room = args['--room']
    height,width = scr.getmaxyx()
    scr.clear()
    curs_set(0)
    ser = False
    count = loadInstallCount()
    while True:
        if input == "serial":
            try:
                if not ser:
                    ser = serial.Serial(device, 115200, timeout=1)
                pressed = buttonPressed(ser)
            except serial.SerialException as e:
                scr.addstr(int(height/2),0,f"--- {e} ---")
                sleep(1)
                continue
        elif input == "space":
            scr.nodelay(True)
            c = scr.getch()
            pressed = c == ord(' ')
        else:
            raise Exception(f"Unknown input {input}")

        if pressed:
            count = incrementCounter(count)
            scr.clear()
            distros = [
                    "ArchLinux",
                    "Gentoo",
                    "Ubuntu",
                    "VoidLinux",
                    "LinuxFromScratch",
                    "Debian",
                    "Manjaro",
                    "Linux Mint",
                    "ElementaryOS",
                    "Hannah Montana Linux",
                    "FreeBSD",
                    "Slackware",
                    "IBM RedHat",
                    "IBM Fedora"
                    ]
            ending = [
                    # " Rejoice!",
                    # " Soon...",
                    ".. Worth it 👍",
                    " error: cannot coerce an integer to a string, at unknown position"
                   f" Surely was using {choice(distros)} before",
                   f" {choice(distros)}--; NixOS++",
                   f" NixOS {count} : 0 {choice(distros)}",
                   f" Another {choice(distros)} User just got enlightened",
                   f" Another {choice(distros)} User finally sees the truth",
                   f" The next {choice(distros)} User chose another class of issues to solve instead of fighting the same problems over and over again"
            ]
            thisEnding=choice(ending)
            thankYou(scr,count,font,thisEnding)
            scr.refresh()
            if token:
                announce(f"35C3 NixOS Installation number *{count}* just completed.{thisEnding}"
                        ,token,room=room)
            sleep(10)
            scr.clear()
            # cleanup input buffer after 10s
            if input == "serial":
                ser.read(1024)
            elif input == "space":
                while (scr.getch() is not -1): pass
        logo(scr,count,font)

        scr.refresh()
        sleep(0.1)


def logo(scr,count,font):
    height,width = scr.getmaxyx()
    num = min(height,width)
    text = Figlet(font,width=width-1,justify="center").renderText(f"Installations : {count}")
    printlogo(scr) #logo height: 17
    scr.addstr(23, 0, text)

wrapper(main)

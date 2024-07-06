#!/usr/bin/python
from subprocess import Popen, PIPE
import re
from base64 import b64decode
from sys import exit

with Popen(["playerctl", "-l"], stdout=PIPE) as p:
	players = p.communicate()[0].decode("utf8").strip().split("\n")

if len(players) == 0 or (len(players) == 1 and players[0] == ''):
	print("No players to select")
	exit(0)

imgs: dict[str, str] = {}
titles: dict[str, str] = {}
for player in players:
	with Popen(["playerctl", "metadata", "-p", player], stdout=PIPE) as p:
		metadata = p.communicate()[0].decode("utf8").strip().split("\n")
	
	for line in metadata:
		if "mpris:artUrl" in line:
			img = line.split("mpris:artUrl")[1].strip()
			
			if img.startswith("data:"):
				regex = r"data:image\/(\w*?);base64,(.+)"
				matches = re.search(regex, img)
				if matches:
					fp = f"/tmp/{player}.{matches.group(1)}"
					with open(fp, "wb+") as f:
						f.write(b64decode(matches.group(2)))
					imgs[player] = fp
				else:
					print("unknown data:", img)
			elif img.startswith("file://"):
				imgs[player] = img[7:]
			
		if "xesam:title" in line:
			titles[player] = line.split("xesam:title")[1].strip()

# generating wofi options

options: list[str] = []

for player in players:
	option = player
	
	if player in imgs.keys():
		option = f"img:{imgs[player]}:text:{option}"
	
	if player in titles.keys():
		option = f"{option}&#10;{titles[player]}"
	
	options.append(option)

# showing wofi

with Popen(
	[
		"wofi",
		"-I",
		"--show=dmenu",
		"--style=.config/wofi/musicselect.css",
		f"--lines={len(players)+1}",
		"-W", "50%",
		"-b",
		"-D", "hide_search=true",
		"-D", "image_size=64",
		"-m",
		"--cache-file=/dev/null",
	],
	stdout=PIPE, stdin=PIPE) as p:
	selection = p.communicate("\n".join(options).encode("utf8"))[0].decode("utf8").strip()

# selecting new player

if selection in options:
	newplayer = players[options.index(selection)]
	
	Popen(["playerctl", "-a", "pause"], stdout=PIPE).wait()
	Popen(["playerctl", "-p", newplayer, "play"], stdout=PIPE).wait()

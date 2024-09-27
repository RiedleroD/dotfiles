#!/usr/bin/bash

# partly copied from https://github.com/Horus645/swww/blob/main/example_scripts/swww_randomize.sh
# meant to be run in sway.conf

# Edit below to control the images transition
export SWWW_TRANSITION_FPS=60
export SWWW_TRANSITION_STEP=255

# making sure only one wallplaster is running at a time

LOCKFILE=/tmp/.wallplaster_id

if [[ -f "$LOCKFILE" ]];then
	prevpid=$(cat "$LOCKFILE");
	kill $prevpid
	#wait for process to be killed
	while kill SIGTERM $prevpid 2>/dev/null; do sleep 0.25; done;
	rm /tmp/.wallplaster_id
	echo "killed previously running instance"
fi

# starting swww if not started already
swwwsock="/run/user/$(id -u $USER)/swww-$WAYLAND_DISPLAY.socket"
if [[ ! -e "$swwwsock" ]];then
	swww-daemon & # yeah why not, fuck it
fi

#put current pid in lockfile so it can be terminated when the script is started again
echo $$ > "$LOCKFILE"

#removing the lockfile when the script is terminated
trap 'rm /tmp/.wallplaster_id' EXIT

# This controls (in seconds) when to switch to the next image
INTERVAL=$((5 * 60))

while true; do
	find ~/Pictures/wallpapers/* \
		| sort -R | head -n1 \
		| xargs swww img --transition-type wipe
	sleep 300
done

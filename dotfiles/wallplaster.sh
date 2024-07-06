#!/usr/bin/bash

# partly copied from https://github.com/Horus645/swww/blob/main/example_scripts/swww_randomize.sh
# meant to be run in sway.conf

# Edit below to control the images transition
export SWWW_TRANSITION_FPS=60
export SWWW_TRANSITION_STEP=255

#making sure only one is running at a time

LOCKFILE=/tmp/.wallplaster_id

if test -f "$LOCKFILE";then
	prevpid=$(cat "$LOCKFILE");
	kill $prevpid
	#wait for process to be killed
	while kill -0 $prevpid 2>/dev/null; do sleep 0.25; done;
	echo "killed previously running instance"
fi

#put current pid in lockfile so it can be terminated when the script is started again
echo $$ > "$LOCKFILE"

#stopping swww and removing the lockfile when the script is terminated
trap 'rm /tmp/.wallplaster_id' EXIT

# This controls (in seconds) when to switch to the next image
INTERVAL=$((5 * 60))

while true; do
	find ~/Pictures/wallpapers/* \
		| while read -r img; do
			echo "$((RANDOM % 1000)):$img"
		done \
		| sort -n | cut -d':' -f2- \
		| while read -r img; do
			swww img "$img" --transition-type wipe
			sleep $INTERVAL
		done
done

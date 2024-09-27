#!/usr/bin/bash

set -euo pipefail
screeninfo=$(swaymsg --pretty -t get_outputs | grep "focused" -A 10)
screenid=$(echo "$screeninfo" | head -n1 | sed -E 's/Output ([^ ]+) .+/\1/')
curscale=$(echo "$screeninfo" | grep "Scale factor:" | grep -oP '\d+(\.\d+)?')

echo "screen: $screenid"
echo "curscale: $curscale"
scale=$curscale # init

if [ "$1" == '+' ]; then
	scale=$(bc -l <<< "${curscale} * 1.1")
elif [ "$1" == '-' ]; then
	scale=$(bc -l <<< "${curscale} / 1.1")
elif [ "$1" == '=' ]; then
	scale="1.75"
fi
	
if [[ $(bc <<< "${scale} < 5") == $(bc <<< "${scale} > 0.25") ]]; then
	swaymsg "output * scale ${scale}"
	echo "new scale: ${scale}"
else
	echo "new scale outside 0.25-5 boundaries: ${scale}"
fi

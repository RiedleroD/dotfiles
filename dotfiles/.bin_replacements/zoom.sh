#!/usr/bin/bash

set -euo pipefail
curscale=$(swaymsg -t get_outputs | jq -r '.. | select(.focused?) | .scale')

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

#!/usr/bin/sh

# pretty simple screenshot thing, but still handy

filename="$(date +%s).png"
filepath="$HOME/Pictures/screenshots/$filename"

grim -g "$(slurp)" -l 9 "$filepath"
wl-copy < "$filepath"

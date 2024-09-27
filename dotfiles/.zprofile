source ./.rev

# start sway if tty1 and no DISPLAY set yet
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  source ./.rev_wayland
  exec sway
fi

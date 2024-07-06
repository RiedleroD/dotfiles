source ./.rev
if [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  source ./.rev_wayland
  exec sway
fi

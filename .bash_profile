source ~/.rev
if systemctl -q is-active graphical.target && [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  # add local bin folder to PATH
  export PATH=/home/riedler/.bin_replacements:/home/riedler/.local/bin:$PATH
  source ~/.rev_wayland
  exec sway
fi

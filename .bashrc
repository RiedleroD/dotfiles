#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

source ~/.rev

if [ -z "${WAYLAND_DISPLAY}" ];
then #X11-specific shit
  echo "enabled X11-specific shit"
else #wayland-specific shit
  echo "enabled wayland-specific shit"
  source ~/.rev_wayland
fi

# aliases for common programs
alias rytd="python3 ~/Music/RYTD/rytd.py"
#kittens
alias diff="kitty +kitten diff"

# custom PS1
PS1='\[\e[34m\]\h\[\e[33m\]\w\[\e[39m\]\$ '


# BEGIN_KITTY_SHELL_INTEGRATION
if test -n "$KITTY_INSTALLATION_DIR" -a -e "$KITTY_INSTALLATION_DIR/shell-integration/bash/kitty.bash"; then source "$KITTY_INSTALLATION_DIR/shell-integration/bash/kitty.bash"; fi
# END_KITTY_SHELL_INTEGRATION
#
# ~/.bashrc
#

source ~/.rev

if [ -z "${WAYLAND_DISPLAY}" ]; then #X11-specific shit
  echo "X11 doesn't have its own .rev"
else #wayland-specific shit
  source ~/.rev_wayland
fi
echo "Welcome to bash!" >&2

# custom PS1
PS1='\[\e[34m\]\h\[\e[33m\]\w\[\e[39m\]\$ '
# ignore duplicate entries in command history
export HISTCONTROL=ignoreboth:erasedups

# BEGIN_KITTY_SHELL_INTEGRATION
if test -n "$KITTY_INSTALLATION_DIR" -a -e "$KITTY_INSTALLATION_DIR/shell-integration/bash/kitty.bash"; then
  source "$KITTY_INSTALLATION_DIR/shell-integration/bash/kitty.bash"
fi
# END_KITTY_SHELL_INTEGRATION

printf "\n"

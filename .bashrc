#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

# fuck vim
export VISUAL="kate -b"
export EDITOR=nano
#ignore duplicate entries in command history
export HISTCONTROL=ignoreboth:erasedups
#gtk rocks, qt sucks
export QT_QPA_PLATFORMTHEME=qt5ct
#need this for some reaon (commented out for hardware compat)
#export LIBVA_DRIVER_NAME=i965
#canberra please?
export GTK_MODULES="canberra-gtk-module"
#jawa awt needs this
export _JAVA_AWT_WM_NONREPARENTING=1
#the only correct tab size
tabs 4
#no clang please
export CC=gcc CXX=g++
#yes sccache please
export RUSTC_WRAPPER=sccache
#SDL should use alsa bc jack is wack
export SDL_AUDIODRIVER=alsa

if [ -z ${WAYLAND_DISPLAY} ];
then #X11-specific shit
  echo "enabled X11-specific shit"
else #wayland-specific shit
  echo "enabled wayland-specific shit"
  #pipewire needs this
  export XDG_CURRENT_DESKTOP=sway
  #setting some backends to wayland
  export GDK_BACKEND=wayland
  export MOZ_ENABLE_WAYLAND=1
  export QT_QPA_PLATFORM=wayland-egl
fi

# aliases for common programs
alias rytd="python3 ~/Music/RYTD/rytd.py"
alias ls=exa
#kittens
alias diff="kitty +kitten diff"

# custom PS1
PS1='\[\e[34m\]\h\[\e[33m\]\w\[\e[39m\]\$ '
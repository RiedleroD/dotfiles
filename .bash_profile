if systemctl -q is-active graphical.target && [[ ! $DISPLAY && $XDG_VTNR -eq 1 ]]; then
  # add local bin folder to PATH
  export PATH=/home/riedler/.bin_replacements:/home/riedler/.local/bin:$PATH
  # fuck vim
  export VISUAL="kate -b"
  export EDITOR=nano
  #canberra please?
  export GTK_MODULES="canberra-gtk-module"
  #need this for some reaon (commented out for hardware compat)
  #export LIBVA_DRIVER_NAME=i965
  #ignore duplicate entries in command history
  export HISTCONTROL=ignoreboth:erasedups
  #gtk rocks, qt sucks
  export QT_QPA_PLATFORMTHEME=qt5ct
  #Many java swing apps need this (IntelliJ, Eclipse, Emulicious)
  export _JAVA_AWT_WM_NONREPARENTING=1
  #gtk3 needs that
  export XDG_CONFIG_HOME=/home/riedler/.config
  #set VDPAU driver for hardware acceleration (commented out for hardware compat)
  #export VDPAU_DRIVER=va_gl
  #setting qt platform
  export QT_QPA_PLATFORM=wayland-egl
  #pipewire needs this
  export XDG_CURRENT_DESKTOP=sway
  #some wayland shit
  export GDK_BACKEND=wayland
  export MOZ_ENABLE_WAYLAND=1
  #the only correct tab size
  tabs 4
  #no clang please
  export CC=gcc CXX=g++
  #alsa please
  export SDL_AUDIODRIVER=alsa
  exec sway
fi
paru -S xdg-user-dirs sway waybar waylock xorg-xwayland qtile kitty \
libertinus-font libcanberra otf-font-awesome opendoas bemenu bemenu-wayland \
dex pcmanfm brightnessctl nwg-menu deadbeef-git exa lxappearance qt5ct \
kvantum kvantum-theme-arc arc-gtk-theme papirus-icon-theme deepin-icon-theme \
pipewire pipewire-pulse pipewire-jack-dropin pipewire-alsa pipewire-v4l2 \
pipewire-media-session helvum gst-plugin-pipewire youtube-dl flameshot \
ttf-joypixels opusfile engrampa p7zip unrar discord_arch_electron \
steam-native-runtime teams-for-linux gimp libreoffice-fresh gthumb inkscape \
google-chrome chromium firefox icaclient geogebra gummi wxmaxima typora-free \
audacity carla obs-studio wlrobs lmms pavucontrol timidity++ vlc alacritty \
htop base-devel git cmake qt5-base qt5-tools qt5-x11extras libsndfile fftw \
libvorbis lame libsamplerate libogg wine stk fluidsynth fltk libgig jack2 sdl \
alsa-lib portaudio perl-list-moreutils perl-exporter-tiny perl-xml-parser \
sfarkxtc mako wireplumber grim --needed

systemctl --user enable wireplumber

python -m ensurepip
pip3 install mutagen

echo "reboot after this."
paru -S xdg-user-dirs sway waybar waylock xorg-xwayland kitty libertinus-font \
libcanberra otf-font-awesome opendoas bemenu bemenu-wayland dex pcmanfm-gtk3 \
brightnessctl nwg-menu deadbeef-git deadbeef-pipewire-plugin-git exa qt5ct \
lxappearance kvantum kvantum-theme-arc arc-gtk-theme papirus-icon-theme \
deepin-icon-theme pipewire pipewire-pulse pipewire-jack pipewire-alsa \
pipewire-v4l2 wireplumber helvum gst-plugin-pipewire youtube-dl flameshot \
ttf-joypixels opusfile engrampa p7zip unrar discord_arch_electron gimp inkscape \
steam-native-runtime teams-for-linux libreoffice-fresh gummi typora-free \
google-chrome chromium firefox tenacity-git carla obs-studio pavucontrol lmms \
vlc timidity++ htop base-devel git cmake qt5-base qt5-tools qt5-x11extras fftw \
libsndfile libvorbis lame libsamplerate libogg wine stk fluidsynth libgig sdl \
fltk alsa-lib perl-list-moreutils sfarkxtc mako imv blueman gnome-themes-extra \
gtk-engine-murrine gvfs-smb gvfs-mtp gvfs-nfs network-manager-applet --needed

systemctl --user enable wireplumber
sudo systemctl enable --now bluetooth

python -m ensurepip
pip3 install mutagen

echo "reboot after this."
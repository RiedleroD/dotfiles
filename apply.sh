#!/usr/bin/sh
mkdir ~/.bin_replacements
cp .bash_profile ~/.bash_profile
cp .bashrc ~/.bashrc

mkdir ~/.config/kitty ~/.config/qtile ~/.config/sway ~/.config/waybar \
~/.config/qt5ct/qss ~/.config/Kvantum/ArcDark# ~/.config/gtk-2.0 \
~/.config/gtk-3.0 -p
cp kitty.conf ~/.config/kitty/kitty.conf
cp qtile.config.py ~/.config/qtile/config.py
cp sway.conf ~/.config/sway/config
cp waybar.conf ~/.config/waybar/config
cp waybar.css ~/.config/waybar/style.css
cp qt5ct.conf ~/.config/qt5ct/qt5ct.conf
cp qt5ct_spinboxes.qss ~/.config/qt5ct/qss/spinboxes.qss
cp kvantum.kvconfig ~/.config/Kvantum/kvantum.kvconfig
cp ArcDark.kvconfig ~/.config/Kvantum/ArcDark#/ArcDark#.kvconfig
cp .gtkrc-2.0 ~/.gtkrc-2.0
cp gtk2-filechooser.ini ~/.config/gtk-2.0/gtkfilechooser.ini
cp gtk3.ini ~/.config/gtk-3.0/settings.ini
cp pcmanfm.conf ~/.config/pcmanfm/default/pcmanfm.conf
doas cp makepkg.conf /etc/makepkg.conf

mkdir /home/riedler/Pictures -p
curl https://i.imgur.com/2kyvrtg.png > /home/riedler/Pictures/wallpaper.png
curl https://i.imgur.com/e2rqx1O.jpg > /home/riedler/Pictures/wallpaper.jpg

echo "Make sure you installed the dependencies!"
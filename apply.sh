#!/usr/bin/sh
mkdir ~/.bin_replacements
cp .bash_profile ~/.bash_profile
cp .bashrc ~/.bashrc

mkdir ~/.config/kitty ~/.config/qtile ~/.config/sway ~/.config/waybar ~/.config/qt5ct/qss ~/.config/Kvantum/ArcDark# -p
cp kitty.conf ~/.config/kitty/kitty.conf
cp qtile.config.py ~/.config/qtile/config.py
cp sway.conf ~/.config/sway/config
cp waybar.conf ~/.config/waybar/config
cp waybar.css ~/.config/waybar/style.css
cp qt5ct.conf ~/.config/qt5ct/qt5ct.conf
cp qt5ct_spinboxes.qss ~/.config/qt5ct/qss/spinboxes.qss
cp kvantum.kvconfig ~/.config/Kvantum/kvantum.kvconfig
cp ArcDark.kvconfig ~/.config/Kvantum/ArcDark#/ArcDark#.kvconfig
doas cp makepkg.conf /etc/makepkg.conf

mkdir /home/riedler/Pictures -p
curl https://i.imgur.com/2kyvrtg.png > /home/riedler/Pictures/wallpaper.png
curl https://i.imgur.com/e2rqx1O.jpg > /home/riedler/Pictures/wallpaper.jpg

echo "Make sure you installed the dependencies!"
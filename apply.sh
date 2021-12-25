#!/usr/bin/sh
mkdir ~/.config/kitty ~/.config/qtile ~/.config/sway ~/.config/waybar -p
cp kitty.conf ~/.config/kitty/kitty.conf
cp qtile.config.py ~/.config/qtile/config.py
cp sway.conf ~/.config/sway/config
cp waybar.conf ~/.config/waybar/config
cp waybar.css ~/.config/waybar/style.css
doas cp makepkg.conf /etc/makepkg.conf

curl https://i.imgur.com/2kyvrtg.png > /home/riedler/Pictures/wallpaper.png
curl https://i.imgur.com/e2rqx1O.jpg > /home/riedler/Pictures/wallpaper.jpg

echo "Make sure you installed the dependencies!"
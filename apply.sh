#!/usr/bin/sh

#custom executables (mostly rerouting and fixed args)
cp .bin_replacements ~/.bin_replacements -r
chmod -w ~/.bin_replacements -R #for security
#making sure all the folders exist
mkdir ~/.config/kitty ~/.config/qtile ~/.config/sway ~/.config/waybar \
~/.config/qt5ct/qss ~/.config/Kvantum/ArcDark# ~/.config/gtk-2.0 \
~/.config/gtk-3.0 ~/.config/flameshot -p
#shell configs
cp .bash_profile ~/.bash_profile
cp .bashrc ~/.bashrc
#WM configs
cp qtile.config.py ~/.config/qtile/config.py
cp sway.conf ~/.config/sway/config
cp waybar.conf ~/.config/waybar/config
cp waybar.css ~/.config/waybar/style.css
#qt/gtk styles
cp qt5ct.conf ~/.config/qt5ct/qt5ct.conf
cp qt5ct_spinboxes.qss ~/.config/qt5ct/qss/spinboxes.qss
cp kvantum.kvconfig ~/.config/Kvantum/kvantum.kvconfig
cp ArcDark.kvconfig ~/.config/Kvantum/ArcDark#/ArcDark#.kvconfig
cp .gtkrc-2.0 ~/.gtkrc-2.0
cp gtk2-filechooser.ini ~/.config/gtk-2.0/gtkfilechooser.ini
cp gtk3.ini ~/.config/gtk-3.0/settings.ini
gnome_schema="org.gnome.desktop.interface"
gsettings set "$gnome_schema" gtk-theme "Arc-Dark"
gsettings set "$gnome_schema" icon-theme "Papirus-Dark"
gsettings set "$gnome_schema" cursor-theme "bloom"
gsettings set "$gnome_schema" font-name "Libertinus Sans 11"
#font configs
cp fonts.conf ~/.config/fontconfig/fonts.conf
#userspace configs
cp pcmanfm.conf ~/.config/pcmanfm/default/pcmanfm.conf
cp kitty.conf ~/.config/kitty/kitty.conf
cp flameshot.ini ~/.config/flameshot/flameshot.ini
#Music
mkdir ~/Music/RYTD -p
git clone https://github.com/RiedleroD/RYTD.git ~/Music/RYTD
cp playlist.rpl ~/Music/default.rpl
cp .rytdconf ~/Music/RYTD/.rytdconf
python3 /home/riedler/Music/RYTD/rytd.py 
#package compilation config
doas cp makepkg.conf /etc/makepkg.conf
#wallpapers
mkdir /home/riedler/Pictures -p
curl https://i.imgur.com/2kyvrtg.png > /home/riedler/Pictures/wallpaper.png
curl https://i.imgur.com/e2rqx1O.jpg > /home/riedler/Pictures/wallpaper.jpg

#notice :)
echo "Make sure you installed the dependencies!"
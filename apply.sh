#!/usr/bin/sh

#custom executables (mostly rerouting and fixed args)
cp .bin_replacements ~/ -r
chmod -w ~/.bin_replacements -R #for security
#making sure all the folders exist
mkdir ~/.config/kitty ~/.config/qtile ~/.config/sway ~/.config/waybar \
~/.config/qt5ct/qss ~/.config/Kvantum/ArcDark# ~/.config/gtk-2.0 \
~/.config/gtk-3.0 ~/.config/flameshot ~/.config/fontconfig \
~/.config/deadbeef/playlists -p
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
#deadbeef config + playlists + plugins
cp deadbeef.conf ~/.config/deadbeef/config
cp playlist0.dbpl ~/.config/deadbeef/playlists/0.dbpl
cp playlist1.dbpl ~/.config/deadbeef/playlists/1.dbpl
if [ ! -f ~/.local/lib/deadbeef/discord_presence.so ] then
	curl "https://deac-ams.dl.sourceforge.net/project/deadbeef/plugins/x86_64/ddb_discord_presence-1.8-linux-x86_64.zip" > /tmp/ddb_discord_presence.zip
	unzip /tmp/ddb_discord_presence.zip -d ~/.local/lib/deadbeef/
	mv ~/.local/lib/deadbeef/plugins/discord_presence.so ~/.local/lib/deadbeef/discord_presence.so
	rm ~/.local/lib/deadbeef/plugins/ -d
	rm /tmp/ddb_discord_presence.zip
fi
if [ ! -f ~/.local/lib/deadbeef/opus.so ] then
	mkdir /data/diyfs/ddb_opus_plugin -p
	git clone "https://bitbucket.org/Lithopsian/deadbeef-opus.git" /data/diyfs/ddb_opus_plugin
	cd /data/diyfs/ddb_opus_plugin
	make
	mv ./opus.so ~/.local/lib/deadbeef/
	cd ~/Scripts/dotfiles
fi
if [ ! -f ~/.local/lib/deadbeef/seekbar.so ] then
	mkdir /data/diyfs/ddb_waveform_seekbar -p
	git clone "https://github.com/cboxdoerfer/ddb_waveform_seekbar.git" /data/diyfs/ddb_waveform_seekbar
	cd /data/diyfs/ddb_waveform_seekbar
	make
	mv ./gtk2/ddb_misc_waveform_GTK2.so ~/.local/lib/deadbeef/ddb_misc_waveform_GTK2.so
	mv ./gtk3/ddb_misc_waveform_GTK3.so ~/.local/lib/deadbeef/ddb_misc_waveform_GTK3.so
	cd ~/Scripts/dotfiles
fi
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
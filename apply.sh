#!/usr/bin/sh

#deadbeef plugins
if [ ! -f ~/.local/lib/deadbeef/discord_presence.so ]; then
	curl "https://deac-ams.dl.sourceforge.net/project/deadbeef/plugins/x86_64/ddb_discord_presence-1.8-linux-x86_64.zip" > /tmp/ddb_discord_presence.zip
	unzip /tmp/ddb_discord_presence.zip -d ~/.local/lib/deadbeef/
	mv ~/.local/lib/deadbeef/plugins/discord_presence.so ~/.local/lib/deadbeef/discord_presence.so
	rm ~/.local/lib/deadbeef/plugins/ -d
	rm /tmp/ddb_discord_presence.zip
else
	echo "skipped deadbeef discord presence plugin"
fi
if [ ! -f ~/.local/lib/deadbeef/opus.so ]; then
	mkdir /data/diyfs/ddb_opus_plugin -p
	git clone "https://bitbucket.org/Lithopsian/deadbeef-opus.git" /data/diyfs/ddb_opus_plugin
	cd /data/diyfs/ddb_opus_plugin
	make
	mv ./opus.so ~/.local/lib/deadbeef/
	cd ~/Scripts/dotfiles
else
	echo "skipped deadbeef opus plugin"
fi
if [ ! -f ~/.local/lib/deadbeef/ddb_misc_waveform_GTK3.so ]; then
	mkdir /data/diyfs/ddb_waveform_seekbar -p
	git clone "https://github.com/cboxdoerfer/ddb_waveform_seekbar.git" /data/diyfs/ddb_waveform_seekbar
	cd /data/diyfs/ddb_waveform_seekbar
	make
	mv ./gtk2/ddb_misc_waveform_GTK2.so ~/.local/lib/deadbeef/ddb_misc_waveform_GTK2.so
	mv ./gtk3/ddb_misc_waveform_GTK3.so ~/.local/lib/deadbeef/ddb_misc_waveform_GTK3.so
	cd ~/Scripts/dotfiles
else
	echo "skipped deadbeef waveform seekbar plugin"
fi
#LMMS devel compilation
if [ ! -d /data/diyfs/lmms ]; then
	git clone https://github.com/LMMS/lmms.git /data/diyfs/lmms --recurse-submodules -b master
	mkdir /data/diyfs/lmms/build
	cd /data/diyfs/lmms/build
	cmake .. -DCMAKE_INSTALL_PREFIX=../target/
	make -j4
	cd ~/Scripts/dotfiles
	cp ./.lmmsrc.xml /data/diyfs/lmms/build/.lmmsrc.xml
else
	echo "skipped lmms-git"
fi
#Music
if [ ! -d ~/Music/RYTD ]; then
	mkdir ~/Music/RYTD -p
	git clone https://github.com/RiedleroD/RYTD.git ~/Music/RYTD
	cp playlist.rpl ~/Music/default.rpl
	cp .rytdconf ~/Music/RYTD/.rytdconf
	python3 /home/riedler/Music/RYTD/rytd.py
else
	echo "skipped RYTD"
fi

#notice :)
echo "Make sure you installed the dependencies!"
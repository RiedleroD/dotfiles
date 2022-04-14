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

#notice :)
echo "Make sure you installed the dependencies!"
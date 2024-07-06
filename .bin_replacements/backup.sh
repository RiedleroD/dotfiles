#!/usr/bin/sh

# TODO: this needs some changes!!
exit 1

rm -drf .cache/paru/
rm -drf .cache/mozilla/firefox/

sudo rsync -r -P -a --delete -e ssh /home/riedler/ riedler@sakamoto:/home/riedler/powidl/home
sudo rsync -r -P -a --delete -e ssh /2fa.ini riedler@sakamoto:/home/riedler/powidl/2fa.ini
sudo rsync -r -P -a --delete -e ssh /data/diyfs/ riedler@sakamoto:/home/riedler/powidl/diyfs

pacman -Qqen > pkglist.txt
pacman -Qqem > aurlist.txt
rsync -r -P -a -e ssh pkglist.txt riedler@sakamoto:/home/riedler/powidl/pacman_pkgs.txt
rsync -r -P -a -e ssh aurlist.txt riedler@sakamoto:/home/riedler/powidl/aur_pkgs.txt
rm pkglist.txt
rm aurlist.txt

flatpak list --columns=application | tail -n +1 > flatpaklist.txt
rsync -r -P -a -e ssh flatpaklist.txt riedler@sakamoto:/home/riedler/powidl/flatpak_pkgs.txt
rm flatpaklist.txt

# note: python packages are not needed because global ones are managed by pacman, and local ones are in the home dir

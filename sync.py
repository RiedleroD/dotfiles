#!/usr/bin/env python3

import hashlib
from os.path import isfile, isdir, exists, expanduser, dirname, abspath, join as joinpath
from subprocess import run, PIPE, call
from os import listdir, makedirs
from sys import stdout
import shutil
from shlex import quote as shesc

#local file: destination file
FILES = {
	#shell configs
	".bash_profile": "~/.bash_profile",
	".bashrc": "~/.bashrc",
	".rev": "~/.rev",
	".rev_wayland": "~/.rev_wayland",
	#desktop environment configs
	"sway.conf": "~/.config/sway/config",#window manager for Wayland
	"i3.conf": "~/.config/i3/config",#window manager for X11,
	"waybar.conf": "~/.config/waybar/config",#taskbar for wayland
	"waybar.css": "~/.config/waybar/style.css",#-||-
	"polybar.conf": "~/.config/polybar/config.ini",#taskbar for X11
	"mako.conf": "~/.config/mako/config",#notification daemon for Wayland
	"dunst.conf": "~/.config/dunst/dunstrc",#notification daemon for X11
	#X11 Stuff
	".Xresources": "~/.Xresources",
	".xinitrc": "~/.xinitrc",
	"xsettingsd.conf": "~/.config/xsettingsd/xsettingsd.conf",
	#graphical toolkit configurations
	"qt5ct.conf": "~/.config/qt5ct/qt5ct.conf",#qt5ct redirects qt5 rendering to kvantum
	"qt5ct_spinboxes.qss": "~/.config/qt5ct/qss/spinboxes.qss",
	"kvantum.kvconfig": "~/.config/Kvantum/kvantum.kvconfig",#kvantum renders qt5 stuff better
	"ArcDark.kvconfig": "~/.config/Kvantum/ArcDark#/ArcDark#.kvconfig",
	"KvArcDark.kvconfig": "~/.config/Kvantum/KvArcDark#/KvArcDark#.kvconfig",
	".gtkrc-2.0": "~/.gtkrc-2.0",#gtk2 is old as shit but ppl still use it
	"gtk2-filechooser.ini": "~/.config/gtk-2.0/gtkfilechooser.ini",
	"gtk3.ini": "~/.config/gtk-3.0/settings.ini",#for gtk3 and gtk4
	#audio config
	"pipewire.conf":"~/.config/pipewire/pipewire.conf",
	#font configs
	"fonts.conf": "~/.config/fontconfig/fonts.conf",
	#userspace configs
	"pcmanfm.conf": "~/.config/pcmanfm/default/pcmanfm.conf",#file manager
	"kitty.conf": "~/.config/kitty/kitty.conf",#terminal
	"flameshot.ini": "~/.config/flameshot/flameshot.ini",#screenshotter
	"./.lmmsrc.xml": "~/.lmmsrc.xml",#LMMS - my DAW
	"htoprc": "~/.config/htop/htoprc",
	#stuff from kate - text editor & half an IDE
	"kate/": "~/.config/kate/",
	"kate.kmessagebox": "~/.config/kate.kmessagebox",
	"kate-externaltoolspluginrc": "~/.config/kate-externaltoolspluginrc",
	"katerc": "~/.config/katerc",
	"katesession":"~/.local/share/kate/anonymous.katesession",
	#Template files
	"./templates/": "~/Templates/",
	#deadbeef config + playlists
	"deadbeef.conf": "~/.config/deadbeef/config",
	"playlist0.dbpl": "~/.config/deadbeef/playlists/0.dbpl",
	"playlist1.dbpl": "~/.config/deadbeef/playlists/1.dbpl",
	#RYTD is my music synchronization script
	"playlist.rpl": "~/Music/default.rpl",
	".rytdconf": "~/Music/RYTD/.rytdconf",
	#package compilation config
	"makepkg.conf": "/etc/makepkg.conf",
	#package manager config
	"pacman.conf": "/etc/pacman.conf",
	#custom executables (mostly rerouting and fixed args)
	".bin_replacements/":"~/.bin_replacements/"
}

FMODS = {
	"~/.bin_replacements/":("755","root"),
	"/etc/makepkg.conf":("644","root"),
	"/etc/pacman.conf":("644","root")
}

GSETT = {
	#bluetooth eats a lot of power, so I disabled auto-startup
	"org.blueman.plugins.powermanager": {
		"auto-power-on": False,
	},
	#gtk stuff
	"org.gnome.desktop.interface": {
		"gtk-theme": "Arc-Dark",
		"icon-theme": "Papirus-Dark",
		"cursor-theme": "bloom",
		"font-name": "Libertinus Sans 11",
	},
}

#see further down, I don't feel like documenting this.
URLS = {
	"DeaDBeeF discord presence plugin":{
		"type"		:"git",
		"url"		:"https://github.com/kuba160/ddb_discord_presence.git",
		"dl_path"	:"/data/diyfs/ddb_discord_presence_plugin",
		"tag"		:"1.8",
		"build"		:"make",
		"src"		:"discord_presence.so",
		"dst"		:"~/.local/lib/deadbeef/discord_presence.so",
		"deps"		:("deadbeef-git","discord_arch_electron","wget"),
	},
	"DeaDBeeF opus plugin":{
		"type"		:"git",
		"url"		:"https://bitbucket.org/Lithopsian/deadbeef-opus.git",
		"dl_path"	:"/data/diyfs/ddb_opus_plugin",
		"build"		:"make",
		"src"		:"opus.so",
		"dst"		:"~/.local/lib/deadbeef/opus.so",
		"clean"		:"make clean",
		"deps"		:("deadbeef-git",),
	},
	"DeaDBeeF waveform seekbar plugin":{
		"type"		:"git",
		"url"		:"https://github.com/cboxdoerfer/ddb_waveform_seekbar.git",
		"dl_path"	:"/data/diyfs/ddb_waveform_seekbar",
		"build"		:"make",
		"src"		:("./gtk3/ddb_misc_waveform_GTK3.so","./gtk2/ddb_misc_waveform_GTK2.so"),
		"dst"		:("~/.local/lib/deadbeef/ddb_misc_waveform_GTK3.so","~/.local/lib/deadbeef/ddb_misc_waveform_GTK2.so"),
		"clean"		:"make clean",
		"deps"		:("deadbeef-git",),
	},
	"LMMS-git":{
		"type"		:"git",
		"url"		:"https://github.com/LMMS/lmms.git",
		"clone_args"	:("--recurse-submodules","-b","master","--depth=1"),
		"dl_path"	:"/data/diyfs/lmms",
		"build"		:"mkdir build -p && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=../target/ && make",
		"dst"		:"/data/diyfs/lmms/build/lmms",
		"deps"		:('libogg','libsndfile','libvorbis','lame','libsamplerate',
					  'fftw','wine','lilv','fluidsynth','alsa-lib','qt5-base',
					  'qt5-tools','qt5-x11extras','sdl2','libgig','lv2','stk',
					  'fltk','perl-list-moreutils','perl-exporter-tiny',
					  'perl-xml-parser','sdl12-compat','suil'),
	},
	"wakatime plugin for kate":{
		"type"		:"git",
		"url"		:"https://github.com/Tatsh/kate-wakatime.git",
		"dl_path"	:"/data/diyfs/wakatime_kate",
		"build"		:"mkdir build -p && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=/usr && make && sudo make install",
		"dst"		:"/usr/lib/qt/plugins/ktexteditor/ktexteditor_wakatime.so"
	},
	"vspcplay":{
		"type"		:"git",
		"url"		:"https://github.com/raphnet/vspcplay.git",
		"dl_path"	:"/data/diyfs/vspcplay",
		"build"		:"make",
		"dst"		:"/data/diyfs/vspcplay/vspcplay",
	},
	#from https://musescore.com/groups/young-composers-group/discuss/172224
	"Default Soundfont":{
		"type"		:"sh",
		"url"		:"https://download906.mediafire.com/899n5u59jpjg/maz5z394oog5xlm/HQ+Orchestral+Soundfont+Collection+v3.0.sfArk",
		"dl_path"	:"~/lmms/samples/soundfonts/HQ Orchestral Soundfont Collection v3.0.sfArk",
		"cmd"		:"sfarkxtc \"$RS_DL_PATH\" \"$RS_DST\"",
		"dst"		:"~/lmms/samples/soundfonts/HQ Orchestral Soundfont Collection v3.0.sf2",
		"deps"		:('sfarkxtc',),
	},
	"RYTD":{
		"type"		:"git",
		"url"		:"https://github.com/RiedleroD/RYTD.git",
		"dl_path"	:"~/Music/RYTD",
		"build"		:"sleep 0",
		"dst"		:"~/Music/RYTD/rytd.py"
	},
	"Wallpaper 1":{
		"type"	:"direct",
		"url"	:"https://i.imgur.com/2kyvrtg.png",
		"dst"	:"~/Pictures/wallpaper.png",
	},
	"Wallpaper 2":{
		"type"	:"direct",
		"url"	:"https://i.imgur.com/e2rqx1O.jpg",
		"dst"	:"~/Pictures/wallpaper.jpg",
	},
}

PKGS = {
	"base":[
		'xdg-user-dirs','kitty','libertinus-font','ttf-joypixels','libcanberra',
		'otf-font-awesome','brightnessctl','nwg-menu','lxappearance','kvantum',
		'qt5ct','kvantum-theme-arc','arc-gtk-theme','papirus-icon-theme','exa',
		'deepin-icon-theme','pipewire','pipewire-pulse','pipewire-jack','dex',
		'pipewire-alsa','pipewire-v4l2','gzip','libtool','gst-plugin-pipewire',
		'youtube-dl-git','opusfile','p7zip','unrar','sdl2','archlinux-keyring',
		'bison','fakeroot','gnome-themes-extra','gtk-engine-murrine','gvfs-nfs',
		'gvfs-smb','gvfs-mtp','wireplumber','bemenu','vulkan-validation-layers',
		'network-manager-applet','htop','autoconf','automake','binutils','grep',
		'wine','cmake','file','findutils','flex','gawk','gcc','gettext','groff',
		'blueman','m4','make','patch','pkgconf','sed','sudo','texinfo','which',
		'git','python-pip'],
	"wayland":['sway','waybar','waylock','xorg-xwayland','bemenu-wayland','mako'],
	"xorg":['i3-wm','polybar','i3lock','bemenu-x11','dunst'],
	"userspace":[
		'pcmanfm-gtk3','deadbeef-git','deadbeef-pipewire-plugin-git','helvum',
		'flameshot','engrampa','discord_arch_electron','teams-for-linux','gimp',
		'steam-native-runtime','inkscape','libreoffice-fresh','typora-free',
		'gummi','google-chrome','chromium','firefox','carla','obs-studio','imv',
		'pavucontrol','lmms','vlc','timidity++'],
}

def lclean():
	stdout.write("\r\033[2K")
def lprint(*args,**kwargs):
	lclean()
	print(*args,flush=True,**kwargs)
def lwrite(*args,**kwargs):
	lprint(*args,end="",**kwargs)
def linput(*args):
	lclean()
	return input(*args)

#Popen command and return stdout
pget = lambda *args,**kwargs: run([*args],capture_output=True,**kwargs).stdout.strip().decode('utf-8')
#Popen command and return exit code
prun = lambda *args,**kwargs: run([*args],check=True,**kwargs).returncode
#Popen command with sudo and return exit code
s_prun = lambda *args,**kwargs: prun("sudo",*args,**kwargs)
#shell command and return stdout
shget= lambda cmd,**kwargs: run(cmd,check=True,shell=True,capture_output=True,**kwargs).stdout.strip().decode('utf-8')
#shell command and return exit code
shrun= lambda cmd,**kwargs: run(cmd,check=True,shell=True,capture_output=False,**kwargs).returncode

#copies a file securely and forcibly
def filecopy(src,dst,dstmode="644"):
	if isdir(src):
		makedirs(dst)
		for fn in listdir(src):
			filecopy(joinpath(src,fn))
	else:
		try:
			shutil.copy(src,dst)
		except PermissionError:
			s_prun("cp",src,dst)
	if dstmode!=None:
		s_prun("chmod",dstmode,dst)

#asks the user yes/no and returns bool
ask_yn = lambda prompt: linput(f"{prompt} [y/n]: ").strip().lower() == 'y'
#asks the user sync/update/diff/omit and returns answer
ask_sudo = lambda prompt: linput(f"{prompt} [s/u/d/o]: ").strip().lower()
print("[s/u/d/o] prompts ask if you want to (s)ync to the repo, (u)pdate the repo, display the (d)iff or (o)mit action\n")
#TODO: parameter to skip all questions and assume yes and sync everywhere

def ensure_parent(fp):
	#NOTE: if fp is a relative path with no directories 
	# (e.g. ./file.txt, but without the dot), this could result in dirname()
	# returning an empty string, which mkdir() wouldn't be able to recognize as
	# a relative path to the current dir, raising a FileNotFoundError
	parent = dirname(fp)
	if not isdir(parent):
		makedirs(parent)

""" --- FILES --- """

def check_files():
	for src, dst in FILES.items():
		check_file(src,dst)
	lwrite()

def check_file(src,dst):
	dst_proper = expanduser(dst)
	if isdir(src):
		if isdir(dst_proper):
			#collecting all filenames from both directories
			filenames = listdir(src)
			for fn in listdir(dst_proper):
				if fn not in filenames:
					filenames.append(fn)
			
			for fn in filenames:
				check_file(joinpath(src,fn),joinpath(dst,fn))
			return
		elif not exists(dst_proper):
			if ask_yn(f"Folder not present. copy {src} to {dst}?"):
				filecopy(src,dst_proper)
			return
		else:
			raise Exception("Source and Destination have to be the same type: either file or folder!")
	elif not exists(src):
		if ask_yn(f"File not present. copy {dst} to {src}?"):
			#SEE: ensure_parent() for why abspath() is needed here
			ensure_parent(abspath(src))
			filecopy(dst_proper,src)
		return
	elif not exists(dst_proper):
		if ask_yn(f"File not present. copy {src} to {dst}?"):
			ensure_parent(dst_proper)
			filecopy(src,dst_proper)
		return
	
	lwrite(f"checking file {src}")
	if not are_files_equal(src,dst_proper):
		while True:
			s_u_d_o = ask_sudo(f"{dst} differs from {src}.")
			if s_u_d_o == 's':
				filecopy(src,dst_proper)
				break
			elif s_u_d_o == 'u':
				filecopy(dst_proper,src,"666")
				break
			elif s_u_d_o == 'd':
				shrun(f"kitty +kitten diff {shesc(src)} {shesc(expanduser(dst))}")
				continue
			else:
				break

#checks if files are equal (returns None if second file doesn't exist)
def are_files_equal(fn1, fp2) -> bool:
	if isfile(fp2):
		with open(fn1,'rb') as f:
			hash1 = hashlib.md5(f.read()).digest()
		with open(fp2,'rb') as f:
			hash2 = hashlib.md5(f.read()).digest()
		return hash1 == hash2
	else:
		return None

#sets proper chmod for files
def chmod_files():
	for fp, mod in FMODS.items():
		chmod_file(fp,*mod)
def chmod_file(fp,mod,owner):
	fp = expanduser(fp)
	if exists(fp):
		s_prun("chmod",mod,fp)
		s_prun("chown",owner,fp)
	if isdir(fp):
		s_prun("chmod","+x",fp)
		for fn in listdir(fp):
			chmod_file(joinpath(fp,fn),mod,owner)

""" --- GSETTINGS --- """

def check_gsettings():
	for group, mappings in GSETT.items():
		for key, value in mappings.items():
			lwrite(f"checking gsettings {group}: {key}")
			if curval:=are_gsett_nequal(group,key,value):
				if ask_yn(f"gsetting {group} {key} is not {value}, but {curval}. Replace?"):
					prun("gsettings","set",group,key,value)
	lwrite()

#checks if gsetting is not a certain value (ignores @-prefixed type annotations)
def are_gsett_nequal(group,key,value):
	curval=pget("gsettings","get",group,key)
	if curval.startswith('@'):
		curval=curval[curval.index(' ')+1:]
	typ=type(value)
	if typ==bool:
		value=str(value).lower()
	elif typ==int:
		curval=int(curval)
	elif typ==str:
		curval=curval[1:-1]
	else:
		raise Exception(f"Unhandled type: {typ}")
	
	return None if curval==value else curval

""" --- DOWNLOADS --- """

def check_downloadables():
	for name,data in URLS.items():
		dst = data["dst"]
		lwrite(f"checking {dst}")
		if type(dst)==str:
			dst = expanduser(dst)
			if not exists(dst):
				select_downloadable_action(name,data,dst)
		elif type(dst) in (tuple,list):
			dst = [expanduser(_dst) for _dst in dst]
			if not all(exists(_dst) for _dst in dst):
				select_downloadable_action(name,data,dst)
		else:
			raise Exception("Destination(s) can't be other than string or collection")
	lwrite()

def select_downloadable_action(name,data,dst):
	if not ask_yn(f"Download {name}?"):
		return
	if "deps" in data.keys():
		prun("paru","-S",*data["deps"],"--needed")
	typ = data["type"]
	if typ=="direct":
		download_direct(data["url"],dst)
	elif typ=="sh":
		download_sh(name,data["url"],dst,data["cmd"],expanduser(data["dl_path"]))
	elif typ=="git":
		download_git(name,**data)
	else:
		lprint(f"{name}: downloadable type '{typ}' not supported")

def download_direct(url,dst):
	ensure_parent(dst)
	shrun(f"curl {shesc(url)} -o {shesc(expanduser(dst))} --progress-bar")
	stdout.write("\r\033[1A\033[2K")#deleting progress bar

def download_sh(name,url,dst,cmd,dl_path):
	if not isfile(dl_path):
		download_direct(url,dl_path)
	ensure_parent(dst)
	lwrite(f"running command for {name}")
	shget(cmd,cwd=dirname(dst),env={"RS_DST":dst,"RS_DL_PATH":dl_path,"RS_URL":url})

def download_git(name,url,dl_path,build,dst,src=None,tag=None,clone_args=("--depth=1",),clean="",**kwargs):
	dl_path = expanduser(dl_path)
	if src:
		if type(src)==str:
			src=(src,)
		if type(dst)==str:
			dst=(dst,)
		assert len(src)==len(dst), "differing amounts of sources and destinations"
	if not exists(joinpath(dl_path,".git")):
		ensure_parent(dl_path)
		lwrite(f"{name}: cloning repo")
		pget("git","clone",url,dl_path,*clone_args)
	else:
		lwrite(f"{name}: pulling updates")
		pget("git","pull",cwd=dl_path)
	if tag:
		pget("git","checkout",tag,cwd=dl_path)
	lwrite(f"{name}: running build")
	shget(build,cwd=dl_path)
	if src:
		lwrite(f"{name}: copying files")
		for srcfn,dstfp in zip(src,dst):
			_dstfp = expanduser(dstfp)
			ensure_parent(_dstfp)
			filecopy(joinpath(dl_path,srcfn),_dstfp,dstmode=None)
	if clean:
		lwrite(f"{name}: cleaning up")
		shget(clean,cwd=dl_path)

""" --- PACKAGES --- """

def check_packages():
	installed_pkgs = [line.split(' ')[0] for line in pget("pacman","-Q").split("\n")]
	missing_pkgs = {}
	toinstall = []
	for group,pkgs in PKGS.items():
		lwrite(f"checking {group} for packages")
		for pkg in pkgs:
			if pkg not in installed_pkgs:
				if group in missing_pkgs.keys():
					missing_pkgs[group].append(pkg)
				else:
					missing_pkgs[group]=[pkg]
					
	for group,pkgs in missing_pkgs.items():
		lwrite(f"{len(pkgs)} packages from group '{group}' are missing.\n")
		if ask_yn("ignore?"):
			continue
		for pkg in pkgs:
			if ask_yn(f"install {pkg}?"):
				toinstall.append(pkg)
	if len(toinstall)>0:
		prun("paru","-S",*toinstall,"--needed")
	

if __name__=="__main__":
	check_files()
	chmod_files()
	check_gsettings()
	check_downloadables()
	check_packages()
	if ask_yn("first setup?"):
		prun("systemctl","--user","enable","wireplumber")
		s_prun("systemctl","enable","--now","bluetooth")
		prun("pip3","install","mutagen")#for corr
		print("reboot now")
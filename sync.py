#!/usr/bin/env python3

import hashlib
from os.path import isfile, isdir, exists, expanduser, dirname, join as joinpath
from subprocess import run, PIPE, call
from os import listdir, makedirs, system as shrun
from sys import stdout
import shutil

#local file: destination file
FILES = {
	#shell configs
	".bash_profile": "~/.bash_profile",
	".bashrc": "~/.bashrc",
	".rev": "~/.rev",
	".rev_wayland": "~/.rev_wayland",
	#desktop environment configs
	"sway.conf": "~/.config/sway/config",#window manager
	"waybar.conf": "~/.config/waybar/config",#taskbar
	"waybar.css": "~/.config/waybar/style.css",#-||-
	"xsettingsd.conf": "~/.config/xsettingsd/xsettingsd.conf",#XWayland stuff
	"mako.conf": "~/.config/mako/config",#notification demon
	#graphical toolkit configurations
	"qt5ct.conf": "~/.config/qt5ct/qt5ct.conf",#qt5ct redirects qt5 rendering to kvantum
	"qt5ct_spinboxes.qss": "~/.config/qt5ct/qss/spinboxes.qss",
	"kvantum.kvconfig": "~/.config/Kvantum/kvantum.kvconfig",#kvantum renders qt5 stuff better
	"ArcDark.kvconfig": "~/.config/Kvantum/ArcDark#/ArcDark#.kvconfig",
	"KvArcDark.kvconfig": "~/.config/Kvantum/KvArcDark#/KvArcDark#.kvconfig",
	".gtkrc-2.0": "~/.gtkrc-2.0",#gtk2 is old as shit but ppl still use it
	"gtk2-filechooser.ini": "~/.config/gtk-2.0/gtkfilechooser.ini",
	"gtk3.ini": "~/.config/gtk-3.0/settings.ini",#for gtk3 and gtk4
	#font configs
	"fonts.conf": "~/.config/fontconfig/fonts.conf",
	#userspace configs
	"pcmanfm.conf": "~/.config/pcmanfm/default/pcmanfm.conf",#file manager
	"kitty.conf": "~/.config/kitty/kitty.conf",#terminal
	"flameshot.ini": "~/.config/flameshot/flameshot.ini",#screenshotter
	"./.lmmsrc.xml": "~/.lmmsrc.xml",#LMMS - my DAW
	#stuff from kate - text editor & half an IDE
	"kate/": "~/.config/kate/",
	"kate.kmessagebox": "~/.config/kate.kmessagebox",
	"kate-externaltoolspluginrc": "~/.config/kate-externaltoolspluginrc",
	"katerc": "~/.config/katerc",
	#Template files
	"./templates/": "~/Templates/",
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
}

#TODO: add safe support for .bin_replacements

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
		"type"	:"zip",
		"url"	:"https://deac-ams.dl.sourceforge.net/project/deadbeef/plugins/x86_64/ddb_discord_presence-1.8-linux-x86_64.zip",
		"src"	:"plugins/discord_presence.so",
		"dst"	:"~/.local/lib/deadbeef/discord_presence.so",
	},
	"DeaDBeeF opus plugin":{
		"type"		:"git",
		"url"		:"https://bitbucket.org/Lithopsian/deadbeef-opus.git",
		"dl_path"	:"/data/diyfs/ddb_opus_plugin",
		"build"		:"make",
		"src"		:"opus.so",
		"dst"		:"~/.local/lib/deadbeef/opus.so",
		"clean"		:"make clean",
	},
	"DeaDBeeF waveform seekbar plugin":{
		"type"		:"git",
		"url"		:"https://github.com/cboxdoerfer/ddb_waveform_seekbar.git",
		"dl_path"	:"/data/diyfs/ddb_waveform_seekbar",
		"build"		:"make",
		"src"		:("./gtk3/ddb_misc_waveform_GTK3.so","./gtk2/ddb_misc_waveform_GTK2.so"),
		"dst"		:("~/.local/lib/deadbeef/ddb_misc_waveform_GTK3.so","~/.local/lib/deadbeef/ddb_misc_waveform_GTK2.so"),
		"clean"		:"make clean",
	},
	"LMMS-git":{
		"type"		:"git",
		"url"		:"https://github.com/LMMS/lmms.git",
		"clone_args"	:("--recurse-submodules","-b","master"),
		"dl_path"	:"/data/diyfs/lmms",
		"build"		:"mkdir build && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=../target/ && make -j0",
		"dst"		:"/data/diyfs/lmms/build/lmms",
	},
	"Default Soundfont":{
		"type"		:"sh",
		"url"		:"https://download1761.mediafire.com/v9gy038xcz4g/maz5z394oog5xlm/HQ+Orchestral+Soundfont+Collection+v3.0.sfArk",
		"dl_path"	:"~/lmms/samples/soundfonts/HQ Orchestral Soundfont Collection v3.0.sfArk",
		"cmd"		:"sfarkxtc \"$RS_DL_PATH\" \"$RS_DST\"",
		"dst"		:"~/lmms/samples/soundfonts/HQ Orchestral Soundfont Collection v3.0.sf2",
	},
	"RYTD":{
		"type"		:"git",
		"url"		:"https://github.com/RiedleroD/RYTD.git",
		"dl_path"	:"~/Music/RYTD",
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
#Popen command and return nothing
prun = lambda *args,**kwargs: run([*args],check=True,**kwargs)
#shell command and return stdout
shget= lambda cmd,**kwargs: run(cmd,check=True,shell=True,capture_output=True,**kwargs).stdout.strip().decode('utf-8')

#asks the user yes/no and returns bool
ask_yn = lambda prompt: linput(f"{prompt} [y/n]: ").strip().lower() == 'y'
#asks the user sync/update/diff/omit and returns answer
ask_sudo = lambda prompt: linput(f"{prompt} [s/u/d/o]: ").strip().lower()
print("[s/u/d/o] prompts ask if you want to (s)ync to the repo, (u)pdate the repo, display the (d)iff or (o)mit action\n")
#TODO: parameter to skip all questions and assume yes and sync everywhere

def ensure_parent(fp):
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
			for fn in listdir(src):
				check_file(joinpath(src,fn),joinpath(dst,fn))
			return
		elif not exists(dst_proper):
			if ask_yn(f"Folder not present. copy {src} to {dst}?"):
				shutil.copy(src,dst_proper)
			return
		else:
			raise Exception("Source and Destination have to be the same type: either file or folder!")
	
	lwrite(f"checking file {src}")
	feq = are_files_equal(src,dst_proper)
	if feq==None:
		if ask_yn(f"File not present. copy {src} to {dst}?"):
			ensure_parent(dst_proper)
			shutil.copy(src,dst_proper)
	elif not feq:
		while True:
			s_u_d_o = ask_sudo(f"{dst} differs from {src}.")
			if s_u_d_o == 's':
				shutil.copy(src,dst_proper)
				break
			elif s_u_d_o == 'u':
				shutil.copy(dst_proper,src)
				break
			elif s_u_d_o == 'd':
				shrun(f"kitty +kitten diff {src} {dst}")
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
	typ = data["type"]
	if typ=="direct":
		download_direct(data["url"],dst)
	elif typ=="sh":
		download_sh(name,data["url"],dst,data["cmd"],expanduser(data["dl_path"]))
	else:#TODO: implement the rest of the download types
		lprint(f"{name}: downloadable type '{typ}' not supported")

def download_direct(url,dst):
	ensure_parent(dst)
	shrun("curl",url,"-o",dst,"--progress-bar")
	write("\r\033[1A\033[2K")#deleting progress bar

def download_sh(name,url,dst,cmd,dl_path):
	if not isfile(dl_path):
		download_direct(url,dl_path)
	ensure_parent(dst)
	lwrite(f"running command for {name}")
	shget(cmd,cwd=dirname(dst),env={"RS_DST":dst,"RS_DL_PATH":dl_path,"RS_URL":url})

if __name__=="__main__":
	check_files()
	check_gsettings()
	check_downloadables()
	#notice :)
	print("Make sure you installed the dependencies!")
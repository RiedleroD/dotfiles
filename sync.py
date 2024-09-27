#!/usr/bin/env python3
from confreader import Config
from helper import lwrite, linput, pget, prun, s_prun, shget, shrun

import hashlib
from os.path import isfile, isdir, exists, expanduser, dirname, abspath, relpath, join as joinpath
from os import listdir, makedirs
from sys import stdout
import shutil
from shlex import quote as shesc

from typing import Type

# TODO: better interface with Config class
FILES = Config.get_files()
FMODS = Config.get_fmods()

GSETT: dict[str, dict[str, bool | int | str]] = {
	# bluetooth eats a lot of power, so I disabled auto-startup
	"org.blueman.plugins.powermanager": {
		"auto-power-on": False,
	},
	# gtk stuff
	"org.gnome.desktop.interface": {
		"color-scheme": "prefer-dark",
		"gtk-theme": "Arc-Dark",
		"icon-theme": "Papirus-Dark",
		"cursor-theme": "bloom",
		"font-name": "Libertinus Sans 11",
	},
	"org.gnome.desktop.wm.preferences": {
		"theme": "Arc-Dark",
	},
}

class Downloadable:
	name: str
	url: str
	dst: tuple[str, ...]
	deps: tuple[str, ...]
	
	def __init__(self, name: str, url: str, dst: str | tuple[str, ...], deps: tuple[str, ...] = tuple()):
		self.name = name
		self.url = url
		dst_: tuple[str, ...] = dst if isinstance(dst, tuple) else (dst,)
		self.dst = tuple(expanduser(fp) for fp in dst_)
		self.deps = deps
	
	def download(self) -> None:
		raise NotImplementedError()

class DownloadableGit(Downloadable):
	clone_args: tuple[str, ...]
	dl_path: str
	tag: str | None
	build: str
	src: tuple[str, ...]
	clean: str
	
	def __init__(self,
			name: str,
			url: str,
			dl_path: str,
			build: str,
			dst: str | tuple[str, ...],
			src: str | tuple[str, ...] = tuple(),
			clean: str = "",
			clone_args: tuple[str, ...] = tuple(),
			deps: tuple[str, ...] = tuple(),
			tag: str | None = None):
		super().__init__(name, url, dst, deps)
		self.dl_path = expanduser(dl_path)
		self.tag = tag
		self.build = build
		src_ = src if isinstance(src, tuple) else (src,)
		self.src = tuple(expanduser(fp) for fp in src_)
		self.clone_args = clone_args
		self.clean = clean
	
	def download(self) -> None:
		assert len(self.src) == len(self.dst), \
			"differing amounts of sources and destinations"
		
		if not exists(joinpath(self.dl_path, ".git")):
			ensure_parent(self.dl_path)
			lwrite(f"{self.name}: cloning repo")
			pget("git", "clone", self.url, self.dl_path, *self.clone_args)
		else:
			lwrite(f"{self.name}: pulling updates")
			pget("git", "pull", cwd=self.dl_path)
		if self.tag is not None:
			pget("git", "checkout", self.tag, cwd=self.dl_path)
		lwrite(f"{self.name}: running build")
		shget(self.build, cwd=self.dl_path)
		if self.src:
			lwrite(f"{self.name}: copying files")
			for srcfn, dstfp in zip(self.src, self.dst):
				_dstfp: str = expanduser(dstfp)
				filecopy(joinpath(self.dl_path, srcfn), _dstfp, dstmode=None)
		if self.clean:
			lwrite(f"{self.name}: cleaning up")
			shget(self.clean, cwd=self.dl_path)

class DownloadableDirect(Downloadable):
	def download(self) -> None:
		assert len(self.dst) == 1
		dstfp: str = self.dst[0]
		ensure_parent(dstfp)
		shrun(f"curl {shesc(self.url)} -o {shesc(dstfp)} --progress-bar")
		stdout.write("\r\033[1A\033[2K") # deleting progress bar

class DownloadableSh(Downloadable):
	dl_path: str
	cmd: str
	
	def __init__(self,
		name: str,
		url: str,
		dst: str | tuple[str, ...],
		dl_path: str,
		cmd: str,
		deps: tuple[str, ...] = tuple()):
		super().__init__(name, url, dst, deps)
		self.dl_path = expanduser(dl_path)
		self.cmd = cmd
	
	def download(self) -> None:
		if not exists(self.dl_path):
			DownloadableDirect(self.name, self.url, self.dl_path).download()
		dstfp = self.dst[0]
		ensure_parent(dstfp)
		lwrite(f"running command for {self.name}")
		shget(self.cmd, cwd=dirname(dstfp), env={
			"RS_DST": dstfp,
			"RS_DL_PATH": self.dl_path,
			"RS_URL": self.url
		})


URLS: tuple[Downloadable, ...] = (
	DownloadableGit(
		name		="DeaDBeeF discord presence plugin",
		url			="https://github.com/kuba160/ddb_discord_presence.git",
		dl_path		="/data/diyfs/ddb_discord_presence_plugin",
		tag			="1.8",
		build		="make",
		src			="discord_presence.so",
		dst			="~/.local/lib/deadbeef/discord_presence.so",
		deps		=("deadbeef-git", "discord_arch_electron", "wget"),
	),
	DownloadableGit(
		name		="DeaDBeeF opus plugin",
		url			="https://bitbucket.org/Lithopsian/deadbeef-opus.git",
		dl_path		="/data/diyfs/ddb_opus_plugin",
		build		="make",
		src			="opus.so",
		dst			="~/.local/lib/deadbeef/opus.so",
		clean		="make clean",
		deps		=("deadbeef-git",),
	),
	DownloadableGit(
		name		="DeaDBeeF waveform seekbar plugin",
		url			="https://github.com/cboxdoerfer/ddb_waveform_seekbar.git",
		dl_path		="/data/diyfs/ddb_waveform_seekbar",
		build		="make",
		src			=("./gtk3/ddb_misc_waveform_GTK3.so", "./gtk2/ddb_misc_waveform_GTK2.so"),
		dst			=("~/.local/lib/deadbeef/ddb_misc_waveform_GTK3.so",
					  "~/.local/lib/deadbeef/ddb_misc_waveform_GTK2.so"),
		clean		="make clean",
		deps		=("deadbeef-git",),
	),
	DownloadableGit(
		name		="LMMS-git",
		url			="https://github.com/LMMS/lmms.git",
		clone_args	=("--recurse-submodules", "-b", "master", "--depth=1"),
		dl_path		="/data/diyfs/lmms",
		build		="mkdir build -p && cd build && cmake .. -DCMAKE_INSTALL_PREFIX=../target/ && make",
		dst			="/data/diyfs/lmms/build/lmms",
		deps		=('libogg', 'libsndfile', 'libvorbis', 'lame', 'alsa-lib',
					  'libsamplerate', 'fftw', 'wine', 'lilv', 'fluidsynth',
					  'qt5-base', 'qt5-tools', 'qt5-x11extras', 'sdl2', 'lv2',
					  'libgig', 'stk', 'fltk', 'perl-list-moreutils', 'suil',
					  'perl-exporter-tiny', 'perl-xml-parser', 'sdl12-compat'),
	),
	# from https://musescore.com/groups/young-composers-group/discuss/172224
	DownloadableSh(
		name		="Default Soundfont",
		url			="https://download906.mediafire.com/899n5u59jpjg/maz5z394oog5xlm/HQ+Orchestral+Soundfont+Collection+v3.0.sfArk",
		dl_path		="~/lmms/samples/soundfonts/HQ Orchestral Soundfont Collection v3.0.sfArk",
		cmd			="sfarkxtc \"$RS_DL_PATH\" \"$RS_DST\"",
		dst			="~/lmms/samples/soundfonts/HQ Orchestral Soundfont Collection v3.0.sf2",
		deps		=('sfarkxtc',),
	),
	DownloadableGit(
		name		="RYTD",
		url			="https://github.com/RiedleroD/RYTD.git",
		dl_path		="~/Music/RYTD",
		build		="sleep 0",
		dst			="~/Music/RYTD/rytd.py"
	),
	DownloadableDirect(
		name		="Wallpaper (Arch)",
		url			="https://i.imgur.com/2kyvrtg.png",
		dst			="~/Pictures/wallpaper_arch.png",
	),
	DownloadableDirect(
		name		="Wallpaper (Links)",
		url			="https://i.imgur.com/F9322ei.jpeg",
		dst			="~/Pictures/wallpaper_links.jpg",
	),
	DownloadableDirect(
		name		="Wallpaper (Avatar137)",
		url			="https://i.imgur.com/eU9G6Ax.jpg",
		dst			="~/Pictures/wallpaper_avatar137.jpg",
	),
)

PKGS: dict[str, list[str]] = {
	"base":[
		'xdg-user-dirs','kitty','libertinus-font','ttf-joypixels','libcanberra',
		'otf-font-awesome','nwg-menu','lxappearance','kvantum','kvantum-qt5',
		'qt5ct','qt6ct','kvantum-theme-arc','arc-gtk-theme','papirus-icon-theme',
		'deepin-icon-theme','pipewire','pipewire-pulse','pipewire-jack','dex',
		'pipewire-alsa','pipewire-v4l2','gzip','libtool','gst-plugin-pipewire',
		'yt-dlp','opusfile','p7zip','unrar','sdl2','archlinux-keyring',
		'bison','fakeroot','gnome-themes-extra','gtk-engine-murrine','gvfs-nfs',
		'gvfs-smb','wireplumber','bemenu','kwallet','kwalletmanager','kwallet-pam',
		'network-manager-applet','htop','autoconf','automake','binutils','grep',
		'wine','cmake','file','findutils','flex','gawk','gcc','gettext','groff',
		'blueman','m4','make','patch','pkgconf','sed','sudo','texinfo','which',
		'git','python-pip','python-mutagen','dhcpcd','flatpak','com.github.tchx84.Flatseal',
		'zsh','bash'],
	"wayland":['sway','waybar','xorg-xwayland','bemenu-wayland','mako','swayidle',
		'xdg-desktop-portal-wlr','xdg-desktop-portal-gtk','swaylock-effects',
		'slurp','grim','wl-clipboard','swww','wofi'],
	"xorg":['i3-wm','polybar','i3lock','bemenu-x11','dunst'],
	"userspace":[
		'pcmanfm-gtk3','deadbeef-git','helvum',
		'engrampa','discord_arch_electron','gimp',
		'steam-native-runtime','libreoffice-fresh','inkscape',
		'kile','org.chromium.Chromium','firefox','carla','obs-studio','imv',
		'pavucontrol','lmms','vspcplay','kate'],
	"laptop":['tlp','ethtool','smartmontools','slimbookbattery','brightnessctl'],
}

# copies a file securely and forcibly
def filecopy(src: str, dst: str, dstmode: str | None = "644") -> None:
	if isdir(src):
		makedirs(dst)
		for fn in listdir(src):
			filecopy(joinpath(src, fn), joinpath(dst, fn), dstmode)
	else:
		ensure_parent(dst)
		try:
			shutil.copy(src, dst)
		except PermissionError:
			s_prun("cp", src, dst)
	if dstmode is not None:
		s_prun("chmod", dstmode, dst)
		if isdir(dst): # dirs should always be listable
			s_prun("chmod", "+x", dst)

def ask_yn(prompt: str) -> bool:
	"""asks the user yes/no and returns bool"""
	return linput(f"{prompt} [y/n]: ").strip().lower() == 'y'
def ask_sudo(prompt: str) -> str:
	"""asks the user sync/update/diff/omit and returns answer"""
	return linput(f"{prompt} [s/u/d/o]: ").strip().lower()


print("[s/u/d/o] prompts ask if you want to (s)ync to the repo, (u)pdate the repo, display the (d)iff or (o)mit action\n")
# TODO: parameter to skip all questions and assume yes and sync everywhere

def ensure_parent(fp: str) -> None:
	parent: str = dirname(abspath(fp))
	if not isdir(parent):
		makedirs(parent)


""" --- FILES --- """

def check_files() -> None:
	for src, dst in FILES.items():
		check_file(src, dst)
	lwrite()

def check_file(src: str, dst: str) -> None:
	if isdir(src):
		if isdir(dst):
			# collecting all filenames from both directories
			filenames = listdir(src)
			for fn in listdir(dst):
				if fn not in filenames:
					filenames.append(fn)
			
			for fn in filenames:
				check_file(joinpath(src, fn), joinpath(dst, fn))
			return
		elif not exists(dst):
			if ask_yn(f"Folder not present. copy {relpath(src)} to {dst}?"):
				filecopy(src, dst)
			return
		else:
			raise Exception("Source and Destination have to be the same type: either file or folder!")
	elif not exists(src):
		if ask_yn(f"File not present. copy {dst} to {relpath(src)}?"):
			filecopy(dst, src)
		return
	elif not exists(dst):
		if ask_yn(f"File not present. copy {relpath(src)} to {dst}?"):
			filecopy(src, dst)
		return
	
	lwrite(f"checking file {src}")
	if not are_files_equal(src, dst):
		while True:
			s_u_d_o = ask_sudo(f"{dst} differs from {relpath(src)}.")
			if s_u_d_o == 's':
				filecopy(src, dst)
				break
			elif s_u_d_o == 'u':
				filecopy(dst, src, "666")
				break
			elif s_u_d_o == 'd':
				shrun(f"kitty +kitten diff {shesc(src)} {shesc(dst)}")
				continue
			else:
				break

def are_files_equal(fn1: str, fp2: str) -> bool | None:
	"""checks if files are equal (returns None if second file doesn't exist)"""
	if isfile(fp2):
		with open(fn1, 'rb') as f:
			hash1 = hashlib.md5(f.read()).digest()
		with open(fp2, 'rb') as f:
			hash2 = hashlib.md5(f.read()).digest()
		return hash1 == hash2
	else:
		return None

def chmod_files() -> None:
	"""sets proper chmod for files"""
	for fp, mod in FMODS.items():
		chmod_file(fp, *mod)
def chmod_file(fp: str, mod: str, owner: str) -> None:
	if exists(fp):
		s_prun("chmod", mod, fp)
		s_prun("chown", owner, fp)
	if isdir(fp):
		s_prun("chmod", "+x", fp)
		for fn in listdir(fp):
			chmod_file(joinpath(fp, fn), mod, owner)


""" --- GSETTINGS --- """

def check_gsettings() -> None:
	for group, mappings in GSETT.items():
		for key, value in mappings.items():
			lwrite(f"checking gsettings {group}: {key}")
			if curval := are_gsett_nequal(group, key, value):
				if ask_yn(f"gsetting {group} {key} is not {value}, but {curval}. Replace?"):
					prun("gsettings", "set", group, key, value)
	lwrite()

def are_gsett_nequal(group: str, key: str, value: bool | int | str) -> None | str | int:
	"""checks if gsetting is not a certain value (ignores @-prefixed type annotations)"""
	strval: str = pget("gsettings", "get", group, key)
	curval: str | int
	if strval.startswith('@'):
		curval = strval[strval.index(' ') + 1:]
	else:
		curval = strval
	typ: Type[bool | int | str] = type(value)
	if typ is bool:
		value = str(value).lower()
	elif typ is int:
		curval = int(curval)
	elif typ is str:
		assert isinstance(curval, str) # make mypy shut up
		curval = curval[1:-1]
	else:
		raise Exception(f"Unhandled type: {typ}")
	
	return None if curval == value else curval


""" --- DOWNLOADS --- """

def check_downloadables() -> None:
	for data in URLS:
		dst = data.dst
		lwrite(f"checking {dst}")
		if not all(exists(_dst) for _dst in dst):
			if not ask_yn(f"Download {data.name}?"):
				return
			if len(data.deps) > 0:
				prun("paru", "-S", *data.deps, "--needed")
			data.download()
	lwrite()


""" --- PACKAGES --- """

def check_packages() -> None:
	installed_pkgs: list[str] = \
		[line.split(' ')[0] for line in pget("pacman", "-Q").split("\n")]
	installed_pkgs += \
		[line for line in
			pget("flatpak", "list", "--columns=application")
			.split("\n")
		][1:]
	missing_pkgs: dict[str, list[str]] = {}
	toinstall_paru: list[str] = []
	toinstall_flatpak: list[str] = []
	for group, pkgs in PKGS.items():
		lwrite(f"checking {group} for packages")
		for pkg in pkgs:
			if pkg not in installed_pkgs:
				if group in missing_pkgs.keys():
					missing_pkgs[group].append(pkg)
				else:
					missing_pkgs[group] = [pkg]
					
	for group, pkgs in missing_pkgs.items():
		lwrite(f"{len(pkgs)} packages from group '{group}' are missing.\n")
		if not ask_yn("investigate?"):
			continue
		for pkg in pkgs:
			if ask_yn(f"install {pkg}?"):
				if '.' in pkg:
					toinstall_flatpak.append(pkg)
				else:
					toinstall_paru.append(pkg)
	if len(toinstall_paru) > 0:
		prun("paru", "-S", *toinstall_paru, "--needed")
	if len(toinstall_flatpak) > 0:
		prun("flatpak", "install", *toinstall_flatpak, "--needed")
	

if __name__ == "__main__":
	check_files()
	chmod_files()
	check_gsettings()
	check_downloadables()
	check_packages()
	if ask_yn("first setup?"):
		prun("systemctl", "--user", "enable", "wireplumber")
		s_prun("systemctl", "enable", "--now", "bluetooth")
		s_prun("systemctl", "enable", "--now", "dhcpcd")
		s_prun("systemctl", "mask", "systemd-rfkill.service", "systemd-rfkill.socket") # for tlp
		print("reboot now")

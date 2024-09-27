#!/usr/bin/env python3
from helper import shget

from os.path import basename, dirname, realpath, join as joinpath
from os import environ

from typing import ClassVar

CURDIR = realpath(dirname(__file__))

class Config:
	files_cache: ClassVar[tuple['SyncFile', ...] | None] = None
	
	@classmethod
	def get_files(cls) -> dict[str, str]:
		if cls.files_cache is None:
			cls.parse_fileconfig()
			assert cls.files_cache is not None
		
		return {sf.get_dstpath(): sf.get_fullpath() for sf in cls.files_cache}
	
	@classmethod
	def get_fmods(cls) -> dict[str, tuple[str, str]]:
		if cls.files_cache is None:
			cls.parse_fileconfig()
			assert cls.files_cache is not None
		
		return {sf.get_fullpath(): sf.get_perms() for sf in cls.files_cache if sf.has_perms()}
	
	@classmethod
	def parse_fileconfig(cls) -> None:
		syncfiles: list[SyncFile] = []
		
		conf = joinpath(CURDIR, 'files.cfg')
		helper = joinpath(CURDIR, 'helper.sh')
		
		with open(conf, 'r') as f:
			for i, line in enumerate(f.read().splitlines()):
				# TODO: this is awful. I NEED to parse this in a better way
				params = shget(f"{helper} {line}").split("\n")
				params = [param for param in params if len(param) > 0]
				
				match len(params):
					case 0:
						continue
					case 1:
						syncfiles.append(SyncFile(params[0]))
					case 2:
						syncfiles.append(SyncFile(params[0], params[1]))
					case 3:
						mode, owner = params[2].split(':')
						syncfiles.append(SyncFile(params[0], params[1], int(mode), owner))
					case _:
						raise SyntaxError(f"Couldn't parse line {i} in {conf}")
		
		cls.files_cache = tuple(syncfiles)

class SyncFile:
	__slots__ = ('fullpath', 'dstpath', 'mode', 'owner')
	fullpath: str
	dstpath: str
	mode: int | None
	owner: str | None
	
	def __init__(
		self,
		fullpath: str,
		dstpath: str | None = None,
		mode: int | None = None,
		owner: str | None = None
	):
		self.fullpath = realpath(fullpath)
		
		if dstpath is not None:
			self.dstpath = dstpath
		else:
			self.dstpath = basename(self.fullpath)
		
		if mode is not None:
			assert 0 <= mode < 1000
			assert 7 >= (mode % 1000) // 100	# user
			assert 7 >= (mode % 100) // 10		# group
			assert 7 >= (mode % 10) // 1		# everyone
		
		self.mode = mode
		self.owner = owner
	
	def get_dstpath(self) -> str:
		"""returns the absolute path to the local file"""
		return joinpath(CURDIR, 'dotfiles', self.dstpath)
	
	def get_fullpath(self) -> str:
		"""returns the absolute path to the in-use file"""
		return self.fullpath
	
	def get_perms(self) -> tuple[str, str]:
		"""returns mode and owner of file"""
		mode = self.mode
		owner = self.owner
		
		if owner is None:
			owner = environ['USER']
		if mode is None:
			# TODO: check source and dest files' mode
			mode = 644
		
		return (f"{mode:03d}", owner)
	
	def has_perms(self) -> bool:
		"""whether owner and mode of file are set"""
		return (self.mode is not None) or (self.owner is not None)

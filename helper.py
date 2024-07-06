#!/usr/bin/env python3
from sys import stdout
from subprocess import run

def lclean() -> None:
	"""clear line"""
	stdout.write("\r\033[2K")

def lprint(*args, **kwargs) -> None:
	"""print instantly to clean line"""
	lclean()
	print(*args, flush=True, **kwargs)

def lwrite(*args, **kwargs) -> None:
	"""write instantly to clean line"""
	lprint(*args, end="", **kwargs)

def linput(*args) -> str:
	"""clean line and request input"""
	lclean()
	return input(*args)


def pget(*args, **kwargs) -> str:
	"""Popen command and return stdout"""
	return run([*args], capture_output=True, **kwargs) \
		.stdout.decode('utf-8').strip()

def prun(*args, **kwargs) -> int:
	"""Popen command and return exit code"""
	return run([*args], check=True, **kwargs).returncode

def s_prun(*args, **kwargs) -> int:
	"""Popen command with sudo and return exit code"""
	return prun("sudo", *args, **kwargs)

def shget(cmd: str, **kwargs) -> str:
	"""shell command and return stdout"""
	return run(cmd, check=True, shell=True, capture_output=True, **kwargs) \
		.stdout.decode('utf-8').strip()

def shrun(cmd: str, **kwargs) -> int:
	"""shell command and return exit code"""
	return run(cmd, check=True, shell=True, capture_output=False, **kwargs) \
		.returncode

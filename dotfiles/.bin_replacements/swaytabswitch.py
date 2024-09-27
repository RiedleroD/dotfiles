#!/usr/bin/env python3
import json
from subprocess import Popen, PIPE
from typing import Any
from argparse import ArgumentParser

VERBOSE = False

def swaymsg(*cmd: str) -> Any:
	fullcmd = ['swaymsg', '--raw', *cmd]
	
	if VERBOSE:
		print(f"executing {fullcmd}")
	
	with Popen(fullcmd, stdout=PIPE) as p:
		return json.loads(p.communicate()[0])

def traverse_nodes(element: dict[str, Any], trvrs_lv: int = 0) -> list[dict[str, Any]]:
	tab = '\t' * trvrs_lv
	match element['type']:
		case 'workspace':
			if VERBOSE:
				print(f"{tab}> {element['type']} id={element['id']} layout={element['layout']}")
			out = []
			for node in element['nodes']:
				out += traverse_nodes(node, trvrs_lv + 1)
				node['nodes'] = None
			return out
		case 'con':
			match element['layout']:
				case 'none':
					if VERBOSE:
						print(f"{tab}+ {element['type']} id={element['id']} app='{element['app_id']}'")
					return [element]
				case _:
					if VERBOSE:
						print(f"{tab}> {element['type']} id={element['id']} layout={element['layout']}")
					out = []
					for node in element['nodes']:
						out += traverse_nodes(node, trvrs_lv + 1)
						node['nodes'] = None
					return out
		case _:
			raise Exception(f"Unknown node type: {element['type']}")

def switch_to_nth_window(n: int, clamp: bool):
	
	if n < 0:
		if clamp:
			n = 0
		else:
			raise ValueError(f"Number too low: {n} < 0")
	
	tree = swaymsg('-t', 'get_tree')
	workspaces = swaymsg('-t', 'get_workspaces')

	for ws in workspaces:
		if ws['focused']:
			focused_ws_id = ws['id']
			if VERBOSE:
				print(f"got workspace {ws['name']}")
				# print(ws)

	for output in tree['nodes']:
		for ws in output['nodes']:
			if ws['id'] == focused_ws_id:
				focused_ws = ws
				if VERBOSE:
					print(f"identified workspace {ws['name']}")
					# print(ws)

	eligible_windows = traverse_nodes(focused_ws)
	
	if n >= len(eligible_windows):
		if clamp:
			n = len(eligible_windows) - 1
		else:
			raise ValueError(f"Number too large: {n} > {len(eligible_windows) - 1}")
	
	win = eligible_windows[n]
	if VERBOSE:
		print(f"switching to window {win['id']}…")
	
	swaymsg(f"[con_id={win['id']}] focus")


if __name__ == '__main__':
	
	parser = ArgumentParser(
		prog='swaytabswitch.py',
		description='switches to nth window on a workspace'
	)
	parser.add_argument(
		'n',
		type=int,
		action='store'
	)
	parser.add_argument(
		'-v', '--verbose',
		action='store_true'
	)
	
	arguments = parser.parse_args()
	
	VERBOSE = arguments.verbose
	
	switch_to_nth_window(arguments.n - 1, True)

#!/usr/bin/ash

run_latehook() {
	# Make tty amber :3
	LD_LIBRARY_PATH="/new_root/usr/lib/:/new_root/usr/lib64/" /new_root/usr/bin/setvtrgb /new_root/etc/vtrgb_amber
}

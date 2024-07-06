#!/bin/sh

# this is part of a horrible bodge that needs to be removed eventually
# but yknow I didn't feel like actually doing some file parsing so there you go

for var in "$@"
do
	echo "$var"
done

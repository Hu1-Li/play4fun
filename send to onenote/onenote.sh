#!/bin/bash -
date '+%Y-%m-%d-%H-%M-%S'
source /home/lihui/.bashrc
if [[ $# -eq 1 ]]; then
	if [[ $1 = "--all" ]]; then
		vol=576
		while [[ $vol -gt 0 ]]; do
			#echo $vol
			lua onenote.lua $vol
			sleep 10
			((vol--));
		done
	elif echo $1 | grep '^[0-9][0-9]*$' > /dev/null; then
		lua onenote.lua $1
	fi
elif [[ $# -eq 2 ]]; then
	vol=$2
	while [[ $vol -gt $1 ]]; do
		#echo $vol
		lua onenote.lua $vol
		sleep 10
		((vol--));
	done
else
	lua onenote.lua
fi

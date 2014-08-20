#!/bin/bash -
date '+%Y-%m-%d-%H-%M-%S' >> log.txt
if [[ $# -eq 1 ]]; then
	if [[ $1 = "--all" ]]; then
		vol=576
		while [[ $vol -gt 0 ]]; do
			#echo $vol
			lua download_one.lua $vol && python mail.py && rm -f *.html
			sleep 10
			((vol--));
		done
	elif echo $1 | grep '^[0-9][0-9]*$' > /dev/null; then
		lua download_one.lua $1 && python mail.py && rm -f *.html
	fi
elif [[ $# -eq 2 ]]; then
		vol=$2
		while [[ $vol -gt $1 ]]; do
			#echo $vol
			lua download_one.lua $vol && python mail.py && rm -f *.html
			sleep 10
			((vol--));
		done
else
	lua download_one.lua && python mail.py && rm -f *.html
fi

#!/usr/bin/env bash

grep -Eo 'mul\([0-9]{1,3},[0-9]{1,3}\)' "$1" |
	sed -e 's/mul(//g' -e 's/)//g' -e 's/,/*/g' |
	paste -sd '+' |
	bc

# Right answer is 167090022

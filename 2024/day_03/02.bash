#!/usr/bin/env bash

grep -Eo "(mul\([0-9]{1,3},[0-9]{1,3}\)|do\(\)|don't\(\))" "$1" |
	sed -e "/don't()/,/do()/d" -e "/do()/d" |
	sed -e 's/mul(//g' -e 's/)//g' -e 's/,/*/g' |
	paste -sd '+' | bc

# Correct answer is 89823704

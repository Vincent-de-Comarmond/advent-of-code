#!/usr/bin/env bash
paste -d "-" <( cut -d" " -f1 "$1" | sort ) <( cut -d" " -f2- "$1" | sort) | bc | grep -oE "[0-9]+" | paste -sd "+" |bc

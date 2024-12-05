#!/usr/bin/env bash

readarray -t list1 < <(cut -d" " -f1 <"$1" | sort)
readarray -t list2 < <(tr -s " " <"$1" | cut -d" " -f2 | sort)
readarray -t uniques < <((
	printf "%s\n" "${list1[@]}" | uniq
	printf "%s\n" "${list2[@]}" | uniq
) | sort | uniq -c | grep -Ev "1 " | rev | cut -d " " -f1 | rev)

filter=$(printf "%s\n" "${uniques[@]}" | paste -sd "|")

paste -d " " <(printf "%s\n" "${list1[@]}" | grep -E "$filter" | sort | uniq -c) <(printf "%s\n" "${list2[@]}" | grep -E "$filter" | sort | uniq -c) | tr -s " " | cut -d" " -f-4 | sed -Ee "s/ +/ /g" -e 's/^ //' -e 's/ /\*/g' | bc | paste -sd "+" | bc

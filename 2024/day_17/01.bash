#!/usr/bin/env bash

declare -i a b c instruction operand combo pointer=0
declare -a program output

a=$(sed -n 1p <"$1" | cut -d " " -f 3)
b=$(sed -n 2p <"$1" | cut -d " " -f 3)
c=$(sed -n 2p <"$1" | cut -d " " -f 3)
readarray -d , -t program < <(tail -n1 "$1" | cut -d " " -f2)

if [[ "$2" != "" ]]; then a="$2"; fi

# Each instruction also reads the 3-bit number after it as an input; this is called its operand.
while ((0 <= pointer && pointer < ${#program[@]})); do

	instruction="${program[$pointer]}"
	operand="${program[$((pointer + 1))]}"

	if ((operand <= 3)); then
		((combo = operand))
	elif ((operand == 4)); then
		((combo = a))
	elif ((operand == 5)); then
		((combo = b))
	elif ((operand == 6)); then
		((combo = c))
	fi

	case "$instruction" in
	0)
		((a = a / (2 ** combo)))
		((pointer += 2))
		;;
	1)
		((b = b ^ operand))
		((pointer += 2))
		;;
	2)
		((b = combo % 8))
		((pointer += 2))
		;;
	3)
		if ((a != 0)); then ((pointer = operand)); else ((pointer += 2)); fi
		;;
	4)
		((b = b ^ c))
		((pointer += 2))
		;;
	5)
		output+=($((combo % 8)))
		((pointer += 2))
		;;
	6)
		((b = a / (2 ** combo)))
		((pointer += 2))
		;;
	7)
		((c = a / (2 ** combo)))
		((pointer += 2))
		;;
	esac
done

printf -v joined '%s,' "${output[@]}"
echo "${joined%,}"

# 2,0,4,2,7,0,1,0,3 is the right answer for part 1

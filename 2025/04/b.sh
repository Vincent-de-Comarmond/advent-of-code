#!/bin/bash
input_grid="$(sed 's/[^@]/0/g;s/@/1/g' $1)"
init_size="$(wc -m <<< "${input_grid//[^1]}")"
prev_grid=""

while [[ "$prev_grid\n" != "$input_grid" ]]; do
	prev_grid="$input_grid"
	input_grid="$(awk -f b.awk <<<"$input_grid")"
	echo "$prev_grid" "$input_grid"
done

final_size="$(wc -m <<< "${input_grid//[^1]}")"
echo $((init_size - final_size))

# 9122 is the right answer for part 2

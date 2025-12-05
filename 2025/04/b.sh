#!/bin/bash
input_grid="$(sed 's/[^@]/0/g;s/@/1/g' $1)"
init_size="$(wc -m <<< "${input_grid//[^1]}")"
prev_grid=""

function transform(){
    awk '
	{ count_paper($0) }
	END { count_paper("") }

	function count_paper(input, i, subtotal, j) {
		cycle(input)
		if (length(b) == 0) {
			return
		}
		for (i = 1; i <= length(b); i++) {
			if (substr(b, i, 1) == "0") {
				printf "0"
			} else {
				subtotal = 0
				for (j = i - 1; j <= i + 1; j++) {
					if ((1 <= j) && j <= length($0)) {
						subtotal += substr(a, j, 1) + substr(c, j, 1)
						subtotal += j != i ? substr(b, j, 1) : 0
					}
				}
				printf subtotal < 4 ? "0" : 1
			}
		}
		print ""
	}

	function cycle(input) {
		c = b; b = a; a = input
	}' <<< "${1:-/dev/stdin}"
}


while [[ "$prev_grid" != "$input_grid" ]]; do
	prev_grid="$input_grid"
	input_grid="$(transform "$input_grid")"
done

final_size="$(wc -m <<< "${input_grid//[^1]}")"
echo $((init_size - final_size))

# 9122 is the right answer for part 2

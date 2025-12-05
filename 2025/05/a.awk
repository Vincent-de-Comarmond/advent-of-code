BEGIN {
	FS = "-"
	split("", range, "")
	fresh_ingredients = 0
}

/-/ {
	range[NR][0] = $1
	range[NR][1] = $2
}

/^[0-9]+$/ {
	for (idx in range) {
		if (range[idx][0] <= $1 && $1 <= range[idx][1]) {
			fresh_ingredients++
			break
		}
	}
}

END {
	print "Fresh ingredients:", fresh_ingredients
}

# 661 is the right answer for part 1

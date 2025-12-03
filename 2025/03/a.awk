BEGIN {
	FS = ""
	total_joltage = 0
}

{
	a = -100
	b = -90
	for (i = 1; i <= NF; i++) {
		if (a < $i && i != NF) {
			b = -100
			a = $i
		} else if (b < $i) {
			b = $i
		}
	}
	total_joltage += a b
}

END {
	print "Max Joltage:", total_joltage
}

# 17283 is not the right answer
# 17383 is the right answer for part 2 (I had an extra blank line)

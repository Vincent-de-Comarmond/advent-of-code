BEGIN { FS = ", " }

/,/ {
	for (i = 1; i <= NF; i++) {
		PATTERNS[$i] = 1
	}
	next
}

/^\s*$/ { next }

{ total += result = make_towel($1) }
END { print total }

# 371 is the right answer for part 1

function make_towel(desired_pattern,        pattern, tmp, max) {
	if (length(desired_pattern) == 0) {
		return 1
	}
	max = 0
	for (pattern in PATTERNS) {
		if (pattern == substr(desired_pattern, 1, length(pattern))) {
			tmp = make_towel(substr(desired_pattern, length(pattern) + 1))
			if (tmp == 1) {
				return tmp
			} else {
				max = (tmp > max) ? tmp : max
			}
		}
	}
	return max
}

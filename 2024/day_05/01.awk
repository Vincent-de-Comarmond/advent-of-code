BEGIN {
	FS = "|"
	total = 0
	split("", rules, FS)
}

/[0-9]+\|[0-9]+/ { rules[$1][$2] = 1 }

/^[[:space:]]*$/ { FS = "," }

/,/ {
	for (i = 1; i <= NF; i++) {
		if (isarray(rules[$i])) {
			for (j in rules[$i]) {
				regexp = j ".*" $i
				if ($0 ~ regexp) {
					next
				}
			}
		}
	}
	idx = int(1 + NF / 2)
	total += $idx
}

END { print total }
# 4135 is the correct answer

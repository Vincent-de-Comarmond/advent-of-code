BEGIN {
	FS = ""
	split("", columns, "")
}

/[0-9]/ {
	for (i = NF; 1 <= i; i--) {
		columns[i] = columns[i] $i
	}
}

/(+|*)/ {
	idx = 0
	total = 0
	split("", buf, "")
	for (i = NF; 1 <= i; i--) {
		number = columns[i]
		if (number ~ /^\s*$/) {
			continue
		}
		buf[++idx] = number
		if ($i ~ /+|*/) {
			stot = ($i == "+") ? 0 : 1
			for (j = 1; j <= idx; j++) {
				stot = ($i == "+") ? stot + buf[j] : stot * buf[j]
			}
			total += stot
			idx = 0
			split("", buf, "")
		}
	}
	print "Grand total:", total
}

# 7858808482092 is the right answer for part 2

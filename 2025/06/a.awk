BEGIN {
	idx = 0
	total = 0
	split("", numbers, "")
}

/[0-9]/ {
	idx++
	for (i = 1; i <= NF; i++) {
		numbers[idx, i] = $i
	}
}

/(+|*)/ {
	for (i = 1; i <= NF; i++) {
		subtotal = numbers[1, i]
		for (j = 2; j <= idx; j++) {
			if ($i == "+") {
				subtotal += numbers[j, i]
			} else {
				subtotal *= numbers[j, i]
			}
		}
		total += subtotal
	}
	print "Grand total:", total
}

# 4412382293768 is the right 

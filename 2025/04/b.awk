BEGIN {
	split("", doc, "")
	initial = 0
}

{
	gsub(/[^@]/, 0, $0)
	initial += gsub(/@/, 1, $0)
	doc[NR] = $0
}

END {
	len = length(doc[1])
	loop = 1
	while (loop == 1) {
		loop = 0
		for (i = 1; i <= NR; i++) {
			a = doc[i + 1]
			b = doc[i]
			c = doc[i - 1]
			tmp = ""
			for (j = 1; j <= len; j++) {
				if (substr(b, j, 1) == 0) {
					tmp = tmp 0
					continue
				}
				subtotal = 0
				for (k = j - 1; k <= j + 1; k++) {
					if (k < 1 || len < k) {
						continue
					}
					subtotal += substr(a, k, 1) + substr(c, k, 1) + substr(b, k, 1)
				}
				if (subtotal < 5) {
					tmp = tmp 0
					loop = 1
				} else {
					tmp = tmp 1
				}
			}
			doc[i] = tmp
		}
	}
	for (i = 1; i <= NR; i++) {
		final += gsub(1, 1, doc[i])
	}
	print initial - final
}

# 9122 is the right answer for part 2

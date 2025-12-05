{
	c = b
	b = a
	a = $0
	count_paper(a, b, c)
}

END {
	c = b
	b = a
	a = ""
	count_paper(a, b, c)
}


function count_paper(a, b, c, i, subtotal, j)
{
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

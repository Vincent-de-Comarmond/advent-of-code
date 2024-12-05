{
	split($0, tmp, "")
	for (i in tmp) {
		charmap[NR, i] = tmp[i]
	}
}

END {
	counts = 0
	for (idx in charmap) {
		char = charmap[idx]
		if (char == "A") {
			split(idx, tmp, SUBSEP)
			counts += search_xmas(charmap, tmp[1], tmp[2])
		}
	}
	print counts
}

# 2034 is the correct solution

function search_xmas(charmap, i, j, diag1, diag2)
{
	diag1 = charmap[i - 1, j - 1] charmap[i, j] charmap[i + 1, j + 1]
	diag2 = charmap[i - 1, j + 1] charmap[i, j] charmap[i + 1, j - 1]
	if ((diag1 == "MAS" || diag1 == "SAM") && (diag2 == "MAS" || diag2 == "SAM")) {
		return 1
	}
	return 0
}

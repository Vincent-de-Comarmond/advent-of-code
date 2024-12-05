{
	split($0, tmp, "")
	for (i in tmp) {
		charmap[NR, i] = tmp[i]
	}
}

END {
	counts = 0
	height = NR
	width = length(tmp)
	for (idx in charmap) {
		char = charmap[idx]
		if (char == "X") {
			split(idx, tmp, SUBSEP)
			counts += search_mas(charmap, tmp[1], tmp[2], 0, -1)
			counts += search_mas(charmap, tmp[1], tmp[2], 1, -1)
			counts += search_mas(charmap, tmp[1], tmp[2], 1, 0)
			counts += search_mas(charmap, tmp[1], tmp[2], 1, 1)
			counts += search_mas(charmap, tmp[1], tmp[2], 0, 1)
			counts += search_mas(charmap, tmp[1], tmp[2], -1, 1)
			counts += search_mas(charmap, tmp[1], tmp[2], -1, 0)
			counts += search_mas(charmap, tmp[1], tmp[2], -1, -1)
		}
	}
	print counts
}

# 2662 is the right answer

function search_mas(charmap, i, j, dir_i, dir_j, _i, _j, _k, _search_string)
{
	_i = i
	_j = j
	for (_k = 1; _k <= length("MAS"); _k++) {
		_i += dir_i
		_j += dir_j
		if (charmap[_i, _j] != substr("MAS", _k, 1)) {
			return 0
		}
	}
	return 1
}

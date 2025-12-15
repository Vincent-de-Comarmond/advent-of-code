BEGIN {
	FS = ","
	split("", red, "")
	split("", borders, "")
}

{
	red[NR][1] = $1
	red[NR][2] = $2
}

1 < NR {
	add_border(red, NR, NR - 1)
}

END {
	add_border(red, 1, NR)
	split("", areas, "")
	for (i = 1; i <= NR; i++) {
		for (j = 1; j < i; j++) {
			areas[i, j] = area(red[i][1], red[i][2], red[j][1], red[j][2])
		}
	}
	split("", sorted_areas, "")
	n = asorti(areas, sorted_areas, "@val_num_desc")
	for (k = 1; k <= n; k++) {
		if (k % 1000 == 0) {
			printf "Progress (full search): %.2f %\n", 100 * k / n
		}
		split(sorted_areas[k], a, SUBSEP)
		i = a[1]
		j = a[2]
		if (is_valid(red, i, j)) {
			print "Max area:", areas[i, j]
			exit (0)
		}
	}
	# 4406010323 is too big for part 2
	# 1474699155 is the right answer for part 2
}


function abs(x)
{
	return (0 <= x ? x : -x)
}

function add_border(reds, idx1, idx2, i, j)
{
	i = min(reds[idx1][1], reds[idx2][1])
	while (i <= max(reds[idx1][1], reds[idx2][1])) {
		j = min(reds[idx1][2], reds[idx2][2])
		while (j <= max(reds[idx1][2], reds[idx2][2])) {
			borders[i][j] = 1
			borders2[idx][1] = i
			borders2[idx][2] = j
			idx++
			j++
		}
		i++
	}
}

function area(x0, y0, x1, y1)
{
	return (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1)
}

function is_valid(reds, idx1, idx2, x0, y0, x1, y1, x, y, _min1, _max1, _min2, _max2)
{
	x0 = reds[idx1][1]
	y0 = reds[idx1][2]
	x1 = reds[idx2][1]
	y1 = reds[idx2][2]
	_min1 = min(x0, x1)
	_max1 = max(x0, x1)
	for (x in borders) {
		if (_min1 + 0 < x + 0 && x + 0 < _max1 + 0) {
			for (y in borders[x]) {
				if (min(y0, y1) + 0 < y + 0 && y + 0 < max(y0, y1) + 0) {
					return 0
				}
			}
		}
	}
	return 1
}

function max(a, b)
{
	return (a + 0 <= b + 0 ? b + 0 : a + 0)
}

function min(a, b)
{
	return (a + 0 <= b + 0 ? a : b)
}

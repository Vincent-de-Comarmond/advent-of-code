BEGIN {
	FS = ","
	split("", red, "")
	split("", horz, "")
	split("", vert, "")
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
		split(sorted_areas[k], a, SUBSEP)
		i = a[1]
		j = a[2]
		if (is_valid(red, i, j)) {
            print red[i][1], red[i][2], red[j][1], red[j][2]
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

function add_border(reds, idx1, idx2, idx)
{
	if (reds[idx1][1] == reds[idx2][1]) {
		# Vertical line - 1 x value
		idx = length(vert) + 1
		vert[idx][0] = reds[idx1][1]
		vert[idx][1] = min(reds[idx1][2], reds[idx2][2])
		vert[idx][2] = max(reds[idx1][2], reds[idx2][2])
	} else {
		# Horizontal line -  1 y value
		idx = length(horz) + 1
		horz[idx][0] = reds[idx1][2]
		horz[idx][1] = min(reds[idx1][1], reds[idx2][1])
		horz[idx][2] = max(reds[idx1][1], reds[idx2][1])
	}
}

function area(x0, y0, x1, y1)
{
	return (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1)
}

function is_valid(reds, idx1, idx2, x0, y0, x1, y1, idx)
{
	x0 = min(reds[idx1][1], reds[idx2][1])
	x1 = max(reds[idx1][1], reds[idx2][1])
	y0 = min(reds[idx1][2], reds[idx2][2])
	y1 = max(reds[idx1][2], reds[idx2][2])
	# Vertical border crossing rectange
	for (idx in vert) {
		if (x0 + 0 < vert[idx][0] && vert[idx][0] < x1 + 0) {
			# Cuts y0
			if (vert[idx][1] < y0 + 0 && y0 + 0 < vert[idx][2]) {
				return 0
			}
			# Cuts y1
			if (vert[idx][1] < y1 + 0 && y1 + 0 < vert[idx][2]) {
				return 0
			}
			# Inside the rectange
			if (y0 + 0 <= vert[idx][1] && vert[idx][2] <= y1 + 0) {
				return 0
			}
		}
	}
	# Horizontal border crossing rectange
	for (idx in horz) {
		if (y0 + 0 < horz[idx][0] && horz[idx][0] < y1 + 0) {
			# Cuts x0
			if (horz[idx][1] < x0 + 0 && x0 + 0 < horz[idx][2]) {
				return 0
			}
			# Cuts x1
			if (horz[idx][1] < x1 + 0 && x1 + 0 < horz[idx][2]) {
				return 0
			}
			# Inside the rectange
			if (x0 + 0 <= horz[idx][1] && horz[idx][2] <= x1 + 0) {
				return 0
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

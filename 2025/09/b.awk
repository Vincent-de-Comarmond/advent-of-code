BEGIN {
	FS = ","
	split("", red, "")
	split("", green_h, "")
	split("", green_v, "")
}

{
	red[NR][1] = $1
	red[NR][2] = $2
	if (1 < NR) {
		add_green(NR - 1, NR)
	}
}

END {
	add_green(NR, 1)
	idx = 0
	maxsize = 0
	iters = NR * (NR - 1) / 2
	split("", done, "")
	for (i = 1; i <= NR; i++) {
		for (j = 1; j < i; j++) {
			idx++
			if (idx % 100 == 0) {
				printf "%.2f %\n", 100 * idx / iters
			}
			if ((i, j) in done || (j, i) in done) {
				continue
			}
			done[i, j] = 1
			x1 = red[i][1]
			y1 = red[i][2]
			x2 = red[j][1]
			y2 = red[j][2]
			dx = (x1 < x2) ? x2 - x1 : x1 - x2
			dy = (y1 < y2) ? y2 - y1 : y1 - y2
			size = (dx + 1) * (dy + 1)
			if (size < maxsize) {
				continue
			}
			# print size
			if (invalid(x1, y1, x2, y2) == 1) {
				continue
			}
			maxsize = size
			mx1 = x1
			my1 = y1
			mx2 = x2
			my2 = y2
		}
	}
	print "Max size:", maxsize
	printf "%d, %d -> %d, %d\n", mx1, my1, mx2, my2
}


function add_green(prev_idx, curr_idx, px, py, x, y, dx, dy, i, b, e)
{
	px = red[prev_idx][1]
	py = red[prev_idx][2]
	x = red[curr_idx][1]
	y = red[curr_idx][2]
	dx = x - px
	dy = y - py
	if (dx == 0) {
		b = py < y ? py : y
		e = py < y ? y : py
		for (i = b + 1; i < e; i++) {
			# green_v[i][x] = 1
			green_v[x, y] = 1
		}
	} else {
		b = px < x ? px : x
		e = px < x ? x : px
		for (i = b + 1; i < e; i++) {
			green_h[i][y] = 1
		}
	}
}

function invalid(x1, y1, x2, y2, x, y, xmin, xmax, ymin, ymax)
{
	xmin = x1 < x2 ? x1 : x2
	xmax = x1 < x2 ? x2 : x1
	ymin = y1 < y2 ? y1 : y2
	ymax = y1 < y2 ? y2 : y1
	for (y = ymin; y <= ymax; y++) {
		for (x = xmin + 1; x < xmax; x++) {
			if ((x, y) in green_v) {
				return 1
			}
		}
	}
	# if (y1 in green_v) {
	# 	for (x in green_v[y1]) {
	# 		if (min < x && x < max) {
	# 			return 1
	# 		}
	# 	}
	# }
	# if (y2 in green_v) {
	# 	for (x in green_v[y2]) {
	# 		if (min < x && x < max) {
	# 			return 1
	# 		}
	# 	}
	# }
	# min = y1 < y2 ? y1 : y2
	# max = y1 < y2 ? y2 : y1
	# if (x1 in green_h) {
	# 	for (y in green_h[x1]) {
	# 		if (min < y && y < max) {
	# 			return 1
	# 		}
	# 	}
	# }
	# if (x2 in green_h) {
	# 	for (y in green_h[x2]) {
	# 		if (min < y && y < max) {
	# 			return 1
	# 		}
	# 	}
	# }
	return 0
}

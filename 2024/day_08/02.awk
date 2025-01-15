{
	split($0, tmp, "")
	for (i in tmp) {
		grid[NR, i] = tmp[i]
		if (tmp[i] != ".") antgrid[tmp[i]][NR, i] = 1
	}
}

END {
	height = NR
	width = length($0)
	split("", antinodes, FS)
	draw_lines(antgrid, antinodes)
	print length(antinodes)
	# 809 is the correct answer
}


function draw_lines(antennaegrid, antinodes,        point1, p1, point2, p2, i, j){
	for (symbol in antennaegrid) {
		for (point1 in antennaegrid[symbol]) {
			for (point2 in antennaegrid[symbol]) {
				if (point1 == point2) continue
				split(point1, p1, SUBSEP)
				split(point2, p2, SUBSEP)
				dy = p2[1] - p1[1]
				dx = p2[2] - p1[2]
				if (dy == 0) {
					for (i = 1; i <= height; i++) antinodes[i, p1[2]] = 1
					continue
				}
				if (dx == 0) {
					for (j = 1; j <= width; j++) antinodes[p1[1], j] = 1
					continue
				}
				for (i = 1; i <= height; i++) {
					for (j = 1; j <= width; j++) {
						if ((i == p1[1]) || (j == p1[2])) continue
						if ((i - p1[1]) / (j - p1[2]) == dy / dx) antinodes[i, j] = 1
					}
				}
			}
		}
	}
}

{
	split($0, tmp, "")
	for (i in tmp) {
		grid[NR, i] = tmp[i]
		if (tmp[i] != ".") {
			antgrid[tmp[i]][NR, i] = 1
		}
	}
}

END {
	height = NR
	width = length($0)
	split("", antinodes, FS)
	for (gridpoint in grid) {
		if (gridpoint in antinodes) continue
		if (isantinode(gridpoint, antgrid) == 1) antinodes[gridpoint] = 1
	}
	print length(antinodes)
	# 214 is the correct answer
}


function abs(value){
	return (value >= 0) ? value : -value
}

function hammingdistance(point1, point2, tmp1, tmp2)
{
	split(point1, tmp1, SUBSEP)
	split(point2, tmp2, SUBSEP)
	return (abs(tmp1[1] - tmp2[1]) + abs(tmp1[2] - tmp2[2]))
}

function isantinode(gridpoint, antgrid, symbol, ij, distance){
	for (symbol in antgrid) {
		for (ij in antgrid[symbol]) {
			distance = hammingdistance(gridpoint, ij)
			if (project(gridpoint, ij, distance / 2) in antgrid[symbol]) return 1
			if (project(gridpoint, ij, distance * 2) in antgrid[symbol]) return 1
		}
	}
	return 0
}

function printgrid(inputgrid, i, j){
	for (j = 1; j <= height; j++) {
		for (i = 1; i <= width; i++) printf inputgrid[j, i]
		print ""
	}
}

function project(point1, point2, dist, tmp1, tmp2, d, dy, dx, y, x){
	split(point1, tmp1, SUBSEP)
	split(point2, tmp2, SUBSEP)
	dy = tmp2[1] - tmp1[1]
	dx = tmp2[2] - tmp1[2]
	d = hammingdistance(point1, point2)
	return (d > 0) ? (tmp1[1] + dy * dist / d) SUBSEP (tmp1[2] + dx * dist / d) : -1 (SUBSEP - 1)
}

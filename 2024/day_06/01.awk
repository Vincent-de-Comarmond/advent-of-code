{
	split($0, tmp, "")
	for (i in tmp) grid[NR][i] = tmp[i]
}

/\^/ {
	pos_y = NR
	pos_x = index($0, "^")
	width=length($0)
}

END {
	step(pos_y, pos_x, 0)
	print count()
}


function count(i, j, cnt)
{
	for (i in grid) {
		for (j in grid[i]) {
			cnt += (grid[i][j] == "X") ? 1 : 0
		}
	}
	return cnt
}

function printgrid(i, j)
{
	for (i = 1; i <= NR; i++) {
		for (j in grid[i]) {
			printf grid[i][j]
		}
		print ""
	}
}

function step(loc_y, loc_x, dir, prev, total, current, k, dx, dy)
{
	current = grid[loc_y][loc_x]
	grid[loc_y][loc_x] = "X"
	for (k == 0; k < 4; k++) {
		dir = (dir + k) % 4
		dx = (2 - dir) % 2
		dy = (dir % 2 == 0) ? dir - 1 : 0

		if (loc_y + dy > NR) return
		if (loc_y + dy <= 0) return
		if (loc_x + dx > width) return
		if (loc_x + dx <= 0) return
		if (grid[loc_y + dy][loc_x + dx] != "#") {
			return step(loc_y + dy, loc_x + dx, dir, current, total + 1)
		}
	}
}

# 5177 is the correct answer

BEGIN {
	FS = ","
	split("", red, "")
}

{
	red[NR][1] = $1
	red[NR][2] = $2
}

END {
	maxsize = 0
	for (i = 1; i <= NR; i++) {
		for (j = 1; j < i; j++) {
			dx = abs(red[i][1] - red[j][1])
			dy = abs(red[i][2] - red[j][2])
			maxsize = max(maxsize, (dx + 1) * (dy + 1))
		}
	}
	print "Max size:", maxsize
	# 4758598740 is the right answer for part 1
}


function abs(x)
{
	return (0 <= x ? x : -x)
}

function max(x, y)
{
	return (x <= y ? y : x)
}

BEGIN {
	split("", puzzle, "")
	split("", active, "")
}

{
	key = substr($1, 1, length($1) - 1)
	for (i = 2; i <= NF; i++) {
		puzzle[key][$i] = 1
	}
}

END {
	print "Number paths:", solve("you", "out")
	# 670 is the right answer for part 1
}


function solve(src, dst, child, t)
{
	if (dst in puzzle[src]) {
		return 1
	} else {
		for (child in puzzle[src]) {
			t += solve(child, dst, "")
		}
		return t
	}
}

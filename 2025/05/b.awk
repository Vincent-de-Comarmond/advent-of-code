BEGIN {
	FS = "-"
	split("", range, "")
}

/-/ {
	range[NR][1] = $1
	range[NR][2] = $2
}

/^\s*$/ {
	sort_and_consolidate()
	exit 0
}


function custom_sort(i1, v1, i2, v2)
{
	if (v1[1] < v2[1]) {
		return -1
	}
	if (v1[1] == v2[1]) {
		return (v2[2] < v1[2] ? -1 : v1[2] == v2[2] ? 0 : 1)
	}
	return 1
}

function sort_and_consolidate(no_fresh_possible, n, tmp, i, a, b)
{
	no_fresh_possible = 0
	n = asort(range, tmp, "custom_sort")
	a = tmp[1][1]
	b = tmp[1][2]
	for (i = 2; i <= n; i++) {
		if (tmp[i][1] <= b) {
			b = b < tmp[i][2] ? tmp[i][2] : b
		} else {
			no_fresh_possible += b - a + 1
			a = tmp[i][1]
			b = tmp[i][2]
		}
	}
	no_fresh_possible += b - a + 1
	print "Possible fresh ingredients:", no_fresh_possible
}
# 359526404143208 is the right answer for part 2

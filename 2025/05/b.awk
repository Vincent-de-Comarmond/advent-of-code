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

function sort_and_consolidate(consolidated, no_fresh_possible, n, tmp, i, idx, a, b, diff)
{
	idx = 0
	split("", consolidated, "")
	no_fresh_possible = 0
	n = asort(range, tmp, "custom_sort")
	a = tmp[1][1]
	b = tmp[1][2]
	for (i = 2; i <= n; i++) {
		if (tmp[i][1] <= b) {
			b = b < tmp[i][2] ? tmp[i][2] : b
		} else {
			idx++
			consolidated[idx][1] = a
			consolidated[idx][2] = b
			a = tmp[i][1]
			b = tmp[i][2]
		}
	}
	idx++
	consolidated[idx][1] = a
	consolidated[idx][2] = b
	for (i = 1; i <= idx; i++) {
		diff = 1 + consolidated[i][2] - consolidated[i][1]
		no_fresh_possible += diff
	}
	print "Possible fresh ingredients:", no_fresh_possible
}

# 359526404143208 is the right answer for part 2

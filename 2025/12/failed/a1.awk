BEGIN {
	FS = ""
	pres_idx = 1
	split("", sizes, FS)
	#
	split("", inefficiency, FS)
	#
	obviously_fit = 0
	obviously_dont_fit = 0
	unclear = 0
	as_8_fit = 8
}

/#|\./ {
	for (i = 1; i <= 3; i++) {
		sizes[pres_idx] += $1 == "#" ? 1 : 0
	}
	if (3 < row_idx) {
		pres_idx++
	}
}

/x/ {
	gsub(/:/, "", $0)
	gsub(/x/, " ", $0)
	split($0, a, " ")
	#
	split("", desired, FS)
	for (i = 3; i <= length(a); i++) {
		desired[i - 2] = a[i]
	}
	solve_one(a[1], a[2], desired)
}

END {
	print "Obviously fit:", obviously_fit
	print "Obviously don't fit:", obviously_dont_fit
	print "Unclear:", unclear
	print "As 8 fit:", as_8_fit
	# 387 is the wrong answer for part 1
}


function solve_one(_width, _length, desired_array, area, outer_area, inner_area, as_8_area)
{
	area = _width * _length
	outer_area = 0
	inner_area = 0
	as_8_area = 0
	for (i = 1; i <= length(desired); i++) {
		outer_area += 3 * 3 * desired[i]
		inner_area += sizes[i] * desired[i]
		as_8_area += 8 * desired[i]
	}
	if (as_8_area <= area) {
		as_8_fit++
	}
	if (outer_area < area) {
		obviously_fit++
	}
	if (area < inner_area) {
		obviously_dont_fit++
	}
	if (inner_area <= area && area <= outer_area) {
		printf "Line %d is unclear\n", NR
		unclear++
	}
}

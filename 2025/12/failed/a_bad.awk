BEGIN {
	FS = ""
	# row_idx = 1
	pres_idx = 1
	# split("", shapes, FS)
	split("", sizes, FS)
	#
	split("", inefficiency, FS)
	inefficiency[1] = 15.0 / 16.0	# Slightly worse at edges
	inefficiency[2] = 15.0 / 16.0	# slightly worse at edges
	inefficiency[3] = 14.0 / 16.0	# Unaffected
	inefficiency[4] = 1.0	# Perfect - excluding corner
	inefficiency[5] = 1.0	# Perfect
	inefficiency[6] = 14.0 / 16.0	# Loose 1 per 2 on edges
	#
	lower_bound = 0
	upper_bound = 0
	edge_cases = 0
	estimated_number = 0
}

/#|\./ {
	for (i = 1; i <= 3; i++) {
		sizes[pres_idx] += $1 == "#" ? 1 : 0
	}
	# shapes[pres_idx][row_idx][1] = $1 == "#" ? 1 : 0
	# shapes[pres_idx][row_idx][2] = $2 == "#" ? 1 : 0
	# shapes[pres_idx][row_idx][3] = $3 == "#" ? 1 : 0
	# row_idx++
	if (3 < row_idx) {
		pres_idx++
		# row_idx = 1
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
	estimated_number += solve_one(a[1], a[2], desired)
}

END {
	printf "Packable between %d and %d\n", lower_bound, upper_bound
	print "Possible number edge cases:", edge_cases
	print "Estimated number:", estimated_number
	# 480 is too high for part 1
	# 474 is too high for part 1
	# 419 is still too high and I'm stumped
	# From the other side 387 is also wrong
	# 400 is the wrong answer
	# 411 is wrong (as 8 fit)
}


function ceil(num)
{
	return (num == int(num) ? num : int(num) + 1)
}

function print_array(input_arr, i)
{
	for (i = 1; i <= length(input_arr); i++) {
		printf (1 < i) ? " %d" : "%d", input_arr[i]
	}
	print ""
}

function solve_one(_width, _length, desired_array, area, rem_area, perimeter, est, losses)
{
	area = _width * _length
	rem_area = area
	perimeter = 2 * _width + 2 * _length
	for (i = 1; i <= length(desired); i++) {
		rem_area -= sizes[i] * desired[i] / inefficiency[i]
	}
	if (perimeter < rem_area) {
		lower_bound++
	}
	if (0 < rem_area) {
		upper_bound++
	}
	if (0 < rem_area && rem_area <= perimeter) {
		# print "Remaining area:", rem_area
		# printf "LINE %d: WARNING ... POSSIBLE EDGE CASE DETECTED FOR LINE %dx%d: ", NR, _width, _length
		# print_array(desired_array)
		edge_cases++
		#########################
		# estimate edge effects #
		#########################
		# Estimate a few remaining area lost per each of the above type on the perimeter
		# losses = ceil(perimeter * desired[1] / area) + ceil(perimeter * desired[2] / area) + ceil(perimeter * desired[3] / area)
		losses = ceil(perimeter / 3)
		if (rem_area < 2 * losses) {
			printf "########\nLine %d is unclear\n", NR
			print "Remaining area:", rem_area
			print "Number of type 1 on edge:", perimeter * 1.0 * desired[1] / area
			print "Number of type 2 on edge:", perimeter * 1.0 * desired[2] / area
			print "Number of type 6 on edge:", perimeter * 1.0 * desired[6] / area
			return 0
		} else {
			return 1
		}
	}
	return (0 < rem_area)
}

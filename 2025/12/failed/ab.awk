BEGIN {
	FS = ""
	split("", SHAPES, FS)
	split("", GALLERY, FS)
	#
	ROW_IDX = 1
	PRES_IDX = 1
	NUM_POSSIBLE = 0
}

/#|\./ {
	SHAPES[PRES_IDX][ROW_IDX][1] = $1
	SHAPES[PRES_IDX][ROW_IDX][2] = $2
	SHAPES[PRES_IDX][ROW_IDX][3] = $3
	ROW_IDX++
	if (3 < ROW_IDX) {
		add_to_gallery(PRES_IDX)
		PRES_IDX++
		ROW_IDX = 1
	}
}

/x/ {
	gsub(/:/, "", $0)
	gsub(/x/, " ", $0)
	split($0, a, " ")
	#
	split("", desired, FS)
	for (i = 3; i <= length(a); i++) {
		desired[1][i - 2] = a[i]
	}
	split("", canvases, FS)
	canvases[1][1][1] = 0
	make_canvas(a[1], a[2], canvases[1])
	calls = 0
	is_possible = is_packable(canvases, desired, 1000)
	NUM_POSSIBLE += is_possible
	print NR, ":", is_possible
}

END {
	print "Number possible:", NUM_POSSIBLE
}


function abs(x)
{
	return (x < 0 ? -x : x)
}

function add_to_gallery(present_index, idx, rep)
{
	#############
	# rotations #
	#############
	split("", rot1, FS)
	split("", rot2, FS)
	split("", rot3, FS)
	rotate(SHAPES[present_index], rot1)
	rotate(rot1, rot2)
	rotate(rot2, rot3)
	# flip
	split("", flipped, FS)
	flip(SHAPES[present_index], flipped)
	#####################
	# flipped_rotations #
	#####################
	split("", frot1, FS)
	split("", frot2, FS)
	split("", frot3, FS)
	rotate(flipped, frot1)
	rotate(frot1, frot2)
	rotate(frot2, frot3)
	#############################################################
	# force awk to treat GALLERY as a minimum 3 dimension array #
	#############################################################
	for (idx = 1; idx <= 8; idx++) {
		GALLERY[present_index][idx][-1] = -1
	}
	##################
	# add to GALLERY #
	##################
	idx = 1
	split("", deduplicator, FS)
	copy_matrix(SHAPES[present_index], GALLERY[present_index][idx])
	deduplicator[matrixtostring(SHAPES[present_index])] = 1
	idx++
	rep = matrixtostring(rot1)
	if (! (rep in deduplicator)) {
		copy_matrix(rot1, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(rot2)
	if (! (rep in deduplicator)) {
		copy_matrix(rot2, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(rot3)
	if (! (rep in deduplicator)) {
		copy_matrix(rot3, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(flipped)
	if (! (rep in deduplicator)) {
		copy_matrix(flipped, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot1)
	if (! (rep in deduplicator)) {
		copy_matrix(frot1, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot2)
	if (! (rep in deduplicator)) {
		copy_matrix(frot2, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot3)
	if (! (rep in deduplicator)) {
		copy_matrix(frot3, GALLERY[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	for (idx = 1; idx <= 8; idx++) {
		delete GALLERY[present_index][idx][-1]
		if (length(GALLERY[present_index][idx]) == 0) {
			delete GALLERY[present_index][idx]
		}
	}
}

function assess_canvas(canvas, x, y, n, i, j, total)
{
	n = 0
	# collect coordinates
	for (i in canvas) {
		for (j in canvas[i]) {
			if (canvas[i][j] != ".") {
				n++
				x[n] = i
				y[n] = j
			}
		}
	}
	# sort coordinates
	asort(x)
	asort(y)
	# compute Manhattan distance
	total = sum_abs_sorted(x, n) + sum_abs_sorted(y, n)
	# average distance per tile
	return (2 * total / n)
}

function can_insert(_canvas, x, y, shape_matrix, i, j)
{
	for (i = 1; i <= 3; i++) {
		if (! ((x + i - 1) in _canvas)) {
			return 0
		}
		for (j = 1; j <= 3; j++) {
			if (! ((y + j - 1) in _canvas[x])) {
				return 0
			}
			if ("" _canvas[x + i - 1][y + j - 1] != ".") {
				if ("" shape_matrix[i][j] != ".") {
					return 0
				}
			}
		}
	}
	return 1
}

function compute_edges(pack, edges, _width, i, j, k)
{
	for (i = 1; i <= length(pack); i++) {
		for (j = length(pack[i]); 1 <= j; j--) {
			if (j == 1 && "" pack[i][j] == ".") {
				edges[i][j] = 1
			}
			if ("" pack[i][j] == ".") {
				for (k = j; max(1, j - _width) <= k; k--) {
					if ("" pack[i][k] != ".") {
						edges[i][j] = 1
					}
				}
			}
		}
	}
}

function copy_array(input, output, i)
{
	split("", output, FS)
	for (i = 1; i <= length(input); i++) {
		output[i] = input[i]
	}
}

function copy_matrix(input, output, i, j)
{
	split("", output, FS)
	for (i = 1; i <= length(input); i++) {
		for (j = 1; j <= length(input[1]); j++) {
			output[i][j] = input[i][j]
		}
	}
}

function desired_completed(desired, d)
{
	for (d in desired) {
		if (desired[d] > 0) {
			return 0
		}
	}
	return 1
}

function flip(input, output, i, j)
{
	make_canvas(length(input[1]), length(input), output)
	output[1][1] = input[1][3]
	output[1][2] = input[1][2]
	output[1][3] = input[1][1]
	output[2][1] = input[2][3]
	output[2][2] = input[2][2]
	output[2][3] = input[2][1]
	output[3][1] = input[3][3]
	output[3][2] = input[3][2]
	output[3][3] = input[3][1]
}

function get_letter()
{
	symbols = "abcdefghijklmnopqrstuvwzyz123456789"
	# print input_num, length(symbols), input_num % length(symbols)
	return substr(symbols, 1 + int((length(symbols) - 1) * rand()), 1)
}

function insert_shape(_canvas, x, y, _shape, insert_into, letter, i, j)
{
	letter = get_letter()
	insert_into[1][1] = 0	# Force as matrix
	copy_matrix(_canvas, insert_into)
	for (i = 1; i <= 3; i++) {
		for (j = 1; j <= 3; j++) {
			if (_shape[i][j] != ".") {
				insert_into[x + i - 1][y + j - 1] = letter
			}
		}
	}
}

function is_packable(canvases1, desired1, limit, canvases2, desired2, added, i, j, p, idx, edges, assessments, k)
{
	print "Calls:", ++calls
	for (i = 1; i <= length(desired1); i++) {
		if (desired_completed(desired1[i])) {
			print_matrix(canvases1[i])
			return 1
		}
	}
	added = 0
	idx = 1
	split("", canvases2, FS)
	split("", desired2, FS)
	split("", assessments, FS)
	for (p in canvases1) {
		split("", edges, FS)
		compute_edges(canvases1[p], edges, 1)
		for (i in edges) {
			for (j in edges[i]) {
				for (d in desired1[p]) {
					if (1 <= desired1[p][d] + 0) {
						for (s in GALLERY[d]) {
							if (can_insert(canvases1[p], i, j, GALLERY[d][s])) {
								added++
								split("", tmp, FS)
								insert_shape(canvases1[p], i, j, GALLERY[d][s], tmp)
								limited_insert(assessments, i SUBSEP j SUBSEP d SUBSEP s, assess_canvas(tmp), limit)
							}
						}
					}
				}
			}
		}
	}
	print "Number assessments:", length(assessments)
	for (i in assessments) {
		for (j in assessments[i]) {
			split(j, k, SUBSEP)
			desired2[idx][0] = -1
			copy_array(desired1[p], desired2[idx])
			desired2[idx][k[3]]--
			canvases2[idx][0][0] = -1
			insert_shape(canvases1[p], k[1], k[2], GALLERY[k[3]][k[4]], canvases2[idx])
			idx++
		}
	}
	if (added < 1) {
		return 0
	}
	return is_packable(canvases2, desired2, limit)
}

function limited_insert(array, key, value, limit, tmp, pos, k, kk)
{
	if (length(array) == 0) {
		array[1][key] = value
		return
	}
	pos = -1
	for (k = length(array); 1 <= k; k--) {
		for (kk in array[k]) {
			if (value < array[k][kk]) {
				pos = k
			}
		}
	}
	if (pos == -1) {
		return
	}
	for (k = min(limit, length(array) + 1); pos + 1 <= k; k--) {
		array[k][0] = 0
		split("", array[k], FS)
		for (kk in array[k - 1]) {
			array[k][kk] = array[k - 1][kk]
		}
	}
	array[pos][key] = value
}

function make_canvas(_width, _length, region_matrix, i, j)
{
	split("", region_matrix, FS)
	for (i = 1; i <= _length; i++) {
		for (j = 1; j <= _width; j++) {
			region_matrix[i][j] = "."
		}
	}
}

function matrixtostring(input_matrix, output, i, j)
{
	output = ""
	for (i = 1; i <= length(input_matrix); i++) {
		for (j = 1; j <= length(input_matrix[1]); j++) {
			output = output input_matrix[i][j]
		}
	}
	return output
}

function max(a, b)
{
	return (a < b ? b : a)
}

function min(a, b)
{
	return (a < b ? a : b)
}

function print_array(input_arr, i, first)
{
	first = 1
	for (i in input_arr) {
		if (first) {
			printf "%s", input_arr[i]
			first = 0
		} else {
			printf " %s", input_arr[i]
		}
	}
	print ""
}

function print_matrix(matrix, _i, _j)
{
	for (_i = 1; _i <= length(matrix); _i++) {
		for (_j = 1; _j <= length(matrix[1]); _j++) {
			printf matrix[_i][_j]
		}
		print ""
	}
}

function rotate(input, output, i, j)
{
	make_canvas(length(input[1]), length(input), output)
	output[1][1] = input[1][3]
	output[1][2] = input[2][3]
	output[1][3] = input[3][3]
	output[2][1] = input[1][2]
	output[2][2] = input[2][2]
	output[2][3] = input[3][2]
	output[3][1] = input[1][1]
	output[3][2] = input[2][1]
	output[3][3] = input[3][1]
}

function sum_abs_sorted(a, n, i, prefix, sum)
{
	prefix = 0
	sum = 0
	for (i = 1; i <= n; i++) {
		sum += (i - 1) * a[i] - prefix
		prefix += a[i]
	}
	return sum
}

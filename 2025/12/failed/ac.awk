BEGIN {
	FS = ""
	split("", SHAPES, FS)
	split("", GALLERY, FS)
	split("", OPTIMAL_PACKS, FS)
	split("", DISTRIBUTIONS, FS)
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
		desired[i - 2] = a[i]
	}
	split("", global_canvas, FS)
	global_canvas[1][1] = 0
	make_canvas(a[1], a[2], global_canvas)
	make_canvas(8, 8, global_canvas)
	calls = 0
	best = int(1e9)
	best_canvas[1][1] = "."
	is_possible = is_packable_dfs(global_canvas, desired)
	print_matrix(best_canvas)
	exit (0)
	NUM_POSSIBLE += is_possible
	print NR, ":", is_possible
}

END {
	print "Number possible:", NUM_POSSIBLE
}


function abs(a)
{
	return (0 <= a ? a : -a)
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
				x[n] = i + 0
				y[n] = j + 0
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

function desiredtostring(desired, output, i)
{
	output = ""
	for (i = 1; i <= length(desired); i++) {
		output = output desired[i] ","
	}
	return output
}

function determine_packings(packing_array, w, l, worst)
{
	# So obviously 3x3 is worst so ... we have to beat this
	worst = int(w / 3) * int(l / 3)
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

function gen(num_keys, pos, to_distribute, remaining, i, key, idx)
{
	if (remaining == -1) {
		remaining = to_distribute
	}
	if (pos == num_keys) {
		assign[pos] = remaining
		idx = to_distribute in DISTRIBUTIONS ? length(DISTRIBUTIONS[to_distribute]) + 1 : 1
		for (i = 1; i <= num_keys; i++) {
			DISTRIBUTIONS[to_distribute][idx][i] = assign[i]
		}
		return
	}
	for (i = 0; i <= remaining; i++) {
		assign[pos] = i
		gen(num_keys, pos + 1, to_distribute, remaining - i)
	}
}

function get_letter()
{
	symbols = "abcdefghijklmnopqrstuvwzyz123456789"
	# print input_num, length(symbols), input_num % length(symbols)
	return substr(symbols, 1 + int((length(symbols) - 1) * rand()), 1)
}

function insert_shape_inplace(pack, r, c, shape, undo, letter, _i, _j, rr, cc)
{
	letter = get_letter()
	# Record only the cells we actually modify (shape cell == 1).
	for (_i = 1; _i <= 3; _i++) {
		rr = r + _i - 1
		for (_j = 1; _j <= 3; _j++) {
			if ("" shape[_i][_j] != ".") {
				cc = c + _j - 1
				pack[rr][cc] = letter
				undo[rr][cc] = 1
			}
		}
	}
}

function is_packable_dfs(canvas, desired_presents, i, j, d, s, edges, undo, oldv, tmp, tmp2, assessments, t)
{
	if (++calls % 1000 == 1) {
		print("Row:", NR) > "/dev/stderr"
		printf("calls %d: rem: %d\n", ++calls, sum_array(desired_presents)) > "/dev/stderr"
	}
	if (desired_completed(desired_presents)) {
		print_matrix(canvas)
		return 1
	}
	# DFS: try to extend each state one move at a time
	# compute edges for this one state's pack matrix
	split("", edges, FS)
	compute_edges(canvas, edges, 1)
	split("", assessments, FS)
	for (i in edges) {
		for (j in edges[i]) {
			for (d in desired_presents) {
				if (1 <= desired_presents[d]) {
					for (s in GALLERY[d]) {
						if (can_insert(canvas, i, j, GALLERY[d][s])) {
							split("", tmp, FS)
							split("", tmp2, FS)
							copy_matrix(canvas, tmp)
							insert_shape_inplace(tmp, i, j, GALLERY[d][s], tmp2)
							assessments[i, j, d, s] = assess_canvas(tmp)
						}
					}
				}
			}
		}
	}
	split("", tmp2, FS) 
	for (i = 1; i <= asorti(assessments, tmp2, "@val_num_asc"); i++) {
		split(tmp2[i], tmp, SUBSEP)
		oldv = desired_presents[tmp[3]]
		desired_presents[tmp[3]]--
		split("", undo, FS)
		insert_shape_inplace(canvas, tmp[1], tmp[2], GALLERY[tmp[3]][tmp[4]], undo)
		t = sum_array(desired_presents)
 		if (t < best) {
			best = t
			copy_matrix(canvas, best_canvas)
			print "Best:", best
		}
		if (is_packable_dfs(canvas, desired_presents)) {
			return 1
		}
		remove_shape_inplace(canvas, undo)
		desired_presents[tmp[3]] = oldv
	}
	return 0
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

function remove_shape_inplace(pack, undo, i, j)
{
	for (i in undo) {
		for (j in undo[i]) {
			pack[i][j] = "."
		}
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

function sum_array(input_arr, out, i)
{
	out = 0
	for (i in input_arr) {
		out += input_arr[i]
	}
	return out
}

BEGIN {
	FS = ""
	split("", shapes, FS)
	split("", gallery, FS)
	split("", optimal_packs, FS)
	row_idx = 1
	pres_idx = 1
	num_possible = 0
}

/#|\./ {
	shapes[pres_idx][row_idx][1] = $1 == "#" ? 1 : 0
	shapes[pres_idx][row_idx][2] = $2 == "#" ? 1 : 0
	shapes[pres_idx][row_idx][3] = $3 == "#" ? 1 : 0
	row_idx++
	if (3 < row_idx) {
		add_to_gallery(pres_idx)
		pres_idx++
		row_idx = 1
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
	split("", global_canvases1, FS)
	global_canvases1[1][1][1] = 0
	make_canvas(a[1], a[2], global_canvases1[1])
	calls = 0
	is_possible = is_packable_dfs(global_canvases1, desired)
	num_possible += is_possible
	print NR, ":", is_possible
}

END {
	print "Number possible:", num_possible
}


function add_to_gallery(present_index, idx, rep)
{
	#############
	# rotations #
	#############
	split("", rot1, FS)
	split("", rot2, FS)
	split("", rot3, FS)
	rotate(shapes[present_index], rot1)
	rotate(rot1, rot2)
	rotate(rot2, rot3)
	# flip
	split("", flipped, FS)
	flip(shapes[present_index], flipped)
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
	# force awk to treat gallery as a minimum 3 dimension array #
	#############################################################
	for (idx = 1; idx <= 8; idx++) {
		gallery[present_index][idx][-1] = -1
	}
	##################
	# add to gallery #
	##################
	idx = 1
	split("", deduplicator, FS)
	copy_matrix(shapes[present_index], gallery[present_index][idx])
	deduplicator[matrixtostring(shapes[present_index])] = 1
	idx++
	rep = matrixtostring(rot1)
	if (! (rep in deduplicator)) {
		copy_matrix(rot1, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(rot2)
	if (! (rep in deduplicator)) {
		copy_matrix(rot2, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(rot3)
	if (! (rep in deduplicator)) {
		copy_matrix(rot3, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(flipped)
	if (! (rep in deduplicator)) {
		copy_matrix(flipped, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot1)
	if (! (rep in deduplicator)) {
		copy_matrix(frot1, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot2)
	if (! (rep in deduplicator)) {
		copy_matrix(frot2, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	rep = matrixtostring(frot3)
	if (! (rep in deduplicator)) {
		copy_matrix(frot3, gallery[present_index][idx])
		deduplicator[rep] = 1
		idx++
	}
	for (idx = 1; idx <= 8; idx++) {
		delete gallery[present_index][idx][-1]
		if (length(gallery[present_index][idx]) == 0) {
			delete gallery[present_index][idx]
		}
	}
}

function can_insert(_canvas, x, y, shape_matrix, i, j)
{
	for (i = 1; i <= 3; i++) {
		for (j = 1; j <= 3; j++) {
			if (! ((x + i - 1) in _canvas)) {
				return 0
			}
			if (! ((y + j - 1) in _canvas[x])) {
				return 0
			}
			if (1 < _canvas[x + i - 1][y + j - 1] + shape_matrix[i][j]) {
				return 0
			}
		}
	}
	return 1
}

function compute_edges(pack, edges, _width, i, j, k)
{
	for (i = 1; i <= length(pack); i++) {
		for (j = 1; j <= length(pack[i]) - _width; j++) {
			if (j == 1 && pack[i][j] == 0) {
				edges[i][j] = 1
			}
			if (pack[i][j] == 1) {
				for (k = 1; k <= _width; k++) {
					if (pack[i][j + k] == 0) {
						edges[i][j + k] = 1
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

function insert_shape_inplace(pack, r, c, shape, undo, _i, _j)
{
	for (_i = 1; _i <= length(shape); _i++) {
		for (_j = 1; _j <= length(shape[_i]); _j++) {
			pack[r + _i - 1][c + _j - 1] += shape[_i][_j]
			undo[r + _i - 1][c + _j - 1] = shape[_i][_j]
		}
	}
}

function is_packable_dfs(packs1, desired_inputs_arrays1, p, i, j, d, s, completed, edges, undo, oldv)
{
	if (++calls % 10000 == 1) {
		print "Row:", NR
		print "Calls:", calls
	}
	for (p in packs1) {
		if (desired_completed(desired_inputs_arrays1[p])) {
			return 1
		}
	}
	# DFS: try to extend each state one move at a time
	for (p in packs1) {
		# compute edges for this one state's pack matrix
		split("", edges, FS)
		# print_matrix(packs1[p])
		compute_edges(packs1[p], edges, 2)
		for (i in edges) {
			for (j in edges[i]) {
				# try each desired shape type d
				for (d in desired_inputs_arrays1[p]) {
					if (desired_inputs_arrays1[p][d] < 1) {
						continue
						# try each shape variant s in that gallery bucket
					}
					for (s in gallery[d]) {
						if (! can_insert(packs1[p], i, j, gallery[d][s])) {
							continue
						}
						oldv = desired_inputs_arrays1[p][d]
						desired_inputs_arrays1[p][d]--
						split("", undo, FS)
						# --- Apply move in-place ---
						insert_shape_inplace(packs1[p], i, j, gallery[d][s], undo)
						# --- Recurse depth-first ---
						if (is_packable_dfs(packs1, desired_inputs_arrays1)) {
							return 1
						}
						# --- Backtrack / undo ---
						remove_shape_inplace(packs1[p], undo)
						desired_inputs_arrays1[p][d] = oldv
					}
				}
			}
		}
	}
	return 0
}

function make_canvas(_width, _length, region_matrix, i, j)
{
	split("", region_matrix, FS)
	for (i = 1; i <= _length; i++) {
		for (j = 1; j <= _width; j++) {
			region_matrix[i][j] = 0
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

function remove_shape_inplace(pack, undo, k, _i, _j)
{
	for (_i in undo) {
		for (_j in undo[_i]) {
			pack[_i][_j] -= undo[_i][_j]
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

function sum_array(input_arr, output, i)
{
	output = 0
	for (i in input_arr) {
		output += input_arr[i]
	}
	return output
}

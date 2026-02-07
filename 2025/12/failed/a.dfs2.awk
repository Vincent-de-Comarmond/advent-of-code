BEGIN {
	FS = ""
	split("", shapes, FS)
	split("", gallery, FS)
	split("", optimal_packs, FS)
	row_idx = 1
	pres_idx = 1
	num_possible = 0
	DEBUG = 1
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

NR == 31 && /x/ {
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
	CANVAS_W = a[1]
	CANVAS_H = a[2]
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

function can_insert(_canvas, x, y, shape_matrix, i, j, xx, yy)
{
	for (i = 1; i <= 3; i++) {
		xx = x + i - 1
		if (xx < 1 || xx > CANVAS_H) {
			return 0
		}
		for (j = 1; j <= 3; j++) {
			yy = y + j - 1
			if (yy < 1 || yy > CANVAS_W) {
				return 0
			}
			if (1 < _canvas[xx][yy] + shape_matrix[i][j]) {
				return 0
			}
		}
	}
	return 1
}

function compute_edges(pack, edges, _width, i, j, k)
{
	for (i = 1; i <= length(pack); i++) {
		for (j = length(pack[i]); 1 <= j; j--) {
			if (j == 1 && pack[i][j] == 0) {
				edges[i][j] = 1
			}
			if (pack[i][j] == 0) {
				for (k = j; max(1, j - _width) <= k; k--) {
					if (pack[i][j] == 0 && pack[i][k] == 1) {
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

function insert_shape_inplace(pack, r, c, shape, undo_r, undo_c, _i, _j, rr, cc, n)
{
	# Record only the cells we actually modify (shape cell == 1).
	n = 0
	for (_i = 1; _i <= 3; _i++) {
		rr = r + _i - 1
		for (_j = 1; _j <= 3; _j++) {
			if (shape[_i][_j]) {
				cc = c + _j - 1
				pack[rr][cc]++
				undo_r[++n] = rr
				undo_c[n] = cc
			}
		}
	}
	return n
}

function is_packable_dfs(packs1, desired_inputs_arrays1, p, i, j, d, s, completed, edges, undo_r, undo_c, undo_n, oldv, a, b, c, e, n, branches, branch_num)
{
	calls++
	if (DEBUG && (calls % 100000 == 1)) {
		print("Row:", NR) > "/dev/stderr"
		printf("calls %d: rem: %d\n", calls, sum_array(desired_inputs_arrays1[1])) > "/dev/stderr"
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
		compute_edges(packs1[p], edges, 1)
		split("", branch_num, FS)
		split("", branches, FS)
		for (i in edges) {
			for (j in edges[i]) {
				for (d in desired_inputs_arrays1[p]) {
					if (1 <= desired_inputs_arrays1[p][d]) {
						for (s in gallery[d]) {
							if (can_insert(packs1[p], i, j, gallery[d][s])) {
								branch_num[i, j]++
								branches[i, j][d, s] = 1
							}
						}
					}
				}
			}
		}
		n = asorti(branch_num, a, "@val_num_asc")
		for (i = 1; i <= n; i++) {
			for (b in branches[a[i]]) {
				split(a[i], c, SUBSEP)
				split(b, e, SUBSEP)
				oldv = desired_inputs_arrays1[p][e[1]]
				desired_inputs_arrays1[p][e[1]]--
				# --- Apply move in-place ---
				undo_n = insert_shape_inplace(packs1[p], c[1], c[2], gallery[e[1]][e[2]], undo_r, undo_c)
				# --- Recurse depth-first ---
				if (is_packable_dfs(packs1, desired_inputs_arrays1)) {
					return 1
				}
				# --- Backtrack / undo ---
				remove_shape_inplace(packs1[p], undo_r, undo_c, undo_n)
				desired_inputs_arrays1[p][e[1]] = oldv
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

function remove_shape_inplace(pack, undo_r, undo_c, n, k)
{
	for (k = 1; k <= n; k++) {
		pack[undo_r[k]][undo_c[k]]--
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

function sum_array(input_arr, out, i)
{
	out = 0
	for (i in input_arr) {
		out += input_arr[i]
	}
	return out
}

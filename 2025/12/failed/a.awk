BEGIN {
	FS = ""
	split("", shapes, FS)
	split("", gallery, FS)
	split("", optimal_packs, FS)
	row_idx = 1
	pres_idx = 1
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
	split("", global_canvases2, FS)
	split("", desired2, FS)
	global_canvases1[1][1][1] = 0
	make_canvas(a[1], a[2], global_canvases1[1])
	# print_matrix(global_canvases1[1])
	is_packable(global_canvases1, global_canvases2, desired, desired2)
	# exit (0)
}

END {
	# for (i in gallery) {
	# 	for (j in gallery[i]) {
	# 		printf "Basis: %d, %d\n", i, j
	# 		print_matrix(gallery[i][j])
	# 		print ""
	# 	}
	# }
	# for (i = 1; i <= length(gallery); i++) {
	# 	for (j = 1; j <= length(gallery[i]); j++) {
	# 		if (j == 1) {
	# 			print "#####\nBASIS\n#####"
	# 		}
	# 		print i, j
	# 		print_matrix(gallery[i][j])
	# 		print ""
	# 	}
	# }
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
	# for (i in _canvas) {
	# 	for (j in _canvas[i]) {
	# 		printf "%d, %d: %d\n", i, j, _canvas[i][j]
	# 	}
	# }
	for (i = x; i <= x + 2; i++) {
		for (j = y; j <= y + 2; j++) {
			if (! (i in _canvas)) {
				# printf "i (%d, %d) not in canvas\n", i, j
				return 0
			}
			if (! (j in _canvas[i])) {
				# printf "j (%d, %d) not in canvas\n", i, j
				return 0
			}
			if (1 < _canvas[i][j] + shape_matrix[i + 1 - x][j + 1 - y]) {
				# printf "Overlap at %d, %d\n", i, j
				return 0
			}
		}
	}
	return 1
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

function insert_shape(global_canvas, x, y, shape_matrix, insert_into, insert_idx, a, b)
{
	insert_into[insert_idx][1][1] = 0	# Force as matrix
	for (a = 1; a <= length(global_canvas); a++) {
		for (b = 1; b <= length(global_canvas[a]); b++) {
			if (x <= a && a <= x + 2 && y <= b && b <= b + 2) {
				insert_into[insert_idx][a][b] = global_canvas[a][b] + shape_matrix[a + 1 - x][b + 1 - y]
			} else {
				insert_into[insert_idx][a][b] = global_canvas[a][b]
			}
		}
	}
}

function is_packable(packs1, packs2, desired_inputs_arrays1, desired_inputs_arrays2,
		     p, i, j, d, s, idx, added, completed)
{
	print "Line:", NR
	print "Calls:", ++calls
	print "Search space:", length(packs1)
	completed = 1
	for (d in desired_inputs_arrays1) {
		for (s in desired_inputs_arrays1[d]) {
			if (0 < desired_inputs_arrays1[d][s]) {
				completed = 0
				break
			}
		}
	}
	if (completed) {
		return 1
	}
	added = 0
	idx = 1
	split("", packs2, FS)
	split("", desired_inputs_arrays2, FS)
	split("", edges, FS)
	for (p in packs1) {
		for (i = 1; i <= length(packs1[p]); i++) {
			for (j = 1; j <= length(packs1[p][i]) - 2; j++) {
				if (j == 1 && packs1[p][i][j] == 0) {
					edges[p][i][j] = 1
				}
				if (packs1[p][i][j] == 1 && packs1[p][i][j + 1] == 0) {
					edges[p][i][j + 1] = 1
				}
				if (packs1[p][i][j] == 1 && packs1[p][i][j + 2] == 0) {
					edges[p][i][j + 2] = 1
				}
			}
		}
	}
	split("", ave_fill, FS)
	for (p in packs1) {
		if (0 < length(packs1[p])) {
			for (i = 1; i <= length(packs1[p]); i++) {
				for (j = 1; j <= length(packs1[p][i]); j++) {
					ave_fill[p] += packs1[p][i][j]
				}
			}
			ave_fill[p] = ave_fill[p] / (length(packs1[p]) * length(packs1[p][1]))
		}
	}
	a2 = 0
	for (p in ave_fill) {
		a2 += ave_fill[p]
	}
	print "Average fill:" (a2 / length(ave_fill))
	for (p in packs1) {
		# print_matrix(packs1[p])
		for (i in edges[p]) {
			for (j in edges[p][i]) {
				for (d in desired_inputs_arrays1[p]) {
					if (desired_inputs_arrays1[p][d] < 1) {
						continue
					}
					for (s in gallery[d]) {
						if (can_insert(packs1[p], i, j, gallery[d][s])) {
							desired_inputs_arrays2[idx][1] = 0
							copy_array(desired_inputs_arrays1[p], desired_inputs_arrays2[idx])
							desired_inputs_arrays2[idx][d]--
							added++
							insert_shape(packs1[p], i, j, gallery[d][s], packs2, idx)
							idx++
						}
					}
				}
			}
		}
	}
	if (added < 1) {
		return 0
	}
	# print "##############################"
	# for (i in packs2) {
	# 	print_matrix(packs2[i])
	# 	print "##############################"
	# }
	return is_packable(packs2, packs1, desired_inputs_arrays2, desired_inputs_arrays1)
}

function is_packable_dfs(packs1, packs2, desired_inputs_arrays1, desired_inputs_arrays2, p, i, j, d, s, idx, added, completed)
{
	print "Line:", NR
	print "Calls:", ++calls
	print "Search space:", length(packs1)
	completed = 1
	for (d in desired_inputs_arrays1) {
		for (s in desired_inputs_arrays1[d]) {
			if (0 < desired_inputs_arrays1[d][s]) {
				completed = 0
				break
			}
		}
	}
	if (completed) {
		return 1
	}
	added = 0
	idx = 1
	split("", packs2, FS)
	split("", desired_inputs_arrays2, FS)
	split("", edges, FS)
	for (p in packs1) {
		for (i = 1; i <= length(packs1[p]); i++) {
			for (j = 1; j <= length(packs1[p][i]) - 2; j++) {
				if (j == 1 && packs1[p][i][j] == 0) {
					edges[p][i][j] = 1
				}
				if (packs1[p][i][j] == 1 && packs1[p][i][j + 1] == 0) {
					edges[p][i][j + 1] = 1
				}
				if (packs1[p][i][j] == 1 && packs1[p][i][j + 2] == 0) {
					edges[p][i][j + 2] = 1
				}
			}
		}
	}
	for (p in packs1) {
		# print_matrix(packs1[p])
		for (i in edges[p]) {
			for (j in edges[p][i]) {
				for (d in desired_inputs_arrays1[p]) {
					if (desired_inputs_arrays1[p][d] < 1) {
						continue
					}
					for (s in gallery[d]) {
						if (can_insert(packs1[p], i, j, gallery[d][s])) {
							desired_inputs_arrays2[idx][1] = 0
							copy_array(desired_inputs_arrays1[p], desired_inputs_arrays2[idx])
							desired_inputs_arrays2[idx][d]--
							added++
							insert_shape(packs1[p], i, j, gallery[d][s], packs2, idx)
							idx++
						}
					}
				}
			}
		}
	}
	if (added < 1) {
		return 0
	}
	# print "##############################"
	# for (i in packs2) {
	# 	print_matrix(packs2[i])
	# 	print "##############################"
	# }
	return is_packable_dfs(packs2, packs1, desired_inputs_arrays2, desired_inputs_arrays1)
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

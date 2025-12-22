END {
	# TESTING
	if (0) {
		# matrix1[0][0] = 1
		# matrix1[0][1] = 1
		# matrix1[0][2] = 1
		# matrix1[1][0] = 1
		# matrix1[1][1] = 2
		# matrix1[1][2] = 3
		print "A:"
		print_matrix(matrix1)
		#
		matrix2[0][0] = 8
		matrix2[1][0] = -1
		print "b:"
		print_matrix(matrix2)
		#
		split("", aug, FS)
		hconcat(matrix1, matrix2, aug)
		split("", rref, FS)
		to_rref(aug, rref)
		print "system"
		print_matrix(rref)
	}
}


function copy_matrix(input_matrix, output_matrix, i, j)
{
	split("", output_matrix, FS)
	for (i = 0; i < length(input_matrix); i++) {
		for (j = 0; j < length(input_matrix[0]); j++) {
			output_matrix[i][j] = input_matrix[i][j]
		}
	}
}

function hconcat(matrix1, matrix2, output, i, j)
{
	split("", output, FS)
	if (length(matrix1) != length(matrix2)) {
		printf("Incompatable matrix sizes %d and %d\n", length(matrix1), length(matrix2)) > "/dev/stderr"
	}
	for (i = 0; i < length(matrix1); i++) {
		for (j = 0; j < length(matrix1[0]) + length(matrix2[0]); j++) {
			if (j < length(matrix1[0])) {
				output[i][j] = matrix1[i][j]
			} else {
				output[i][j] = matrix2[i][j - length(matrix1[0])]
			}
		}
	}
}

function mmult(matrix1, matrix2, output_matrix, a, b, c, i, j, k)
{
	a = length(matrix1)
	b = length(matrix1[0])
	c = length(matrix2[0])
	if (length(matrix2) != b) {
		print "Incompatablie matrix multiplication"
		exit 1
	}
	split("", output_matrix, "")
	for (i = 0; i < a; i++) {
		for (j = 0; j < c; j++) {
			for (k = 0; k < b; k++) {
				output_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
			}
		}
	}
}

function normalize_row(input_matrix, idx, j, factor)
{
	factor = 0
	for (j = 0; j < length(input_matrix[idx]); j++) {
		if ((input_matrix[idx][j] + 0 != 0) && (factor == 0)) {
			factor = 1.0 / (input_matrix[idx][j] + 0.0)
		}
		input_matrix[idx][j] *= factor
	}
	return factor
}

function print_matrix(input_matrix, i, j)
{
	for (i = 0; i < length(input_matrix); i++) {
		for (j = 0; j < length(input_matrix[0]); j++) {
			printf j == 0 ? "% 2.3f" : ", % 2.3f", input_matrix[i][j]
		}
		print ""
	}
}

function reduce_down(input_matrix, idx, i, j, factor)
{
	for (i = idx + 1; i < length(input_matrix); i++) {
		if (input_matrix[i][idx] + 0 == 0) {
			continue
		}
		factor = input_matrix[i][idx] / input_matrix[idx][idx]
		for (j = 0; j < length(input_matrix[0]); j++) {
			input_matrix[i][j] -= factor * input_matrix[idx][j]
		}
	}
}

function remove_null_information(input_matrix, output_matrix, i, j, unseen, all_null)
{
	split("", tmp, FS)
	for (i = 0; i < length(input_matrix); i++) {
		for (j = 0; j < length(input_matrix[0]); j++) {
			tmp[i] = j == 0 ? input_matrix[i][0] : tmp[i] SUBSEP input_matrix[i][j]
		}
	}
	split("", tmp12, FS)
	for (i = 0; i < length(tmp); i++) {
		unseen = 1
		for (j = 0; j < i; j++) {
			if (tmp[i] == tmp[j]) {
				unseen = 0
				break
			}
		}
		if (unseen) {
			idx = length(tmp12)
			for (j = 0; j < length(input_matrix[0]); j++) {
				tmp12[idx][j] = input_matrix[i][j]
			}
		}
	}
	split("", output_matrix, FS)
	for (i = 0; i < length(tmp12); i++) {
		idx = length(output_matrix)
		all_null = 1
		for (j = 0; j < length(tmp12[0]); j++) {
			if (tmp12[i][j] != 0) {
				all_null = 0
				break
			}
		}
		if (all_null) {
			continue
		}
		for (j = 0; j < length(tmp12[0]); j++) {
			output_matrix[idx][j] = tmp2[i][j]
		}
	}
}

function swap(input_matrix, idx1, idx2, j)
{
	split("", tmp, "")
	for (j = 0; j < length(input_matrix[idx1]); j++) {
		tmp[0][j] = input_matrix[idx1][j]
		tmp[1][j] = input_matrix[idx2][j]
	}
	for (j = 0; j < length(tmp[0]); j++) {
		input_matrix[idx1][j] = tmp[1][j]
		input_matrix[idx2][j] = tmp[0][j]
	}
}

function take_column(matrix_in, idx, vec_out, i)
{
	split("", vec_out, FS)
	for (i = 0; i < length(matrix_in); i++) {
		vec_out[i][0] = matrix_in[i][idx]
	}
}

function to_rref(augmented_in, augmented_out, pivots, nrows, ncols, i, j, k)
{
	nrows = length(augmented_in)
	copy_matrix(augmented_in, augmented_out)
	# "Reduce down"
	for (i = 0; i < nrows; i++) {
		if (augmented_out[i][i] + 0 == 0) {
			for (j = i + 1; j < nrows; j++) {
				if (augmented_out[j][i] + 0 != 0) {
					swap(augmented_out, j, i)
					break
				}
			}
		}
		reduce_down(augmented_out, i)
	}
	# "Normalize"
	for (i = 0; i < nrows; i++) {
		factor = normalize_row(augmented_out, i)
	}
	ncols = length(augmented_out[0])
	# Already upper triangular
	split("", pivots, FS)
	for (i = 0; i < nrows; i++) {
		if (augmented_out[i][i] == 1) {
			pivots[i] = i
			continue
		}
		# -1 => don't pivot on solution column
		for (j = i + 1; j < ncols - 1; j++) {
			if (augmented_out[i][j] == 1) {
				pivots[j] = i
				break
			}
		}
	}
	# "Reduce up"
	for (i = 0; i < nrows; i++) {
		#Don't operate on solution column
		for (j = i + 1; j < ncols - 1; j++) {
			if (augmented_out[i][j] != 0 && j in pivots && i < pivots[j]) {
				factor = augmented_out[i][j]
				for (k = 0; k < ncols; k++) {
					augmented_out[i][k] -= factor * augmented_out[pivots[j]][k]
				}
			}
		}
	}
}

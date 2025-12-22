# END {
# 	split("", mat, "")
# 	# mat[0][0] = 1
# 	# mat[0][1] = 2
# 	# #
# 	# mat[1][0] = 2
# 	# mat[1][1] = 4
# 	# #
# 	# mat[2][0] = 3
# 	# mat[2][1] = 6
# 	mat[0][0] = 1
# 	mat[0][1] = 2
# 	mat[0][2] = 3
# 	#
# 	mat[1][0] = 4
# 	mat[1][1] = 2
# 	mat[1][2] = 1
# 	#
# 	mat[2][0] = 5
# 	mat[2][1] = 2
# 	mat[2][2] = 4
# 	#
# 	mat[3][0] = 1
# 	mat[3][1] = 8
# 	mat[3][2] = 9
# 	#
# 	print "Matrix"
# 	print_matrix(mat)
# 	print "Pseudo Inverse"
# 	split("", left_inv, FS)
# 	split("", right_inv, FS)
# 	pinv(mat, left_inv, right_inv)
# 	print "Left inverse"
# 	print_matrix(left_inv)
# 	print "Right inverse"
# 	print_matrix(right_inv)
# 	print "Checking"
# 	split("", tmp, FS)
# 	mmult(mat, left_inv, tmp)
# 	print_matrix(tmp)
# 	print "Checking 2"
# 	split("", tmp, FS)
# 	mmult(left_inv, mat, tmp)
# 	print_matrix(tmp)
# }

function inv(in_matrix, inverse, i, j, k, s, factor)
{
	split("", tmp, "")
	split("", inverse, "")
	r = length(in_matrix)
	c = length(in_matrix[0])
	for (i = 0; i < r; i++) {
		for (j = 0; j < c; j++) {
			tmp[i][j] = in_matrix[i][j]
			inverse[i][j] = i == j ? 1 : 0
		}
	}
	for (i = 0; i < r; i++) {
		if (tmp[i][i] + 0 == 0) {
			for (j = i + 1; j < r; j++) {
				if (tmp[j][i] + 0 != 0) {
					swap(tmp, j, i)
					swap(inverse, j, i)
					factor = 1.0 / (tmp[i][i] + 0.0)
					multiply_row(tmp, i, factor)
					multiply_row(inverse, i, factor)
					break
				}
			}
		}
		reduce_down(tmp, inverse, i)
	}
	# Case for skipped column
	for (i = 0; i < r; i++) {
		if (tmp[i][i] != 1) {
			for (j = i; j < c; j++) {
				if (tmp[i][j] != 0) {
					factor = 1.0 / (tmp[i][j] + 0.0)
					multiply_row(tmp, i, factor)
					multiply_row(inverse, i, factor)
					break
				}
			}
		}
	}
	for (i = 0; i < r; i++) {
		for (j = i + 1; j < c; j++) {
			if (tmp[i][j] == 0) {
				continue
			}
			factor = tmp[i][j]
			for (k = 0; k < c; k++) {
				tmp[i][k] -= factor * tmp[j][k]
				inverse[i][k] -= factor * inverse[j][k]
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

function multiply_row(matrix, idx, multiplier, j)
{
	for (j = 0; j < length(matrix[idx]); j++) {
		matrix[idx][j] *= multiplier
	}
}

function pinv(input_matrix, left_inverse, right_inverse)
{
	## Simplified here as we assume that we have linearly independant
	split("", transposed, FS)
	transpose(input_matrix, transposed)
	split("", transposed_mult_input, FS)
	split("", transposed_mult_input_inverted, FS)
	mmult(transposed, input_matrix, transposed_mult_input)
	inv(transposed_mult_input, transposed_mult_input_inverted)
	mmult(transposed_mult_input_inverted, transposed, left_inverse)
	split("", input_mult_transposed, FS)
	split("", input_mult_transposed_inverted, FS)
	mmult(input_matrix, transposed, input_mult_transposed)
	inv(input_mult_transposed, input_mult_transposed_inverted)
	mmult(transposed, input_mult_transposed_inverted, right_inverse)
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

function reduce_down(input_matrix, complement, idx, r, c, i, j, factor)
{
	r = length(input_matrix)
	c = length(input_matrix[0])
	for (i = idx + 1; i < r; i++) {
		if (input_matrix[i][idx] + 0 != 0) {
			factor = input_matrix[i][idx] / input_matrix[idx][idx]
			for (j = 0; j < c; j++) {
				input_matrix[i][j] -= factor * input_matrix[idx][j]
				if (isarray(complement)) {
					complement[i][j] -= factor * complement[idx][j]
				}
			}
		}
	}
}

function rref(input_matrix, output_matrix, r, c, i, j, factor)
{
	split("", output_matrix, "")
	r = length(input_matrix)
	c = length(input_matrix[0])
	for (i = 0; i < r; i++) {
		for (j = 0; j < c; j++) {
			output_matrix[i][j] = input_matrix[i][j]
		}
	}
	for (i = 0; i < r; i++) {
		if (output_matrix[i][i] + 0 == 0) {
			for (j = i + 1; j < r; j++) {
				if (output_matrix[j][i] + 0 != 0) {
					swap(output_matrix, j, i)
					factor = 1.0 / (output_matrix[i][i] + 0.0)
					multiply_row(output_matrix, i, factor)
					break
				}
			}
		}
		reduce_down(output_matrix, "", i)
	}
	# Case for skipped column
	for (i = 0; i < r; i++) {
		if (output_matrix[i][i] != 1) {
			for (j = i; j < c; j++) {
				if (output_matrix[i][j] != 0) {
					factor = 1.0 / (output_matrix[i][j] + 0.0)
					multiply_row(output_matrix, i, factor)
					break
				}
			}
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

function to_vector(string, output, i)
{
	split(string, tmp, SUBSEP)
	for (i = 1; i <= length(tmp); i++) {
		output[i - 1][0] = tmp[i]
	}
}

function transpose(input_matrix, output_matrix, m, n, i, j)
{
	m = length(input_matrix)
	n = length(input_matrix[0])
	split("", output_matrix, "")
	for (i = 0; i < m; i++) {
		for (j = 0; j < n; j++) {
			output_matrix[j][i] = input_matrix[i][j]
		}
	}
}

END {
	# TESTING
	if (0) {
		matrix1[0][0] = 1
		matrix1[0][1] = 1
		matrix1[0][2] = 1
		matrix1[1][0] = 1
		matrix1[1][1] = 2
		matrix1[1][2] = 3
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
		to_rref_int(aug, rref)
		print "system"
		print_matrix(rref)
	}
}


function abs(input)
{
	return (0 < input ? input : -input)
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

function gcd(a, b, rem)
{
	while (b + 0 != 0) {
		rem = a % b
		a = b
		b = rem
	}
	return a
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

function lcm(a, b)
{
	return (a * b / gcd(a, b))
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

function normalize_row(input_matrix, idx, j, factor, _gcd)
{
	split("", __tmp, FS)
	for (j = 0; j < length(input_matrix[idx]); j++) {
		if (input_matrix[idx][j] + 0 != 0) {
			__tmp[length(__tmp)] = input_matrix[idx][j]
		}
	}
	if (length(__tmp) == 0) {
		return
	}
	if (length(__tmp) == 1 && __tmp[0] + 0 == 1) {
		return
	}
	for (j = 0; j < length(__tmp); j++) {
		_gcd = (j == 0) ? abs(__tmp[0]) : gcd(_gcd, abs(__tmp[j]))
	}
	factor = __tmp[0] < 0 ? -1.0 / _gcd : 1.0 / _gcd
	for (j = 0; j < length(input_matrix[idx]); j++) {
		input_matrix[idx][j] *= factor
	}
	return factor
}

function print_matrix(input_matrix, _i, _j)
{
	for (_i = 0; _i < length(input_matrix); _i++) {
		for (_j = 0; _j < length(input_matrix[0]); _j++) {
			printf _j == 0 ? "% 2.3f" : ", % 2.3f", input_matrix[_i][_j]
		}
		print ""
	}
}

function reduce_down(input_matrix, idx, idx2, i, j, pval, factor, a, b)
{
	# print "Input - reducing below: ", idx
	# print_matrix(input_matrix)
	pval = 0
	for (j = idx; j < length(input_matrix[0]) - 1; j++) {
		if (0.02 < abs(input_matrix[idx][j])) {
			pval = input_matrix[idx][j]
			idx2 = j
			break
		}
	}
	if (pval == 0) {
		return
	}
	for (i = idx + 1; i < length(input_matrix); i++) {
		if (input_matrix[i][idx2] + 0 == 0) {
			continue
		}
		factor = lcm(abs(pval), abs(input_matrix[i][idx2]))
		a = factor / abs(input_matrix[i][idx2])
		b = factor / abs(pval)
		if ((pval < 0) != (input_matrix[i][idx2] < 0)) {
			b = -b
		}
		for (j = 0; j < length(input_matrix[0]); j++) {
			input_matrix[i][j] = a * input_matrix[i][j] - b * input_matrix[idx][j]
		}
	}
	# print "output - reducing below: ", idx
	# print_matrix(input_matrix)
}

function swap(input_matrix, idx1, idx2, j)
{
	# printf "Swapping %d <-> %d\n", idx1, idx2
	# print_matrix(input_matrix)
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

function to_rref_int(augmented_in, augmented_out, pivots, nrows, ncols, i, j, k, is_pivot, factor, pval, a, b, idx2)
{
	split("", augmented_out, FS)
	split("", pivots, FS)
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
	for (i = 0; i < nrows; i++) {
		normalize_row(augmented_out, i)
	}
	ncols = length(augmented_out[0])
	# Get pivots
	for (i = 0; i < nrows; i++) {
		is_pivot = 0
		for (j = 0; j < ncols - 1; j++) {
			if (augmented_out[i][j] + 0 != 0) {
				if (! is_pivot) {
					is_pivot = 1
					pivots[j] = i
					break
				}
			}
		}
	}
	# Reduce up
	for (i = nrows - 1; 0 <= i; i--) {
		idx2 = -1
		pval = 0
		for (j = 0; j < ncols - 1; j++) {
			if (augmented_out[i][j] != 0) {
				pval = augmented_out[i][j]
				idx2 = j
				break
			}
		}
		if (idx2 < 0) {
			continue
		}
		for (j = i - 1; 0 <= j; j--) {
			if (augmented_out[j][idx2] + 0 == 0) {
				continue
			}
			factor = lcm(abs(pval), abs(augmented_out[j][idx2]))
			a = factor / abs(augmented_out[j][idx2])
			b = factor / abs(pval)
			if ((pval < 0) != (augmented_out[j][idx2] < 0)) {
				b = -b
			}
			for (k = 0; k < ncols; k++) {
				augmented_out[j][k] = a * augmented_out[j][k] - b * augmented_out[i][k]
			}
		}
	}
	for (i = 0; i < nrows; i++) {
		normalize_row(augmented_out, i)
	}
}

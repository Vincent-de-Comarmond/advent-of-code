BEGIN {
    counter=1
	FPAT = "[0-9]+"
}

/Button A/ {
	X[0, 0] = $1
	X[1, 0] = $2
}

/Button B/ {
	X[0, 1] = $1
	X[1, 1] = $2
}

/Prize/ {
	Y[0] = $1 + 10000000000000
	Y[1] = $2 + 10000000000000
	det = determinant(X)
	if (! (almost_equal(det, 0, 10 ^ -9))) {
		inverse(X, invX)
		mmult(invX, Y, soln)
		isint[0] = almost_equal(soln[0], round(soln[0]), 10 ^ -3)
		isint[1] = almost_equal(soln[1], round(soln[1]), 10 ^ -3)
		if (isint[0] && isint[1]) {
		    cost += 3 * soln[0] + soln[1]
		    counter++
		}
	}
}

END {
	print cost
	# 95688837203288 is the right answer for part 2
}


function almost_equal(num1, num2, tolerance,        tmp) {
	tmp = (num1 >= num2) ? num1 - num2 : num2 - num1
	return (tmp <= tolerance)
}

function almost_int(num1,        tmp) {
	tmp = num1 % 1
	if (tmp >= 0) {
		return (tmp < 10 ^ -5)
	}
	return (-tmp < 10 ^ -5)
}

function determinant(input_matrix) {
	return (input_matrix[0, 0] * input_matrix[1, 1] - input_matrix[1, 0] * input_matrix[0, 1])
}

function inverse(input_matrix, output_matrix,        det) {
	det = determinant(input_matrix)
	output_matrix[0, 0] = input_matrix[1, 1] / det
	output_matrix[1, 0] = -input_matrix[1, 0] / det
	output_matrix[1, 1] = input_matrix[0, 0] / det
	output_matrix[0, 1] = -input_matrix[0, 1] / det
}

function mmult(input_matrix, input_vector, output_vector) {
	output_vector[0] = input_matrix[0, 0] * input_vector[0] + input_matrix[0, 1] * input_vector[1]
	output_vector[1] = input_matrix[1, 0] * input_vector[0] + input_matrix[1, 1] * input_vector[1]
}

function round(number) {
	return int(number + 0.5)
}

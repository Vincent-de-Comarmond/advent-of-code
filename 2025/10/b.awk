BEGIN {
	button_pushes = 0
	split("", choices, FS)
}

{
	# print "Row:", NR
	split("", aug, FS)
	split("", buttons, FS)
	split("", joltages, FS)
	split("", pivots, FS)
	split("", rref, FS)
	process_line(buttons, joltages)
	hconcat(buttons, joltages, aug)
	to_rref_int(aug, rref, pivots)
	t = solve(rref, pivots)
	button_pushes += t
	printf "\t%d: %.1f\n", NR, t
	# exit (0)
}

END {
	print "Minimal button pushes:", button_pushes
	# 20044 is too low ... WTF
	# 20045 is too low
	# 20083 is the right answer for part 2
}


function choose(n, c, i, j, new)
{
	if ((n, c) in choices) {
		return
	}
	if (c == 1) {
		for (i = 0; i < n; i++) {
			choices[n, c][i] = 1
		}
		return
	}
	choose(n, c - 1)
	split("", tmp, FS)
	for (i in choices[n, c - 1]) {
		for (j = 0; j < n; j++) {
			# Weird AWK regex
			if (i !~ ("\\<" j "\\>")) {
				tmp[length(tmp)] = sort_join(i, j)
			}
		}
	}
	choices[n, c][tmp[0]] = 1
	for (i = 1; i < length(tmp); i++) {
		if (! (tmp[i] in choices[n, c])) {
			choices[n, c][tmp[i]] = 1
		}
	}
}

function clean()
{
	gsub(/\(|\)/, "", $0)
	gsub(/{|}/, "", $0)
}

function make_search_space(upper_bound, dimensions, array, i, j)
{
	if (dimensions == 0) {
		return
	}
	if (dimensions == 1) {
		for (i = 0; i <= upper_bound; i++) {
			array[i] = 0
		}
		return
	}
	make_search_space(upper_bound, dimensions - 1, array)
	for (i in array) {
		for (j = 0; j <= upper_bound; j++) {
			array[i SUBSEP j] = 0
		}
		delete array[i]
	}
}

function process_line(rref_matrix, pivots)
{
	clean()
	split("", joltages, FS)
	read_joltages(joltages)
	#
	split("", buttons, "")
	read_buttons(buttons, length(joltages))
}

function read_buttons(buttons_matrix, num_machines)
{
	for (i = 2; i < NF; i++) {
		split($i, button, ",")
		for (j = 0; j < num_machines; j++) {
			buttons[j][i - 2] = 0
		}
		for (j = 1; j <= length(button); j++) {
			buttons[button[j]][i - 2] = 1
		}
	}
}

function read_joltages(target)
{
	split($NF, a, ",")
	for (i = 1; i <= length(a); i++) {
		target[i - 1][0] = a[i]
	}
}

function round(input)
{
	return (input >= 0) ? int(input + 0.5) : int(input - 0.5)
}

function solve(rref_matrix, pivots, nrow, ncol, i, j, m, best, subsol, val)
{
	best = int(1e9)
	nrow = length(rref_matrix)
	ncol = length(rref_matrix[0])
	split("", free, FS)
	for (i = 0; i < ncol - 1; i++) {
		if (! (i in pivots)) {
			free[length(free)] = i
		}
	}
	if (length(free) == 0) {
		best = 0
		for (j in pivots) {
			subsol = rref_matrix[pivots[j]][ncol - 1] / rref_matrix[pivots[j]][j]
			if (subsol < -0.05 || 0.05 < abs(subsol - round(subsol))) {
				print("Only 1 invalid solution found") > "/dev/stderr"
				exit (1)
			}
			best += subsol
		}
		return best
	}
	## Set up equations
	# We're going for 
	# print_matrix(rref_matrix)
	split("", divisor, FS)
	split("", constant, FS)
	split("", M, FS)
	for (i = 0; i < ncol - 1; i++) {
		if (i in pivots) {
			divisor[i][0] = rref_matrix[pivots[i]][i]
			constant[i][0] = rref_matrix[pivots[i]][ncol - 1]
			for (j = 0; j < length(free); j++) {
				M[i][j] = -rref_matrix[pivots[i]][free[j]]
			}
		} else {
			divisor[i][0] = 1
			constant[i][0] = 0
			for (j = 0; j < length(free); j++) {
				M[i][j] = (i == free[j]) ? 1 : 0
			}
		}
	}
	if (1) {
		####################
		# some brute force #
		####################
		m = -int(1e4)
		for (i = 0; i < length(constant); i++) {
			val = int(constant[i][0] / divisor[i][0]) + 1
			m = m + 0 < val ? val : m
		}
		split("", searchspace, FS)
		make_search_space(m, length(M[0]), searchspace)
		n = 0
		for (i in searchspace) {
			if (++n % 500000 == 0) {
				printf "\t\t%.2f %\n", 100.0 * n / length(searchspace)
			}
			subsol = 0
			split(i, a, SUBSEP)
			split("", u, FS)
			for (j = 1; j <= length(a); j++) {
				u[j - 1][0] = a[j]
			}
			split("", tmp, FS)
			mmult(M, u, tmp)
			for (j = 0; j < length(tmp); j++) {
				val = (constant[j][0] + tmp[j][0]) / divisor[j][0]
				if (val < -0.01 || 0.1 < abs(val - round(val))) {
					subsol = int(1e9)
					break
				}
				subsol += val
			}
			best = subsol < best ? subsol : best
		}
		return best
	}
	if (1) {
		#####################################
		# simplex (slightly fragile)        #
		#####################################
		## Check possibilities
		m = length(M)
		n = length(M[0])
		choose(m, n)
		best = int(1e9)
		for (i in choices[m, n]) {
			# Choose constraints to enforce
			split(i, a, SUBSEP)
			split("", aug, FS)
			for (j = 1; j <= length(a); j++) {
				for (k = 0; k < n; k++) {
					aug[j - 1][k] = -M[a[j]][k]
				}
				aug[j - 1][k] = constant[a[j]][0]
			}
			split("", vertex, FS)
			to_rref_int(aug, vertex, dummy)
			if (valid_soln(vertex)) {
				# print "Vertex"
				# print_matrix(vertex)
				take_column(vertex, n, dummy)
				split("", output, FS)
				mmult(M, dummy, output)
				subsol = 0
				for (j = 0; j < length(output); j++) {
					val = (constant[j][0] + output[j][0]) / divisor[j][0]
					if (val < -0.05 || 0.05 < abs(val - round(val))) {
						subsol = int(1e9)
						break
					}
					subsol += val
				}
				best = subsol < best ? subsol : best
			}
		}
		return best
	}
}

function sort_join(part1, part2)
{
	split(part1, alpha, SUBSEP)
	split(part2, beta, SUBSEP)
	if (alpha[1] + 0 <= beta[1] + 0) {
		return (part1 SUBSEP part2)
	}
	return (part2 SUBSEP part1)
}

function valid_soln(augmented_matrix, m, n, val)
{
	m = length(augmented_matrix)
	n = length(augmented_matrix[0])
	for (i = 0; i < m; i++) {
		for (j = 0; j < n; j++) {
			val = augmented_matrix[i][j]
			if (i == j && val + 0 == 0) {
				return 0
			}
			if (i != j) {
				if (j < n - 1 && val + 0 != 0) {
					return 0
				}
				if (j == n - 1 && val + 0 < 0) {
					return 0
				}
			}
		}
	}
	return 1
}

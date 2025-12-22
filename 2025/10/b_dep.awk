BEGIN {
	button_pushes = 0
	split("", choices, FS)
}

NR != 36 {
	next
}

{
	split("", buttons, FS)
	split("", joltages, FS)
	process_line(buttons, joltages)
	split("", rref, FS)
	split("", pivots, FS)
	reduce(buttons, joltages, rref, pivots)
	print "Buttons"
	print_matrix(buttons)
	print "Joltages"
	print_matrix(joltages)
	print "Reduced"
	print_matrix(rref)
	t = solve(rref, pivots)
	button_pushes += t
	printf "%d: %.2f\n", NR, t
}

END {
	print "Minimal button pushes:", button_pushes
	# 20044 is too low ... WTF
	# 20045 is too low
}


function abs(input)
{
	return (0 < input ? input : -input)
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

function reduce(buttons, joltages, rref, pivots)
{
	split("", aug, FS)
	hconcat(buttons, joltages, aug)
	split("", tmp2, FS)
	to_rref(aug, rref, pivots)
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
		split("", dummy, FS)
		take_column(rref_matrix, ncol - 1, dummy)
		subsol = 0
		for (j = 0; j < length(dummy); j++) {
			if (dummy[j][0] + 0 < -0.5) {
				print("Only 1 invalid solution found") > "/dev/stderr"
				exit (1)
			} else {
				subsol += dummy[j][0]
			}
		}
		return subsol
	}
	## Set up equations
	# We're going for 
	# print_matrix(rref_matrix)
	split("", constant, FS)
	split("", M, FS)
	for (i = 0; i < ncol - 1; i++) {
		if (i in pivots) {
			constant[i][0] = rref_matrix[pivots[i]][ncol - 1]
			for (j = 0; j < length(free); j++) {
				M[i][j] = -rref_matrix[pivots[i]][free[j]]
			}
		} else {
			constant[i][0] = 0
			for (j = 0; j < length(free); j++) {
				M[i][j] = (i == free[j]) ? 1 : 0
			}
		}
	}
	if (1) {
		#########################################
		# I'm tired of this now ...	        #
		# Gonna try a bit of brute force        #
		#########################################
		m = -int(1e4)
		for (i = 0; i < nrow - 1; i++) {
			m = m + 0 < rref_matrix[i][ncol - 1] ? rref_matrix[i][ncol - 1] : m
		}
		split("", searchspace, FS)
		make_search_space(m, length(M[0]), searchspace)
		n = 0
		for (i in searchspace) {
			if (++n % 100000 == 0) {
				printf "\t%.2f %\n", 100.0 * n / length(searchspace)
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
				val = constant[j][0] + tmp[j][0]
				if (val < -0.01 || 0.1 < abs(val - round(val))) {
					subsol = int(1e9)
					break
				}
				subsol += val
			}
			if (subsol < best) {
				print "Best:", subsol
				for (j = 0; j < length(tmp); j++) {
					print constant[j][0] + tmp[j][0]
				}
				best = subsol
			}
			# best = subsol < best ? subsol : best
		}
		return best
	}
	if (1) {
		#########################################
		# Attempt to manually implement simplex #
		#########################################
		#########################################################################
		# This works ... sadly I did not think about the			#
		# fact that all entries must be integer ... so that's a problem	#
		#########################################################################
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
			to_rref(aug, vertex, dummy)
			if (valid_soln(vertex)) {
				print "Vertex"
				print_matrix(vertex)
				take_column(vertex, n, dummy)
				split("", output, FS)
				mmult(M, dummy, output)
				subsol = 0
				print "\nVal"
				for (j = 0; j < length(output); j++) {
					val = constant[j][0] + output[j][0]
					if (val < -0.01) {
						subsol = int(1e9)
						break
					}
					# if (0.1 + 0 < abs(val - round(val)) + 0) {
					# 	subsol = int(1e9)
					# 	break
					# }
					subsol += val
				}
				if (subsol < best) {
					print "Best:", subsol
					for (j = 0; j < length(output); j++) {
						print constant[j][0], output[j][0], (constant[j][0] + output[j][0])
					}
					best = subsol
				}
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
			if (i == j && val + 0 != 1) {
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

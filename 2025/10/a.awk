BEGIN {
	total_button_pushes = 0
	split("", cache, "")
}

{
	# Load targets
	split($1, a, "")
	split("", target, "")
	for (i = 2; i < length(a); i++) {
		target[i - 2][0] = a[i] == "#" ? 1 : 0
	}
	# Load buttons (as column vectors of a matrix)
	split("", buttons, "")
	for (i = 2; i < NF; i++) {
		split(substr($i, 2, length($i) - 2), button, ",")
		for (j = 0; j < length(target); j++) {
			buttons[j][i - 2] = 0
		}
		for (j = 1; j <= length(button); j++) {
			buttons[button[j]][i - 2] = 1
		}
	}
	# Find minimal solution
	b = length(buttons[0])
	for (p = 1; p < 15; p++) {
		get_options(b, p)
		for (option in cache[b, p]) {
			split("", vec, FS)
			to_vector(cache[b, p][option], vec)
			split("", outcome, FS)
			mmult(buttons, vec, outcome)
			if (equal_p(outcome, target)) {
				printf "Solution for %d: %d\n", NR, p
				total_button_pushes += p
				next
			}
		}
	}
}

END {
	print "Minimal total button presses:", total_button_pushes
	# 509 is the right answer for part 1
}


function add_subsep(string1, string2, a, b, i, result)
{
	split(string1, a, SUBSEP)
	split(string2, b, SUBSEP)
	result = ""
	for (i = 1; i <= length(a); i++) {
		if (i == 1) {
			result = a[1] + b[1]
		} else {
			result = result SUBSEP (a[i] + b[i])
		}
	}
	return result
}

function equal_p(vec1, vec2, i)
{
	if (length(vec1) != length(vec2)) {
		return 0
	}
	for (i = 0; i < length(vec2); i++) {
		if (vec1[i][0] % 2 != vec2[i][0] % 2) {
			return 0
		}
	}
	return 1
}

function get_options(num_buttons, num_pushes, b, p, i, j, idx, new)
{
	b = num_buttons
	p = num_pushes
	if ((b, p) in cache) {
		return
	}
	split("", tmp, FS)
	push_button(b, tmp)
	if (p == 1) {
		for (i in tmp) {
			cache[b, p][i] = tmp[i]
		}
		return
	}
	get_options(b, p - 1)
	idx = 0
	split("", tmp2, FS)
	for (i in cache[b, p - 1]) {
		for (j in tmp) {
			tmp2[++idx] = add_subsep(cache[b, p - 1][i], tmp[j])
			# printf "%d, %d: %s\n", b, p, tmp2[idx]
		}
	}
	cache[b, p][1] = tmp2[1]
	for (i = 2; i <= idx; i++) {
		new = 1
		for (j in cache[b, p]) {
			if (tmp2[i] == cache[b, p][j]) {
				new = 0
				break
			}
		}
		if (new) {
			cache[b, p][length(cache[b, p]) + 1] = tmp2[i]
		}
	}
}

function push_button(num_buttons, output, i, j, idx)
{
	split("", output, FS)
	idx = 0
	for (i = 0; i < num_buttons; i++) {
		output[++idx] = ""
		for (j = 0; j < num_buttons; j++) {
			if (j == 0) {
				output[idx] = (i == j) ? "1" : "0"
			} else {
				output[idx] = (i == j) ? output[idx] SUBSEP "1" : output[idx] SUBSEP "0"
			}
		}
	}
}

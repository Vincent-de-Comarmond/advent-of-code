{
	split($0, tmp, FS)
	v = issafe(tmp)
	v = (v == 0) ? anysafe(tmp) : v
	safe += v
}

END {
	print safe
}


function anysafe(input_array, i, j)
{
	for (i = 1; i <= length(input_array); i++) {
		split("", _tmp, FS)
		for (j = 1; j <= length(input_array); j++) {
			if (i != j) {
				_tmp[length(_tmp) + 1] = input_array[j]
			}
		}
		if (issafe(_tmp) == 1) {
			return 1
		}
	}
	return 0
}

function issafe(input_array, k, a, b, c, diff)
{
	for (k = 2; k <= length(input_array); k++) {
		c = input_array[k]
		b = input_array[k - 1]
		diff = (c >= b) ? c - b : b - c
		if (diff < 1 || diff > 3) {
			return 0
		}
		if (k == 2) {
			continue
		}
		if (k > 2) {
			a = input_array[k - 2]
			if (! ((a < b && b < c) || (a > b && b > c))) {
				return 0
			}
		}
	}
	return 1
}

function printarray(input_array, i, output)
{
	output = ""
	for (i = 1; i <= length(input_array); i++) {
		if (i == 1) {
			output = input_array[i]
		} else {
			output = output " " input_array[i]
		}
	}
	printf "%s\n", output
}

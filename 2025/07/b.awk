BEGIN {
	FS = ""
	prev = 0
	curr = 1
}

NR == 1 {
	buffer[curr][index($0, "S")] = 1
}

/\^/ {
	prev = curr
	curr = ! curr
	for (i = 1; i <= NF; i++) {
		buffer[curr][i] = 0
	}
	for (i = 1; i <= NF; i++) {
		if ($i == "^") {
			buffer[curr][i] = 0
			buffer[curr][i - 1] += buffer[prev][i]
			buffer[curr][i + 1] += buffer[prev][i]
		} else {
			buffer[curr][i] += buffer[prev][i]
		}
	}
}

END {
	paths = 0
	for (i = 1; i <= NF; i++) {
		paths += buffer[curr][i]
	}
	print "Number paths:", paths
	# 231507396180012 is the right answer for part 2
}


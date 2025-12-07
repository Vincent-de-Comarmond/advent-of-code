BEGIN {
	FS = ""
	split("", buffer, "")
}

NR == 1 {
	par = (NR % 2)
	for (i = 1; i <= NF; i++) {
		buffer[par][i] = 0
	}
	buffer[par][index($0, "S")] = 1
}

1 < NR {
	ppar = (NR - 1) % 2
	par = NR % 2
	for (i = 1; i <= NF; i++) {
		buffer[par][i] = 0
	}
	for (i = 1; i <= NF; i++) {
		if ($i != "^") {
			if (buffer[ppar][i]) {
				buffer[par][i] += buffer[ppar][i]
			}
			continue
		}
		if (0 < buffer[ppar][i]) {
			buffer[par][i] = 0
			if (1 < i) {
				buffer[par][i - 1] += buffer[ppar][i]
			}
			if (i < NF) {
				buffer[par][i + 1] += buffer[ppar][i]
			}
		}
	}
}

END {
	paths = 0
	for (i = 1; i <= NF; i++) {
		paths += buffer[par][i]
	}
	print "Number paths:", paths
}

# 231507396180012 is the right answer for part 2

BEGIN {
	FS = ""
	splits = 0
	split("", indicies, "")
}

NR == 1 {
	indicies[index($0, "S")] = 1
}

/^/ {
	for (i = 1; i <= NF; i++) {
		if ($i != "^") {
			continue
		}
		if (indicies[i] == 1) {
			splits++
			delete indicies[i]
			if (1 < i) {
				indicies[i - 1] = 1
			}
			if (i < NF) {
				indicies[i + 1] = 1
			}
		}
	}
}

END {
    print "Number splits:", splits
}

# 1717 is the right answer for part 1

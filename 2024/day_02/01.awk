{
	for (k = 2; k <= NF; k++) {
		i = k - 2
		j = k - 1
		diff = ($k >= $j) ? $k - $j : $j - $k
		if (diff < 1 || diff > 3) {
			next
		}
		if (i == 0) {
			continue
		}
		if (! (($i < $j && $j < $k) || ($i > $j && $j > $k))) {
			next
		}
	}
	safe += 1
}

END {
	print safe
}


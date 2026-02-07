/x/ {
	gsub(/:/, "", $0)
	gsub(/x/, " ", $0)
	split($0, a, " ")
	x = a[1]
	y = a[2]
	split("", desired, FS)
	num_desired = 0
	for (i = 3; i <= length(a); i++) {
		num_desired += a[i]
	}
	if (num_desired <= int(x / 3) * int(y / 3)) {
		total += 1
	}
}

END {
	printf "Total packable: %d\n", total
}

# 403 is the correct answer

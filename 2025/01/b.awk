BEGIN {
	num_zeros = 0
	value = 50
}

/L/ {
	value = value == 0 ? 100 : value
	value -= substr($0, 2)
}

/R/ {
	value = value == 100 ? 0 : value
	value += substr($0, 2)
}

{
	while ((value < 0) || (100 < value)) {
		value += (value < 0) ? 100 : -100
		num_zeros++
	}
	if ((0 == value) || (value == 100)) {
		num_zeros++
	}
}

END {
	print "Password is:", num_zeros
}

# 6295 is the right answer

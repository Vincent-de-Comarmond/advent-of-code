BEGIN {
	num_zeros = 0
	value = 50
}

/L/ {
	value = positive_mod(value - substr($0, 2), 100)
}

/R/ {
	value = positive_mod(value + substr($0, 2), 100)
}

{
	num_zero += value == 0 ? 1 : 0
}

END {
	print "Password is:", num_zero
}


function positive_mod(x, base)
{
	return ((x % base) + base) % base
}


# 1052 is the right answer for part 1

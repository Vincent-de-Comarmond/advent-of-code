BEGIN { FS = "|" }

/[0-9]+\|[0-9]+/ { rules[$1][$2] = 1 }

/^[[:space:]]*$/ { FS = "," }

/,/ {
	for (i = 1; i <= NF; i++) {
		if (isarray(rules[$i])) {
			for (j in rules[$i]) {
				regexp = j ".*" $i
				if ($0 ~ regexp) fix_input_and_count()
			}
		}
	}
}
END { print total }


function custom_comparitor(i1, v1, i2, v2, l, r)
{
	if (isarray(rules[v1]) && (v2 in rules[v1])) return -1
	if (isarray(rules[v2]) && (v1 in rules[v2])) return 1
	return 0
}

function fix_input_and_count(tmp, sorted)
{
	split($0, tmp, FS)
	asort(tmp, sorted, "custom_comparitor")
	total += sorted[int(1 + NF / 2)]
	next
}
# Correct answer is 5285

BEGIN {
	SUBSEP = ","
	split("", puzzle, "")
	split("", inverse, "")
	split("", all_parents, "")
}

{
	key = substr($1, 1, length($1) - 1)
	all_parents[key] = 1
	for (i = 2; i <= NF; i++) {
		puzzle[key][$i] = 1
		inverse[$i][key] = 1
		all_parents[$i] = 1
	}
}

END {
	split("", empty, FS)
	populate_parents("dac", dac_parents)
	populate_parents("fft", fft_parents)
	if ("fft" in dac_parents) {
		svr2fft = solve("svr", "fft", fft_parents)
		fft2dac = solve("fft", "dac", dac_parents)
		dac2out = solve("dac", "out", all_parents)
		print "Total possible routes:", svr2fft * fft2dac * dac2out
		exit (0)
	}
	if ("dac" in fft_parents) {
		svr2dac = solve("svr", "dac", dac_parents)
		dac2fft = solve("dac", "fft", fft_parents)
		fft2out = solve("fft", "out", all_parents)
		print "Total possible routes:", svr2dac * dac2fft * fft2out
		exit (0)
	}
	exit (1)
	# 332052564714990 is the right answer for part 2
	# Execution time less than 2 seconds
}


function populate_parents(child, populate_me)
{
	populate_me[""] = 1
	delete populate_me[""]
	start = length(populate_me)
	if (length(populate_m) == 0) {
		populate_me[child] = 1
	}
	for (i in populate_me) {
		if (i in inverse) {
			for (j in inverse[i]) {
				populate_me[j] = 1
			}
		}
	}
	end = length(populate_me)
	if (start == end) {
		return
	}
	return populate_parents(child, populate_me)
}

function solve(src, dst, parents, child, t)
{
	if (dst in puzzle[src]) {
		return 1
	} else {
		t = 0
		for (child in puzzle[src]) {
			if (child in parents) {
				t += solve(child, dst, parents, highest)
			}
		}
		return t
	}
}

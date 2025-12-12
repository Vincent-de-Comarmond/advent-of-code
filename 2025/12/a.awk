BEGIN {
	FS = ""
	split("", shapes, FS)
	row_idx = 1
	pres_idx = 1
}

/#|\./ {
	if (9 < row_idx) {
		pres_idx++
		row_idx = 1
	}
	shapes[pres_idx][row_idx++] = $1 == "#" ? 1 : 0
	shapes[pres_idx][row_idx++] = $2 == "#" ? 1 : 0
	shapes[pres_idx][row_idx++] = $3 == "#" ? 1 : 0
}

/x/ {
	gsub(/:/, "", $0)
	gsub(/x/, " ", $0)
	split($0, a, " ")
	#
	wid = a[1]
	len = a[2]
	split("", desired, FS)
	for (i = 3; i <= length(a); i++) {
		desired[i - 2] = a[i]
	}
}

END {
	for (i = 1; i <= length(shapes); i++) {
		for (j = 0; j < 3; j++) {
			print shapes[i][3 * j + 1], shapes[i][3 * j + 2], shapes[i][3 * j + 3]
		}
		print ""
	}
}

function solve_one(width, _length, desired){
    
    

    
    
}

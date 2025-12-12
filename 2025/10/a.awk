BEGIN {
	button_pushes = 0
}

{
	split($1, a, "")
	for (i = 2; i < length(a); i++) {
		target[i - 2] = a[i] == "#" ? 1 : 0
	}
	idx = 0
	split("", buttons, "")
	for (i = 2; i < NF; i++) {
		split(substr($i, 2, length($i) - 2), button, ",")
		for (j = 1; j <= length(button); j++) {
			buttons[idx][button[j]] = 1
		}
		idx++
	}
	exit 0
}

END {
	for (i = 0; i <= idx; i++) {
		for (j = 0; j < length(target); j++) {
			printf j == 0 ? "%d" : ", %d", buttons[i][j]
		}
		print ""
	}
	print "Minimal button pushes:", button_pushes
}


function solve(target, buttons, presses, current_state,
    i)
{
    for (i = 0; i <= idx; i++) {
	if 



	    
    for (i=0; i < length(target); i++){
	
		for (j = 0; j < length(target); j++) {
			printf j == 0 ? "%d" : ", %d", buttons[i][j]
		}
		print ""
	}
	
    }
    



	
}

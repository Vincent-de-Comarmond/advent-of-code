{
	split($0, tmp, FS)
	for (j=1; j<=NF;j++) array_in[NR][j]=tmp[j]
}

END {
    for (j=1;j <= 25; j++) applyrules(array_in)
    print length(array_in[length(array_in)])
    ## 183484 is the right answer for part 1
}


function applyrules(input,         i, t, n){
	n=length(input)

	for (i = 1; i <= length(input[n]); i++) {
	    t = input[n][i]
	    if (t == 0) {
		input[n + 1][length(input[n+1]) + 1] = 1
	    } else if (length(t) % 2 == 0) {
		input[n+1][length(input[n+1]) + 1] = substr(t, 1, int(length(t) / 2)) + 0
		input[n+1][length(input[n+1]) + 1] = substr(t, int(length(t) / 2) + 1) + 0
	    } else {
		input[n+1][length(input[n+1]) + 1] = t * 2024
	    }
	}
}

function walk_array(arr, name,      i)
{
    for (i in arr) {
        if (isarray(arr[i])) walk_array(arr[i], (name "[" i "]"))
        else printf("%s[%02d] = %s\n", name, i, arr[i])
    }
}

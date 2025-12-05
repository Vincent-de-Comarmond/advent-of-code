BEGIN {
FS=","
total=0
}

{
    for (i=1; i <=NF; i++){
        split($i, limits, "-")
        for (j=limits[1]; j <=limits[2]; j++){
	    k=length(j)/2
	    if (k != int(k)) continue;
	    for (l=1; l <= length(j) - k; l++){
	        a = substr(j, l, k)
		b = substr(j, l+k, k)
		if (a == b){
		    # printf("Range: %d -> %d\n", limits[1], limits[2])
		    # print("Found repeat", j)
		    total+= j
		}
	    }
        }
    }
}

END {
    print("Invalid sum:", total)
}

# 19386344315 is the right answer for part 1
